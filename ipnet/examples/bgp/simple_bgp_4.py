from mininet.log import setLogLevel

from ipnet import IPNetwork, CLIX


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    r1 = net.addFRR("r1", defaultRoute="via 192.168.12.2")
    r2 = net.addBGPRouter("r2",
                          router_id="2.2.2.2",
                          as_number=65001,
                          bgp_networks=["2.2.2.2/32", "192.168.12.0/24", "192.168.23.0/24"],
                          bgp_peers=[{"neighbor": "r2-eth1 interface", "remote_as": "external"}])
    r3 = net.addBGPRouter("r3",
                          router_id="3.3.3.3",
                          as_number=65002,
                          bgp_networks=["3.3.3.3/32", "192.168.34.0/24", "192.168.23.0/24"],
                          bgp_peers=[{"neighbor": "r3-eth0 interface", "remote_as": "external"}])
    r4 = net.addFRR("r4", defaultRoute="via 192.168.34.1")

    net.addLink(r1, r2,
                intfName1="r1-eth0", params1={"ip": "192.168.12.1/24"},
                intfName2="r2-eth0", params2={"ip": "192.168.12.2/24"})
    net.addLink(r2, r3,
                intfName1="r2-eth1", params1={"ip": "192.168.23.1/24"},
                intfName2="r3-eth0", params2={"ip": "192.168.23.2/24"})
    net.addLink(r3, r4,
                intfName1="r3-eth1", params1={"ip": "192.168.34.1/24"},
                intfName2="r4-eth0", params2={"ip": "192.168.34.2/24"})

    net.start()
    print(r2.vtysh_cmd("show bgp summary"))
    print(r3.vtysh_cmd("show bgp summary"))

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
