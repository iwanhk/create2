# %%
from conflux_web3.dev import get_mainnet_web3
from cfx_address import Base32Address
import json
import random
import os


def loadIndex():
    with open('./index', 'r') as f:
        return int(f.readline().strip())


def writeIndex(index):
    with open('./index', 'w') as f:
        return int(f.write(str(index)))


w3 = get_mainnet_web3()

secret = os.environ.get("NEWBIE_PRIVATE_KEY")
account = w3.account.from_key(secret)
w3.cfx.default_account = w3.account.from_key(secret)
w3.wallet.add_account(account)

# %%
j = json.load(open("./Create2Factory.json"))
j_ = json.load(open("./Registry.json"))

# the hex address of create2factory is 0x8A3A92281Df6497105513B18543fd3B60c778E40 in every network.
# See https://github.com/Conflux-Chain/CIPs/blob/master/CIPs/cip-31.md for more information
create2factory = w3.cfx.contract(
    address=Base32Address(
        "0x8A3A92281Df6497105513B18543fd3B60c778E40", w3.cfx.chain_id),
    abi=j["abi"],
)

# %%
salt = 0
while salt < 1145141919810:
    salt = loadIndex()
    target_address = create2factory.functions.deploy(
        j_["bytecode"], salt).call()
    mark = target_address[-3:].lower()
    print(f"[{mark}] - {salt}")
    if mark == 'bee':
        print(f"salt {salt}: {target_address}")
        with open('result', 'w+') as f:
            f.write(f"salt {salt}: {target_address}")
        break
    salt += 1
    writeIndex(salt)
target_address = Base32Address(target_address, w3.cfx.chain_id, verbose=True)
print(f"salt {salt}: {target_address}")

# %%
m = input("Ready to deploy? y/n\n")

if m == "y":
    print(f"begin deployment...")
    create2factory.functions.deploy(j_["bytecode"], salt).transact().executed()
    print(f"successfully deployed at {target_address}")
