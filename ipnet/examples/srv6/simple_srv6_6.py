from mininet.log import setLogLevel

from ipnet import IPNetwork, CLIX


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    for i in range(1, 5):
        net.addSRv6Router("r{}".format(i), inNamespace=True)
        
    h1 = net.addSRv6Router('h1')
    h2 = net.addSRv6Router('h2')

    net.addLink("r1", h1,
                intfName1="r1_h1", params1={"ip": "192.168.1.1/24"},
                intfName2="h1_r1", params2={"ip": "192.168.1.2/24"})
    net.get("h1").cmd("ip route add default dev h1_r1 via 192.168.1.2")

    net.addLink("r4", h2,
                intfName1="r4_h2", params1={"ip": "192.168.2.1/24"},
                intfName2="h2_r4", params2={"ip": "192.168.2.2/24"})
    net.get("h2").cmd("ip route add default dev h2_r4 via 192.168.2.2")

    net.addLink("r1", "r2", intfName1="r1_r2", intfName2="r2_r1")
    net.addLink("r1", "r3", intfName1="r1_r3", intfName2="r3_r1")

    net.addLink("r2", "r4", intfName1="r2_r4", intfName2="r4_r2")
    net.addLink("r2", "r3", intfName1="r2_r3", intfName2="r3_r2")

    net.addLink("r3", "r4", intfName1="r3_r4", intfName2="r4_r3")

    net.start()

    net.get("h1").cmd("ip -6 addr add fd00:1::1/64 dev h1_r1")
    net.get("h1").cmd("ip -6 route add default dev h1_r1 via fd00:1::2")
    net.get("r1").set_ipv6_cmd("fd00:1::2/64", "r1_h1")

    net.get("h2").cmd("ip -6 addr add fd00:2::1/64 dev h2_r4")
    net.get("h2").cmd("ip -6 route add default dev h2_r4 via fd00:2::2")
    net.get("r4").set_ipv6_cmd("fd00:2::2/64", "r4_h2")

    net.get("r1").set_ipv6_cmd("fd00:a::1/64", "r1_r2")
    net.get("r2").set_ipv6_cmd("fd00:a::2/64", "r2_r1")

    net.get("r1").set_ipv6_cmd("fd00:b::1/64", "r1_r3")
    net.get("r3").set_ipv6_cmd("fd00:b::2/64", "r3_r1")

    net.get("r2").set_ipv6_cmd("fd00:c::1/64", "r2_r3")
    net.get("r3").set_ipv6_cmd("fd00:c::2/64", "r3_r2")

    net.get("r2").set_ipv6_cmd("fd00:d::1/64", "r2_r4")
    net.get("r4").set_ipv6_cmd("fd00:d::2/64", "r4_r2")

    net.get("r3").set_ipv6_cmd("fd00:e::1/64", "r3_r4")
    net.get("r4").set_ipv6_cmd("fd00:e::2/64", "r4_r3")

    # add route
    net.get("r1").cmd("ip -6 route add fd00:2::1/128 encap seg6 mode inline segs fd00:a::2,fd00:d::2 dev r1_r2")
    net.get("r4").cmd("ip -6 route add fd00:1::1/128 encap seg6 mode inline segs fd00:e::1,fd00:b::1 dev r4_r3")

    return net


if __name__ == "__main__":
    net = setup()
    # add route
    net.get("r1").cmd("ip -6 route add fd00:2::1/128 encap seg6 mode inline segs fd00:a::2,fd00:d::2 dev r1_r2")
    net.get("r4").cmd("ip -6 route add fd00:1::1/128 encap seg6 mode inline segs fd00:e::1,fd00:b::1 dev r4_r3")
    CLIX(net)
    net.stop()
