"""
ref:
    * http://www.uni-koeln.de/~pbogusze/posts/FRRouting_SR_Segment_Routing_tech_demo.html
    * http://docs.frrouting.org/projects/dev-guide/en/latest/ospf-sr.html
    * https://blog.swineson.me/en/use-linux-as-an-mpls-router/
    * https://tex2e.github.io/rfc-translater/html/rfc8660.html
"""

from mininet.log import setLogLevel

from ipnet import IPNetwork, FRR, CLIX, enable_mpls, disable_rp


r1_conf = """\
configure terminal

interface r1_h1
  ip ospf area 0
interface r1_h3
  ip ospf area 0
interface r1_r2
  ip ospf area 0
interface r1_r3
  ip ospf area 0
interface lo
  ip address 10.0.0.1/32
  ip ospf area 0
  
router ospf
  ospf router-id 10.0.0.1
  # router-info area 0.0.0.0
  capability opaque
  mpls-te on
  mpls-te router-address 10.0.0.1
  segment-routing on
  segment-routing global-block 19000 21999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.1/32 index 100
exit
"""

r2_conf = """\
configure terminal

interface r2_r1
  ip ospf area 0
interface r2_r3
  ip ospf area 0
interface r2_r4
  ip ospf area 0
interface lo
  ip address 10.0.0.2/32
  ip ospf area 0
  
router ospf
  ospf router-id 10.0.0.2
  # router-info area 0.0.0.0
  capability opaque
  mpls-te on
  mpls-te router-address 10.0.0.2
  segment-routing on
  segment-routing global-block 19000 21999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.2/32 index 200
exit
"""

r3_conf = """\
configure terminal

interface r3_r1
  ip ospf area 0
interface r3_r2
  ip ospf area 0
interface r3_r5
  ip ospf area 0
interface lo
  ip address 10.0.0.3/32
  ip ospf area 0
  
router ospf
  ospf router-id 10.0.0.3
  # router-info area 0.0.0.0
  capability opaque
  mpls-te on
  mpls-te router-address 10.0.0.3
  segment-routing on
  segment-routing global-block 19000 21999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.3/32 index 300
exit
"""

r4_conf = """\
configure terminal

interface r4_r2
  ip ospf area 0
interface r4_r5
  ip ospf area 0
interface r4_r6
  ip ospf area 0
interface lo
  ip address 10.0.0.4/32
  ip ospf area 0

router ospf
  ospf router-id 10.0.0.4
  # router-info area 0.0.0.0
  capability opaque
  mpls-te on
  mpls-te router-address 10.0.0.4
  segment-routing on
  segment-routing global-block 19000 21999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.4/32 index 400
exit
"""

r5_conf = """\
configure terminal

interface r5_r3
  ip ospf area 0
interface r5_r4
  ip ospf area 0
interface r5_r6
  ip ospf area 0
interface lo
  ip address 10.0.0.5/32
  ip ospf area 0

router ospf
  ospf router-id 10.0.0.5
  # router-info area 0.0.0.0
  capability opaque
  mpls-te on
  mpls-te router-address 10.0.0.5
  segment-routing on
  segment-routing global-block 19000 21999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.5/32 index 500
exit
"""


r6_conf = """\
configure terminal

interface r6_r4
  ip ospf area 0
interface r6_r5
  ip ospf area 0
interface r6_h3
  ip ospf area 0
interface r6_h4
  ip ospf area 0
interface lo
  ip address 10.0.0.6/32
  ip ospf area 0

router ospf
  ospf router-id 10.0.0.6
  # router-info area 0.0.0.0
  capability opaque
  mpls-te on
  mpls-te router-address 10.0.0.6
  segment-routing on
  segment-routing global-block 19000 21999
  segment-routing node-msd 8
  segment-routing prefix 10.0.0.6/32 index 600
exit
"""

class MPLSNode(FRR):

    def config(self, **params):
        super().config(**params)
        enable_mpls(self)
        disable_rp(self)



def main():
    setLogLevel("info")
    net = IPNetwork()

    # add frr node
    r1 = net.addFRR("r1", cls=MPLSNode, enable_daemons=["ospfd"])
    r2 = net.addFRR("r2", cls=MPLSNode, enable_daemons=["ospfd"])
    r3 = net.addFRR("r3", cls=MPLSNode, enable_daemons=["ospfd"])
    r4 = net.addFRR("r4", cls=MPLSNode, enable_daemons=["ospfd"])
    r5 = net.addFRR("r5", cls=MPLSNode, enable_daemons=["ospfd"])
    r6 = net.addFRR("r6", cls=MPLSNode, enable_daemons=["ospfd"])

    # host
    h1 = net.addHost("h1", ip=None)
    h2 = net.addHost("h2", ip=None)
    h3 = net.addHost("h3", ip=None)
    h4 = net.addHost("h4", ip=None)

    # config link
    net.addLink(r1, h1,
                intfName1="r1_h1", params1={"ip": "192.168.1.1/24"},
                intfName2="h1_r1", params2={"ip": "192.168.1.2/24"})
    h1.cmd("ip route add default dev h1_r1 via 192.168.1.1")
    
    net.addLink(r1, h2,
                intfName1="r1_h2", params1={"ip": "192.168.2.1/24"},
                intfName2="h2_r1", params2={"ip": "192.168.2.2/24"})
    h2.cmd("ip route add default dev h2_r1 via 192.168.2.1")
    
    net.addLink(r6, h3,
                intfName1="r6_h3", params1={"ip": "192.168.3.1/24"},
                intfName2="h3_r6", params2={"ip": "192.168.3.2/24"})
    h3.cmd("ip route add default dev h3_r6 via 192.168.3.1")
    
    net.addLink(r6, h4,
                intfName1="r6_h4", params1={"ip": "192.168.4.1/24"},
                intfName2="h4_r6", params2={"ip": "192.168.4.2/24"})
    h4.cmd("ip route add default dev h4_r6 via 192.168.4.1")

    net.addLink(r1, r2, 
                intfName1="r1_r2", params1={"ip": "10.0.12.1/24"}, 
                intfName2="r2_r1", params2={"ip": "10.0.12.2/24"})
    net.addLink(r1, r3, 
                intfName1="r1_r3", params1={"ip": "10.0.13.1/24"}, 
                intfName2="r3_r1", params2={"ip": "10.0.13.2/24"})

    net.addLink(r2, r4, 
                intfName1="r2_r4", params1={"ip": "10.0.24.1/24"}, 
                intfName2="r4_r2", params2={"ip": "10.0.24.2/24"})
    net.addLink(r2, r3, 
                intfName1="r2_r3", params1={"ip": "10.0.23.1/24"}, 
                intfName2="r3_r2", params2={"ip": "10.0.23.2/24"})

    net.addLink(r3, r5, 
                intfName1="r3_r5", params1={"ip": "10.0.35.1/24"}, 
                intfName2="r5_r3", params2={"ip": "10.0.35.2/24"})

    net.addLink(r4, r6, 
                intfName1="r4_r6", params1={"ip": "10.0.46.1/24"}, 
                intfName2="r6_r4", params2={"ip": "10.0.46.2/24"})
    net.addLink(r4, r5, 
                intfName1="r4_r5", params1={"ip": "10.0.45.1/24"}, 
                intfName2="r5_r4", params2={"ip": "10.0.45.2/24"})

    net.addLink(r5, r6, 
                intfName1="r5_r6", params1={"ip": "10.0.56.1/24"}, 
                intfName2="r6_r5", params2={"ip": "10.0.56.2/24"})
    
    # add route
    
    net.start()
    
    r1.vtysh_cmd(r1_conf)
    r2.vtysh_cmd(r2_conf)
    r3.vtysh_cmd(r3_conf)
    r4.vtysh_cmd(r4_conf)
    r5.vtysh_cmd(r5_conf)
    r6.vtysh_cmd(r6_conf)

    CLIX(net)
    
    net.stop()


if __name__ == "__main__":
    main()