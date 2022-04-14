from mininet.log import setLogLevel

from frrnet.frr_net import FRRNetwork, CLIWithVtysh


def main():
    setLogLevel("info")
    net = FRRNetwork()

    h1 = net.addHost("h1")
    h3 = net.addHost("h3")
    h2 = net.addHost("h2")

    net.addLink(h1, h3)
    net.addLink(h3, h2)

    net.start()
    CLIWithVtysh(net)
    net.stop()


if __name__ == '__main__':
    main()