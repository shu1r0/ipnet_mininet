"""
References:
    * http://www.uni-koeln.de/~pbogusze/posts/FRRouting_SR_Segment_Routing_tech_demo.html
    * http://docs.frrouting.org/projects/dev-guide/en/latest/ospf-sr.html
    * https://blog.swineson.me/en/use-linux-as-an-mpls-router/
    * https://tex2e.github.io/rfc-translater/html/rfc8660.html

    * [Segment Routing用 Stateful PCEをフルスクラッチで開発した話](https://enog.jp/wordpress/wp-content/uploads/2022/06/20220610_enog74_mishima.pdf)
    * [nttcom/pola](https://github.com/nttcom/pola)
    * [大規模SR網の運用を効率化するネットワークコントローラの開発](https://speakerdeck.com/watal/da-gui-mo-srwang-falseyun-yong-woxiao-lu-hua-surunetutowakukontororafalsekai-fa-ntt-tech-conference-2022)
    * [FRR PAHT](https://docs.frrouting.org/en/latest/pathd.html)
    * [Virtual Routing and Forwarding](https://docs.kernel.org/networking/vrf.html)
    
"""
from mininet.log import setLogLevel

from ipnet import IPNetwork, MPLSRouter, IPNode, CLIX, add_vrf_cmd


pe1_conf = """\
configure terminal
interface pe1_h1
  ip router isis 1
interface pe1_h2
  ip router isis 1
interface pe1_p1
  ip router isis 1
interface pe1_p2
  ip router isis 1
interface lo
  ip address 10.255.0.1/32
  ip router isis 1

router isis 1
  net 49.0000.0000.0000.0001.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.255.0.1
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.255.0.1/32 index 100
exit

router bgp 65000
  bgp router-id 10.255.0.1
  neighbor 10.255.0.6 remote-as 65000
  neighbor 10.255.0.6 update-source 10.255.0.1
  address-family ipv4 vpn
    neighbor 10.255.0.6 activate
  exit-address-family
exit

router bgp 65000 vrf c1
  address-family ipv4
    redistribute connected
    label vpn export auto
    rd vpn export 65000:10
    rt vpn both 65000:10
    export vpn
    import vpn
  exit-address-family
exit

router bgp 65000 vrf c2
  address-family ipv4
    redistribute connected
    label vpn export auto
    rd vpn export 65000:20
    rt vpn both 65000:20
    export vpn
    import vpn
  exit-address-family
exit

route-map color100 permit 1
  set sr-te color 100
exit

segment-routing
  traffic-eng
    pcep
      pce pce1
        address ip 192.168.255.1
        source-address ip 192.168.255.2
        pce-initiated
        sr-draft07
      exit
      pcc
        peer pce1
      exit
    exit
  exit
exit
"""

pe2_conf = """\
configure terminal
interface pe2_h3
  ip router isis 1
interface pe2_h4
  ip router isis 1
interface pe2_p3
  ip router isis 1
interface pe2_p4
  ip router isis 1
interface lo
  ip address 10.255.0.6/32
  ip router isis 1

router isis 1
  net 49.0000.0000.0000.0004.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.255.0.6
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.255.0.6/32 index 600
exit

router bgp 65000
  bgp router-id 10.255.0.6
  neighbor 10.255.0.1 remote-as 65000
  neighbor 10.255.0.1 update-source 10.255.0.6
  address-family ipv4 vpn
    neighbor 10.255.0.1 activate
  exit-address-family
exit

router bgp 65000 vrf c1
  address-family ipv4 unicast
    redistribute connected
    label vpn export auto
    rd vpn export 65000:10
    rt vpn both 65000:10
    export vpn
    import vpn
  exit-address-family
exit

router bgp 65000 vrf c2
  address-family ipv4 unicast
    redistribute connected
    label vpn export auto
    rd vpn export 65000:20
    rt vpn both 65000:20
    export vpn
    import vpn
  exit-address-family
exit

route-map color100 permit 1
  set sr-te color 100
exit

segment-routing
  traffic-eng
    pcep
      pce pce1
        address ip 192.168.255.1
        source-address ip 192.168.255.3
        pce-initiated
        sr-draft07
      exit
      pcc
        peer pce1
      exit
    exit
  exit
exit
"""

p1_conf = """\
configure terminal
interface p1_pe1
  ip router isis 1
interface p1_p2
  ip router isis 1
interface p1_p3
  ip router isis 1
interface lo
  ip address 10.255.0.2/32
  ip router isis 1

router isis 1
  net 49.0000.0000.0000.0002.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.255.0.2
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.255.0.2/32 index 200
exit
"""

p2_conf = """\
configure terminal
interface p2_pe1
  ip router isis 1
interface p2_p1
  ip router isis 1
interface p2_p4
  ip router isis 1
interface lo
  ip address 10.255.0.3/32
  ip router isis 1

router isis 1
  net 49.0000.0000.0000.0006.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.255.0.3
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.255.0.3/32 index 300
exit
"""

p3_conf = """\
configure terminal
interface p3_pe2
  ip router isis 1
interface p3_p1
  ip router isis 1
interface p3_p4
  ip router isis 1
interface lo
  ip address 10.255.0.4/32
  ip router isis 1

router isis 1
  net 49.0000.0000.0000.0003.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.255.0.4
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.255.0.4/32 index 400
exit
"""

p4_conf = """\
configure terminal
interface p4_pe2
  ip router isis 1
interface p4_p2
  ip router isis 1
interface p4_p3
  ip router isis 1
interface lo
  ip address 10.255.0.5/32
  ip router isis 1

router isis 1
  net 49.0000.0000.0000.0007.00
  is-type level-1
  mpls-te on
  mpls-te router-address 10.255.0.5
  segment-routing on
  segment-routing global-block 16000 23999
  segment-routing node-msd 8
  segment-routing prefix 10.255.0.5/32 index 500
exit
"""


class ProviderEdgeRouter(MPLSRouter):
  pass


class ProviderRouter(MPLSRouter):
  pass

class PathComputationElement(IPNode):
  pass


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    # FRRouting Router
    pe1 = net.addFRR("pe1", cls=ProviderEdgeRouter, enable_daemons=["bgpd", "isisd", "pathd"])
    pe2 = net.addFRR("pe2", cls=ProviderEdgeRouter, enable_daemons=["bgpd", "isisd", "pathd"])
    p1 = net.addFRR("p1", cls=ProviderRouter, enable_daemons=["isisd", "pathd"])
    p2 = net.addFRR("p2", cls=ProviderRouter, enable_daemons=["isisd", "pathd"])
    p3 = net.addFRR("p3", cls=ProviderRouter, enable_daemons=["isisd", "pathd"])
    p4 = net.addFRR("p4", cls=ProviderRouter, enable_daemons=["isisd", "pathd"])

    # host
    h1: IPNode = net.addHost("h1", cls=IPNode)
    h2: IPNode = net.addHost("h2", cls=IPNode)
    h3: IPNode = net.addHost("h3", cls=IPNode)
    h4: IPNode = net.addHost("h4", cls=IPNode)

    # config link
    net.addLink(pe1, h1,
                intfName1="pe1_h1", params1={"ip": "192.168.1.1/24"},
                intfName2="h1_pe1", params2={"ip": "192.168.1.2/24"})
    net.addLink(pe1, h2,
                intfName1="pe1_h2", params1={"ip": "192.168.2.1/24"},
                intfName2="h2_pe1", params2={"ip": "192.168.2.2/24"})
    net.addLink(pe1, p1,
                intfName1="pe1_p1", params1={"ip": "10.0.1.1/24"},
                intfName2="p1_pe1", params2={"ip": "10.0.1.2/24"})
    net.addLink(pe1, p2,
                intfName1="pe1_p2", params1={"ip": "10.0.2.1/24"},
                intfName2="p2_pe1", params2={"ip": "10.0.2.2/24"})
    net.addLink(p1, p2,
                intfName1="p1_p2", params1={"ip": "10.0.12.1/24"},
                intfName2="p2_p1", params2={"ip": "10.0.12.2/24"})
    net.addLink(p1, p3,
                intfName1="p1_p3", params1={"ip": "10.0.13.1/24"},
                intfName2="p3_p1", params2={"ip": "10.0.13.2/24"})
    net.addLink(p2, p4,
                intfName1="p2_p4", params1={"ip": "10.0.24.1/24"},
                intfName2="p4_p2", params2={"ip": "10.0.24.2/24"})
    net.addLink(p3, pe2,
                intfName1="p3_pe2", params1={"ip": "10.0.3.1/24"},
                intfName2="pe2_p3", params2={"ip": "10.0.3.2/24"})
    net.addLink(p3, p4,
                intfName1="p3_p4", params1={"ip": "10.0.34.1/24"},
                intfName2="p4_p3", params2={"ip": "10.0.34.2/24"})
    net.addLink(p4, pe2,
                intfName1="p4_pe2", params1={"ip": "10.0.4.1/24"},
                intfName2="pe2_p4", params2={"ip": "10.0.4.2/24"})
    net.addLink(pe2, h3,
                intfName1="pe2_h3", params1={"ip": "192.168.3.1/24"},
                intfName2="h3_pe2", params2={"ip": "192.168.3.2/24"})
    net.addLink(pe2, h4,
                intfName1="pe2_h4", params1={"ip": "192.168.4.1/24"},
                intfName2="h4_pe2", params2={"ip": "192.168.4.2/24"})
    
    h1.add_default_route_cmd("h1_pe1", "192.168.1.1")
    h2.add_default_route_cmd("h2_pe1", "192.168.2.1")
    h3.add_default_route_cmd("h3_pe2", "192.168.3.1")
    h4.add_default_route_cmd("h4_pe2", "192.168.4.1")
    
    # VRF config
    add_vrf_cmd(pe1, vrf_name="c1", table_id=10, enslaved_intf="pe1_h1")
    add_vrf_cmd(pe1, vrf_name="c2", table_id=20, enslaved_intf="pe1_h2")
    add_vrf_cmd(pe2, vrf_name="c1", table_id=10, enslaved_intf="pe2_h3")
    add_vrf_cmd(pe2, vrf_name="c2", table_id=20, enslaved_intf="pe2_h4")
    
    # MGMT 
    pce = net.add_mgmt_l2network("pce", controller_cls=PathComputationElement, inNamespace=False, cls=ProviderEdgeRouter, ip_base="192.168.255.{node}/24")

    net.start()

    print(pe1.vtysh_cmd(pe1_conf))
    print(pe2.vtysh_cmd(pe2_conf))
    print(p1.vtysh_cmd(p1_conf))
    print(p2.vtysh_cmd(p2_conf))
    print(p3.vtysh_cmd(p3_conf))
    print(p4.vtysh_cmd(p4_conf))

    # pe1.tcpdump("pe1_p1")
    # pe1.tcpdump("pe1_p2")
    # pe1.tcpdump("pe1_s255")
    # pe2.tcpdump("pe2_p3")
    # pe2.tcpdump("pe2_p4")
    # pe2.tcpdump("pe2_s255")

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()

