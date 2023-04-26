from mininet.log import setLogLevel

from ipnet import IPNetwork, CLIX, VPP


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    for i in range(1, 5):
        net.addSRv6Router("r{}".format(i), inNamespace=True)
        net.addRouter("r{}".format(i), inNamespace=True, cls=VPP)

    h1 = net.addSRv6Router('h1')
    h2 = net.addSRv6Router('h2')

    net.addLink("r1", h1,
                intfName1="r1_h1",
                intfName2="h1_r1", params2={"ip": "192.168.1.2/24"})
    net.get("h1").cmd("ip route add default dev h1_r1 via 192.168.1.1")

    net.addLink("r4", h2,
                intfName1="r4_h2",
                intfName2="h2_r4", params2={"ip": "192.168.2.2/24"})
    net.get("h2").cmd("ip route add default dev h2_r4 via 192.168.2.1")

    net.addLink("r1", "r2", intfName1="r1_r2", intfName2="r2_r1")
    net.addLink("r1", "r3", intfName1="r1_r3", intfName2="r3_r1")

    net.addLink("r2", "r4", intfName1="r2_r4", intfName2="r4_r2")
    net.addLink("r2", "r3", intfName1="r2_r3", intfName2="r3_r2")

    net.addLink("r3", "r4", intfName1="r3_r4", intfName2="r4_r3")

    net.start()

    net.get("h1").cmd("ip -6 addr add fd00:1::2/64 dev h1_r1")
    net.get("h1").cmd("ip -6 route add default dev h1_r1 via fd00:1::1")
    net.get("r1").vppctl("set interface ip address host-r1_h1 fd00:1::1/64")
    net.get("r1").vppctl("set interface ip address host-r1_h1 192.168.1.1/24")

    net.get("h2").cmd("ip -6 addr add fd00:2::2/64 dev h2_r4")
    net.get("h2").cmd("ip -6 route add default dev h2_r4 via fd00:2::1")
    net.get("r4").vppctl("set interface ip address host-r4_h2 fd00:2::1/64")
    net.get("r4").vppctl("set interface ip address host-r4_h2 192.168.2.1/24")

    net.get("r1").vppctl("set interface ip address host-r1_r2 fd00:a::1/64")
    net.get("r2").vppctl("set interface ip address host-r2_r1 fd00:a::2/64")

    net.get("r1").vppctl("set interface ip address host-r1_r3 fd00:b::1/64")
    net.get("r3").vppctl("set interface ip address host-r3_r1 fd00:b::2/64")

    net.get("r2").vppctl("set interface ip address host-r2_r3 fd00:c::1/64")
    net.get("r3").vppctl("set interface ip address host-r3_r2 fd00:c::2/64")

    net.get("r2").vppctl("set interface ip address host-r2_r4 fd00:d::1/64")
    net.get("r4").vppctl("set interface ip address host-r4_r2 fd00:d::2/64")

    net.get("r3").vppctl("set interface ip address host-r3_r4 fd00:e::1/64")
    net.get("r4").vppctl("set interface ip address host-r4_r3 fd00:e::2/64")
    
    net.get("r1").vppctl("set sr encaps source addr fd00:bbbb:a::")
    net.get("r1").vppctl("sr localsid address fd00:bbbb:a:: behavior end")
    net.get("r1").vppctl("ip route add fd00:bbbb:b::/48 via fd00:a::2 host-r1_r2")
    net.get("r1").vppctl("ip route add fd00:bbbb:c::/48 via fd00:b::2 host-r1_r3")
    net.get("r1").vppctl("ip route add fd00:bbbb:d::/48 via fd00:a::2 host-r1_r2")
    net.get("r1").vppctl("ip route add fd00:bbbb:d::/48 via fd00:b::2 host-r1_r3")

    net.get("r2").vppctl("set sr encaps source addr fd00:bbbb:b::")
    net.get("r2").vppctl("sr localsid address fd00:bbbb:b:: behavior end")
    net.get("r2").vppctl("ip route add fd00:bbbb:a::/48 via fd00:a::1 host-r2_r1")
    net.get("r2").vppctl("ip route add fd00:bbbb:d::/48 via fd00:d::2 host-r2_r4")

    net.get("r3").vppctl("set sr encaps source addr fd00:bbbb:c::")
    net.get("r3").vppctl("sr localsid address fd00:bbbb:c:: behavior end")
    net.get("r3").vppctl("ip route add fd00:bbbb:a::/48 via fd00:b::1 host-r3_r1")
    net.get("r3").vppctl("ip route add fd00:bbbb:d::/48 via fd00:e::2 host-r3_r4")

    net.get("r4").vppctl("set sr encaps source addr fd00:bbbb:d::")
    net.get("r4").vppctl("sr localsid address fd00:bbbb:d:: behavior end")
    net.get("r4").vppctl("ip route add fd00:bbbb:b::/48 via fd00:d::1 host-r4_r2")
    net.get("r4").vppctl("ip route add fd00:bbbb:c::/48 via fd00:e::1 host-r4_r3")
    net.get("r4").vppctl("ip route add fd00:bbbb:a::/48 via fd00:d::1 host-r4_r2")
    net.get("r4").vppctl("ip route add fd00:bbbb:a::/48 via fd00:e::1 host-r4_r3")
    
    net.get("r1").vppctl("sr localsid address fd00:bbbb:a::4 behavior end.dt4 0")
    net.get("r1").vppctl("sr policy add bsid fd00:bbbb:a::e4 next fd00:bbbb:d::4 encap")
    net.get("r1").vppctl("sr steer l3 192.168.2.0/24 via bsid fd00:bbbb:a::e4")
    
    net.get("r4").vppctl("sr localsid address fd00:bbbb:d::4 behavior end.dt4 0")
    net.get("r4").vppctl("sr policy add bsid fd00:bbbb:d::e4 next fd00:bbbb:a::4 encap")
    net.get("r4").vppctl("sr steer l3 192.168.1.0/24 via bsid fd00:bbbb:d::e4")

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
