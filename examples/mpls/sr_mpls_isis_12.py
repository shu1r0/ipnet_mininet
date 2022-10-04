"""
References:
    * http://www.uni-koeln.de/~pbogusze/posts/FRRouting_SR_Segment_Routing_tech_demo.html
    * http://docs.frrouting.org/projects/dev-guide/en/latest/ospf-sr.html
    * https://blog.swineson.me/en/use-linux-as-an-mpls-router/
    * https://tex2e.github.io/rfc-translater/html/rfc8660.html
"""
from mininet.log import setLogLevel

from ipnet import IPNetwork, FRR, IPNode, CLIX, MPLSRouter


r1_conf = """\
configure terminal
interface r1_h1
  ip router isis 1
interface r1_r2
  ip router isis 1
interface lo
  ip address 10.0.0.1/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0001.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.1
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.1/32 index 100
exit
"""

r2_conf = """\
configure terminal
interface r2_r1
  ip router isis 1
interface r2_r3
  ip router isis 1
interface r2_r6
  ip router isis 1
interface lo
  ip address 10.0.0.2/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0002.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.2
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.2/32 index 200
exit
"""

r3_conf = """\
configure terminal
interface r3_r2
  ip router isis 1
interface r3_r4
  ip router isis 1
interface r3_r5
  ip router isis 1
interface lo
  ip address 10.0.0.3/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0003.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.3
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.3/32 index 300
exit
"""

r4_conf = """\
configure terminal
interface r4_r3
  ip router isis 1
interface r4_h3
  ip router isis 1
interface lo
  ip address 10.0.0.4/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0004.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.4
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.4/32 index 400
exit
"""

r5_conf = """\
configure terminal
interface r5_h2
  ip router isis 1
interface r5_r6
  ip router isis 1
interface lo
  ip address 10.0.0.5/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0005.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.5
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.5/32 index 500
exit
"""

r6_conf = """\
configure terminal
interface r6_r2
  ip router isis 1
interface r6_r5
  ip router isis 1
interface r6_r7
  ip router isis 1
interface lo
  ip address 10.0.0.6/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0006.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.6
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.6/32 index 600
exit
"""

r7_conf = """\
configure terminal
interface r7_r3
  ip router isis 1
interface r7_r6
  ip router isis 1
interface r7_r8
  ip router isis 1
interface lo
  ip address 10.0.0.7/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0007.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.7
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.7/32 index 700
exit
"""

r8_conf = """\
configure terminal
interface r8_r7
  ip router isis 1
interface r8_h4
  ip router isis 1
interface lo
  ip address 10.0.0.8/32
  ip router isis 1
router isis 1
  net 49.0000.0000.0000.0008.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.0.0.8
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.8/32 index 800
exit
"""


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    # FRRouting Router
    r1 = net.addFRR("r1", enable_daemons=["isisd"], cls=MPLSRouter)
    r2 = net.addFRR("r2", enable_daemons=["isisd"], cls=MPLSRouter)
    r3 = net.addFRR("r3", enable_daemons=["isisd"], cls=MPLSRouter)
    r4 = net.addFRR("r4", enable_daemons=["isisd"], cls=MPLSRouter)
    r5 = net.addFRR("r5", enable_daemons=["isisd"], cls=MPLSRouter)
    r6 = net.addFRR("r6", enable_daemons=["isisd"], cls=MPLSRouter)
    r7 = net.addFRR("r7", enable_daemons=["isisd"], cls=MPLSRouter)
    r8 = net.addFRR("r8", enable_daemons=["isisd"], cls=MPLSRouter)

    # host
    h1: IPNode = net.addHost("h1", cls=IPNode)
    h2: IPNode = net.addHost("h2", cls=IPNode)
    h3: IPNode = net.addHost("h3", cls=IPNode)
    h4: IPNode = net.addHost("h4", cls=IPNode)

    # config link
    net.addLink(r1, h1,
                intfName1="r1_h1", params1={"ip": "192.168.1.1/24"},
                intfName2="h1_r1", params2={"ip": "192.168.1.2/24"})
    net.addLink(r1, r2,
                intfName1="r1_r2", params1={"ip": "192.168.12.1/24"},
                intfName2="r2_r1", params2={"ip": "192.168.12.2/24"})
    net.addLink(r2, r3,
                intfName1="r2_r3", params1={"ip": "192.168.23.1/24"},
                intfName2="r3_r2", params2={"ip": "192.168.23.2/24"})
    net.addLink(r2, r6,
                intfName1="r2_r6", params1={"ip": "192.168.26.1/24"},
                intfName2="r6_r2", params2={"ip": "192.168.26.2/24"})
    net.addLink(r3, r4,
                intfName1="r3_r4", params1={"ip": "192.168.34.1/24"},
                intfName2="r4_r3", params2={"ip": "192.168.34.2/24"})
    net.addLink(r3, r7,
                intfName1="r3_r7", params1={"ip": "192.168.37.1/24"},
                intfName2="r7_r3", params2={"ip": "192.168.37.2/24"})
    net.addLink(r4, h3,
                intfName1="r4_h3", params1={"ip": "192.168.3.1/24"},
                intfName2="h3_r4", params2={"ip": "192.168.3.2/24"})
    net.addLink(r5, h2,
                intfName1="r5_h2", params1={"ip": "192.168.2.1/24"},
                intfName2="h2_r5", params2={"ip": "192.168.2.2/24"})
    net.addLink(r5, r6,
                intfName1="r5_r6", params1={"ip": "192.168.56.1/24"},
                intfName2="r6_r5", params2={"ip": "192.168.56.2/24"})
    net.addLink(r6, r7,
                intfName1="r6_r7", params1={"ip": "192.168.67.1/24"},
                intfName2="r7_r6", params2={"ip": "192.168.67.2/24"})
    net.addLink(r7, r8,
                intfName1="r7_r8", params1={"ip": "192.168.78.1/24"},
                intfName2="r8_r7", params2={"ip": "192.168.78.2/24"})
    net.addLink(r8, h4,
                intfName1="r8_h4", params1={"ip": "192.168.4.1/24"},
                intfName2="h4_r8", params2={"ip": "192.168.4.2/24"})
    
    h1.add_default_route_cmd("h1_r1", "192.168.1.1")
    h2.add_default_route_cmd("h2_r5", "192.168.2.1")
    h3.add_default_route_cmd("h3_r4", "192.168.3.1")
    h4.add_default_route_cmd("h4_r8", "192.168.4.1")
    
    # SR MPLS Route
    r1.cmd("ip route add 192.168.2.2/32 encap mpls 16400/16800/16500 via 192.168.12.2")
    r1.cmd("ip route add 192.168.3.2/32 encap mpls 16500/16800/16400 via 192.168.12.2")
    r1.cmd("ip route add 192.168.4.2/32 encap mpls 16400/16500/16800 via 192.168.12.2")

    net.start()

    r1.vtysh_cmd(r1_conf)
    r2.vtysh_cmd(r2_conf)
    r3.vtysh_cmd(r3_conf)
    r4.vtysh_cmd(r4_conf)
    r5.vtysh_cmd(r5_conf)
    r6.vtysh_cmd(r6_conf)
    r7.vtysh_cmd(r7_conf)
    r8.vtysh_cmd(r8_conf)

    r1.tcpdump("r1_r2")
    r4.tcpdump("r4_r3")
    r5.tcpdump("r5_r6")
    r8.tcpdump("r8_r7")

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
