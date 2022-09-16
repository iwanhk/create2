from scripts.functions import *


def bump(i):
    if Deployer[-1].getAddress(i)[:6] == '0x8888':
        print(f"Found {i}")
    # pbar.update(1)


def main():
    active_network = network.show_active()
    print("Current Network:" + active_network)

    admin, creator, consumer, iwan = get_accounts(active_network)

    try:
        if active_network in LOCAL_NETWORKS:
            pass

        if active_network in TEST_NETWORKS:
            # fac = Factory.deploy(addr(admin))
            # print(faca.deployRecords(0))
            pass

        if active_network in REAL_NETWORKS:
            faca = FactoryAssembly[-1]
            print(faca.deployRecords(0))

    except Exception:
        console.print_exception()
        # Test net contract address


if __name__ == "__main__":
    main()
