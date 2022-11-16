"""
References:
    * http://www.uni-koeln.de/~pbogusze/posts/FRRouting_SR_Segment_Routing_tech_demo.html
    * http://docs.frrouting.org/projects/dev-guide/en/latest/ospf-sr.html
    * https://blog.swineson.me/en/use-linux-as-an-mpls-router/
    * https://tex2e.github.io/rfc-translater/html/rfc8660.html

    * [Segment Routing用 Stateful PCEをフルスクラッチで開発した話](https://enog.jp/wordpress/wp-content/uploads/2022/06/20220610_enog74_mishima.pdf)
    * [nttcom/pola](https://github.com/nttcom/pola)
    * [大規模SR網の運用を効率化するネットワークコントローラの開発](https://speakerdeck.com/watal/da-gui-mo-srwang-falseyun-yong-woxiao-lu-hua-surunetutowakukontororafalsekai-fa-ntt-tech-conference-2022)
    * [FRR PATH](https://docs.frrouting.org/en/latest/pathd.html)
    * [Virtual Routing and Forwarding](https://docs.kernel.org/networking/vrf.html)
    
"""
from mininet.log import setLogLevel

from ipnet import IPNetwork, FRR, IPNode, CLIX, add_vrf_cmd


pe1_conf = """\
configure terminal
interface pe1_h1
  ipv6 router isis 1
interface pe1_h2
  ipv6 router isis 1
interface pe1_p1
  ipv6 router isis 1
interface pe1_p2
  ipv6 router isis 1
interface lo
  ipv6 address 2001:db8:1::/64
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.0001.00
  is-type level-1
exit

segment-routing
  srv6
    locators
      locator default
        prefix 2001:db8:1::/64
      exit
    exit
  exit
exit

router bgp 65000
  bgp router-id 10.255.0.1
  no bgp default ipv6-unicast
  neighbor 2001:db8:6:: remote-as 65000
  neighbor 2001:db8:6:: update-source 2001:db8:1::
  segment-routing srv6
    locator default
  exit
  address-family ipv6 vpn
    neighbor 2001:db8:6:: activate
  exit-address-family
exit

router bgp 65000 vrf c1
  bgp router-id 10.255.0.1
  address-family ipv6
    sid vpn export auto
    redistribute connected
    rd vpn export 65000:10
    rt vpn both 65000:10
    export vpn
    import vpn
  exit-address-family
exit

router bgp 65000 vrf c2
  bgp router-id 10.255.0.1
  address-family ipv6
    sid vpn export auto
    redistribute connected
    rd vpn export 65000:20
    rt vpn both 65000:20
    export vpn
    import vpn
  exit-address-family
exit
"""

pe2_conf = """\
configure terminal
interface pe2_h3
  ipv6 router isis 1
interface pe2_h4
  ipv6 router isis 1
interface pe2_p3
  ipv6 router isis 1
interface pe2_p4
  ipv6 router isis 1
interface lo
  ipv6 address 2001:db8:6::/64
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.0006.00
  is-type level-1
exit

segment-routing
  srv6
    locators
      locator default
        prefix 2001:db8:6::/64
      exit
    exit
  exit
exit

router bgp 65000
  bgp router-id 10.255.0.6
  no bgp default ipv6-unicast
  neighbor 2001:db8:1:: remote-as 65000
  neighbor 2001:db8:1:: update-source 2001:db8:6::
  segment-routing srv6
    locator default
  exit
  address-family ipv6 vpn
    neighbor 2001:db8:1:: activate
  exit-address-family
exit

router bgp 65000 vrf c1
  bgp router-id 10.255.0.6
  address-family ipv6 unicast
    sid vpn export auto
    redistribute connected
    rd vpn export 65000:10
    rt vpn both 65000:10
    export vpn
    import vpn
  exit-address-family
exit

router bgp 65000 vrf c2
  bgp router-id 10.255.0.6
  address-family ipv6 unicast
    sid vpn export auto
    redistribute connected
    rd vpn export 65000:20
    rt vpn both 65000:20
    export vpn
    import vpn
  exit-address-family
exit
"""

p1_conf = """\
configure terminal
interface p1_pe1
  ipv6 router isis 1
interface p1_p2
  ipv6 router isis 1
interface p1_p3
  ipv6 router isis 1
interface lo
  ipv6 address 2001:db8:2::/64
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.0002.00
  is-type level-1
exit
"""

p2_conf = """\
configure terminal
interface p2_pe1
  ipv6 router isis 1
interface p2_p1
  ipv6 router isis 1
interface p2_p4
  ipv6 router isis 1
interface lo
  ipv6 address 2001:db8:3::/64
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.0003.00
  is-type level-1
exit
"""

p3_conf = """\
configure terminal
interface p3_pe2
  ipv6 router isis 1
interface p3_p1
  ipv6 router isis 1
interface p3_p4
  ipv6 router isis 1
interface lo
  ipv6 address 2001:db8:4::/64
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.0004.00
  is-type level-1
exit
"""

p4_conf = """\
configure terminal
interface p4_pe2
  ipv6 router isis 1
interface p4_p2
  ipv6 router isis 1
interface p4_p3
  ipv6 router isis 1
interface lo
  ipv6 address 2001:db8:5::/64
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.0005.00
  is-type level-1
exit
"""


class ProviderEdgeRouter(FRR):
  pass


class ProviderRouter(FRR):
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
    net.addLink(pe1, h1, intfName1="pe1_h1", intfName2="h1_pe1")
    net.addLink(pe1, h2, intfName1="pe1_h2", intfName2="h2_pe1")
    net.addLink(pe1, p1, intfName1="pe1_p1", intfName2="p1_pe1")
    net.addLink(pe1, p2, intfName1="pe1_p2", intfName2="p2_pe1")
    net.addLink(p1, p2, intfName1="p1_p2", intfName2="p2_p1")
    net.addLink(p1, p3, intfName1="p1_p3", intfName2="p3_p1")
    net.addLink(p2, p4, intfName1="p2_p4", intfName2="p4_p2")
    net.addLink(p3, pe2, intfName1="p3_pe2", intfName2="pe2_p3")
    net.addLink(p3, p4, intfName1="p3_p4", intfName2="p4_p3")
    net.addLink(p4, pe2, intfName1="p4_pe2", intfName2="pe2_p4")
    net.addLink(pe2, h3, intfName1="pe2_h3", intfName2="h3_pe2")
    net.addLink(pe2, h4, intfName1="pe2_h4", intfName2="h4_pe2")
    
    # addresses setting
    h1.set_ipv6_cmd("fd00:1::2/64", "h1_pe1")
    pe1.set_ipv6_cmd("fd00:1::1/64", "pe1_h1")
    h1.add_v6_default_route_cmd("h1_pe1", "fd00:1::1")
    h2.set_ipv6_cmd("fd00:2::2/64", "h2_pe1")
    pe1.set_ipv6_cmd("fd00:2::1/64", "pe1_h2")
    h2.add_v6_default_route_cmd("h2_pe1", "fd00:2::1")
    h3.set_ipv6_cmd("fd00:3::2/64", "h3_pe2")
    pe2.set_ipv6_cmd("fd00:3::1/64", "pe2_h3")
    h3.add_v6_default_route_cmd("h3_pe2", "fd00:3::1")
    h4.set_ipv6_cmd("fd00:4::2/64", "h4_pe2")
    pe2.set_ipv6_cmd("fd00:4::1/64", "pe2_h4")
    h4.add_v6_default_route_cmd("h4_pe2", "fd00:4::1")
    
    # VRF config
    add_vrf_cmd(pe1, vrf_name="c1", table_id=10, enslaved_intf="pe1_h1", keep_addr_on_down=1)
    add_vrf_cmd(pe1, vrf_name="c2", table_id=20, enslaved_intf="pe1_h2", keep_addr_on_down=1)
    add_vrf_cmd(pe2, vrf_name="c1", table_id=10, enslaved_intf="pe2_h3", keep_addr_on_down=1)
    add_vrf_cmd(pe2, vrf_name="c2", table_id=20, enslaved_intf="pe2_h4", keep_addr_on_down=1)
    
    # MGMT 
    # mgmt = net.add_mgmt_l2network("mgmt", controller_cls=PathComputationElement, inNamespace=False, ip_base="192.168.255.{node}/24")

    net.start()

    pe1.vtysh_cmd(pe1_conf)
    pe2.vtysh_cmd(pe2_conf)
    p1.vtysh_cmd(p1_conf)
    p2.vtysh_cmd(p2_conf)
    p3.vtysh_cmd(p3_conf)
    p4.vtysh_cmd(p4_conf)

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

