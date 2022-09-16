# %%
from conflux_web3.dev import get_testnet_web3
from cfx_address import Base32Address
import json
import random
import os

w3 = get_testnet_web3()

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
# salt = random.randint(1, 1145141919810)
for salt in range(1145141919810):
    target_address = create2factory.functions.deploy(
        j_["bytecode"], salt).call()
    print(str(salt) + '      ['+target_address[:6]+']')
    if target_address[3:6] == '888' or target_address[3:6] == '000' or target_address[3:6] == '000':
        print(f"salt {salt}: {target_address}")
target_address = Base32Address(target_address, w3.cfx.chain_id, verbose=True)
print(f"salt {salt}: {target_address}")

# %%
m = input("Ready to deploy? y/n\n")

if m == "y":
    print(f"begin deployment...")
    create2factory.functions.deploy(j_["bytecode"], salt).transact().executed()
    print(f"successfully deployed at {target_address}")
