from mininet.log import setLogLevel

from frrnet.frr_net import FRRNetwork, CLIWithVtysh


def main():
    setLogLevel("info")
    net = FRRNetwork()
    
    for i in range(1, 5):
        net.addFRR("leaf{}".format(i))
        
    for i in range(1, 2):
        net.addFRR("spine{}".format(i))

    for i in range(1, 3):
        net.addHost("s{}".format(i))

    net.start()
    CLIWithVtysh(net)
    net.stop()


if __name__ == '__main__':
    main()

