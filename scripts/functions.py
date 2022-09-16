from web3 import Web3
from brownie import Factory, FactoryAssembly, Deployer, accounts, network, config, web3, convert
from scripts.tools import *
import os
import zlib
# from import webdriver

D18 = 10**18
ZERO = '0x0000000000000000000000000000000000000000'
active_network = network.show_active()

LOCAL_NETWORKS = ['development', 'mainnet-fork', 'polygon-fork']
TEST_NETWORKS = ['rinkeby', 'bsc-test', 'mumbai']
REAL_NETWORKS = ['mainnet', 'polygon', 'wuhan']
DEPLOYED_ADDR = {  # Deployed address
    'rinkeby': "",
    'mumbai': ""
}


def get_accounts(active_network):
    if active_network in LOCAL_NETWORKS:
        admin = accounts.add(config['wallets']['admin'])
        creator = accounts.add(config['wallets']['creator'])
        consumer = accounts.add(config['wallets']['consumer'])
        iwan = accounts.add(config['wallets']['iwan'])

        accounts[0].transfer(admin, "100 ether")
        accounts[1].transfer(creator, "100 ether")
        accounts[2].transfer(consumer, "100 ether")
        accounts[3].transfer(iwan, "100 ether")

    else:
        admin = accounts.add(config['wallets']['admin'])
        creator = accounts.add(config['wallets']['creator'])
        consumer = accounts.add(config['wallets']['consumer'])
        iwan = accounts.add(config['wallets']['iwan'])

    balance_alert(admin, "admin")
    balance_alert(creator, "creator")
    balance_alert(consumer, "consumer")
    balance_alert(iwan, "iwan")
    return [admin, creator, consumer, iwan]


def flat_contract(name: str, meta_data: dict) -> None:
    if not os.path.exists(name + '_flat'):
        os.mkdir(name + '_flat')

    with open(name + '_flat/settings.json', 'w') as f:
        json.dump(meta_data['standard_json_input']['settings'], f)

    for file in meta_data['standard_json_input']['sources'].keys():
        print(f"Flatten file {name+ '_flat/'+ file} ")
        with open(name + '_flat/' + file, 'w') as f:
            content = meta_data['standard_json_input']['sources'][file]['content'].split(
                '\n')

            for line in content:
                if 'import "' in line:
                    f.write(line.replace('import "', 'import "./')+'\n')
                    continue
                if '    IERC1820Registry internal constant _ERC1820_REGISTRY = IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);' in line:
                    f.write(
                        '    IERC1820Registry internal constant _ERC1820_REGISTRY = IERC1820Registry(0x88887eD889e776bCBe2f0f9932EcFaBcDfCd1820);//Conflux')
                    continue

                f.write(line+'\n')
            f.write(f'\n// Generated by {__file__} \n')


def chrome():
    options = webdriver.ChromeOptions()
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")

    driver = webdriver.Chrome(options=options)
    return driver


def deflate(data, compresslevel=9):
    compress = zlib.compressobj(
        compresslevel,        # level: 0-9
        zlib.DEFLATED,        # method: must be DEFLATED
        -zlib.MAX_WBITS,      # window size in bits:
        #   -15..-8: negate, suppress header
        #   8..15: normal
        #   16..30: subtract 16, gzip header
        zlib.DEF_MEM_LEVEL,   # mem level: 1..8/9
        0                     # strategy:
        #   0 = Z_DEFAULT_STRATEGY
        #   1 = Z_FILTERED
        #   2 = Z_HUFFMAN_ONLY
        #   3 = Z_RLE
        #   4 = Z_FIXED
    )
    deflated = compress.compress(data)
    deflated += compress.flush()
    return deflated


def makeInt(x, y, width=100, height=100):
    return y + x*(2 << 63) + (height+y)*(2 << 127) + (width+x)*(2 << 191)


def loadComponentData(dir, template, user):
    files = os.listdir(dir)
    for file in files:  # 遍历文件夹
        # 判断是否是文件夹，不是文件夹才打开
        if not os.path.isdir(file) and file[-4:] == '.svg':
            with open(dir + "/" + file) as f:
                buffer = f.read()
                # remove the first line
                buffer = buffer[buffer.index('\n')+1:]
                compress_data = deflate(str.encode(buffer))
                file = file[:file.index('-svgrepo-com.svg')]
                template.upload(file, compress_data, len(buffer), addr(user))
                # tx.wait(1)
                print(
                    f"{file} {len(buffer)} compressed to {int(len(compress_data)*100/len(buffer))}%")


def abiEncode(contract):
    all_functions = ''
    web3_f = web3.eth.contract(address=contract.address, abi=contract.abi)
    for func in web3_f.all_functions():
        name = str(func)[10:-1]
        all_functions += name + " : "+Web3.keccak(text=name)[:4].hex() + "\n"
    all_functions += 'Type function with arguments to generate data. exit to quit:\n\n'

    while True:
        choice = input(all_functions)
        if choice == 'q' or choice == '':
            break
        # print("web3_f.functions."+choice+".buildTransaction()")
        print(eval("web3_f.functions."+choice+".buildTransaction()")['data'])
    # transaction= web3_f.functions.mint(Base32Address.encode(str(consumer), 1), 1, addr(admin)).buildTransaction() # 获得函数调用的transaction
    # print(transaction['data'])
