from scripts.functions import *
import sys

RANGE = 0xfffffff


def main():
    active_network = network.show_active()
    print("Current Network:" + active_network)

    admin, creator, consumer, iwan = get_accounts(active_network)

    try:
        if active_network in LOCAL_NETWORKS:
            # pool = ThreadPool(100)
            # pbar = tqdm(desc="bumping...", total=RANGE)

            # # pool.map(bump, list(range(RANGE)))
            # deployer = Deployer[-1]
            # for i in range(RANGE):
            #     if deployer.getAddress(i)[-4:] == '8888':
            #         print(f"Found {i}")
            #         break
            #     pbar.update(1)
            # pool.close()
            # pool.join()
            j_ = json.load(open("./build/contracts/Registry.json"))
            newbie1 = accounts.load('newbie1')
            admin.transfer(newbie1, 10*10**18)
            dep = Deployer.deploy(addr(newbie1))

            i = 0
            while i < RANGE:
                _a = dep.getAddress(j_['bytecode'], i)
                if _a[-3:].lower() == 'bee':
                    print(f"\n\nsalt={i}  {_a=}")
                    break
                if i % 10 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                i += 1

        if active_network in TEST_NETWORKS:
            # fac = Factory.deploy(addr(admin))
            # faca = FactoryAssembly.deploy(addr(admin))
            # # fac.Deploy("Database", addr(admin))
            # bytecode = faca.getBytecode(admin, 0)
            # faca.Deploy(bytecode, 255, addr(admin))
            # faca.Deploy(bytecode, 256, addr(admin))
            # print(faca.deployRecords(0))
            # print(faca.deployRecords(1))
            pass

        if active_network in REAL_NETWORKS:
            # fac = Factory.deploy(addr(admin))
            # faca = FactoryAssembly.deploy(addr(admin))
            # # fac.Deploy("Database", addr(admin))
            # bytecode = faca.getBytecode(admin, 0)
            # faca.Deploy(bytecode, 0, addr(admin))
            # print(faca.deployRecords(0))
            pass

    except Exception:
        console.print_exception()
        # Test net contract address


if __name__ == "__main__":
    main()
