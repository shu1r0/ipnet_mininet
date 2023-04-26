from mininet.log import setLogLevel

from ipnet import IPNetwork, CLIX, VPP, IPNode


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    h1 = net.addHost('h1', cls=IPNode)
    h2 = net.addHost('h2', cls=IPNode)

    vpp1 = net.addRouter('vpp1', cls=VPP)

    net.addLink(h1, vpp1, intfName1="h1_vpp1", intfName2="vpp1_h1")
    net.addLink(h2, vpp1, intfName1="h2_vpp1", intfName2="vpp1_h2")

    net.start()

    h1.set_ip_cmd("192.168.100.1/24", "h1_vpp1")
    h2.set_ip_cmd("192.168.100.2/24", "h2_vpp1")

    vpp1.vppctl("set int l2 bridge host-vpp1_h1 1")
    vpp1.vppctl("set int l2 bridge host-vpp1_h2 1")

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()


