from mininet.log import setLogLevel

from ipnet import IPNetwork, FRR, CLIX, IPNode, add_vrf_cmd


spine_conf = """\
enable
configure terminal

interface {s_name}_l1
  ipv6 router isis 1
interface {s_name}_l2
  ipv6 router isis 1
interface {s_name}_l3
  ipv6 router isis 1
interface {s_name}_l4
  ipv6 router isis 1
interface lo
  ipv6 address {srv6_locator_pre}
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.000{id}.00
  is-type level-1
exit

segment-routing
  srv6
    locators
      locator default
        prefix {srv6_locator_pre}
      exit
    exit
  exit
exit

router bgp {as_number}
  bgp router-id {router_id}
  no bgp default ipv4-unicast
  no bgp default ipv6-unicast
  no bgp ebgp-requires-policy
  bgp bestpath as-path multipath-relax
  neighbor CLOS peer-group
  neighbor CLOS remote-as external
  neighbor CLOS bfd
  neighbor CLOS capability extended-nexthop
  neighbor {s_name}_l1 interface peer-group CLOS
  neighbor {s_name}_l2 interface peer-group CLOS
  neighbor {s_name}_l3 interface peer-group CLOS
  neighbor {s_name}_l4 interface peer-group CLOS

  segment-routing srv6
    locator default
  exit
  
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
  
  address-family ipv4 unicast
    neighbor CLOS activate
  exit-address-family
  
  address-family ipv6 vpn
    neighbor CLOS activate
  exit-address-family
exit
"""


leaf_conf = """\
enable
configure terminal

interface {l_name}_s1
  ipv6 router isis 1
interface {l_name}_s2
  ipv6 router isis 1
interface {l_name}_s3
  ipv6 router isis 1
interface {l_name}_s4
  ipv6 router isis 1
interface lo
  ipv6 address {srv6_locator_pre}
  ipv6 router isis 1

router isis 1
  net 49.0000.0000.0000.00{id}.00
  is-type level-1
exit

segment-routing
  srv6
    locators
      locator default
        prefix {srv6_locator_pre}
      exit
    exit
  exit
exit

router bgp {as_number}
  bgp router-id {router_id}
  no bgp default ipv4-unicast
  no bgp default ipv6-unicast
  no bgp ebgp-requires-policy
  bgp bestpath as-path multipath-relax
  neighbor CLOS peer-group
  neighbor CLOS remote-as external
  neighbor CLOS bfd
  neighbor CLOS capability extended-nexthop
  neighbor {l_name}_s1 interface peer-group CLOS
  neighbor {l_name}_s2 interface peer-group CLOS
  neighbor {l_name}_s3 interface peer-group CLOS
  neighbor {l_name}_s4 interface peer-group CLOS

  segment-routing srv6
    locator default
  exit
  
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
  
  address-family ipv4 unicast
    neighbor CLOS activate
  exit-address-family
  
  address-family ipv6 vpn
    neighbor CLOS activate
  exit-address-family
exit

router bgp {as_number} vrf group1
  bgp router-id {router_id}
  address-family ipv6
    sid vpn export auto
    redistribute connected
    rd vpn export {as_number}:10
    rt vpn both 65101:10 65102:10 65103:10 65104:10
    export vpn
    import vpn
  exit-address-family
exit

router bgp {as_number} vrf group2
  bgp router-id {router_id}
  address-family ipv6
    sid vpn export auto
    redistribute connected
    rd vpn export {as_number}:20
    rt vpn both 65101:20 65102:20 65103:20 65104:20
    export vpn
    import vpn
  exit-address-family
exit
"""



class Leaf(FRR):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.srv6_locator = kwargs.get("srv6_locator", "")


class Spine(FRR):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.srv6_locator = kwargs.get("srv6_locator", "")


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    # Spine
    s1 = net.addFRR("s1", cls=Spine, enable_daemons=["bgpd", "isisd", "pathd"])
    s2 = net.addFRR("s2", cls=Spine, enable_daemons=["bgpd", "isisd", "pathd"])
    s3 = net.addFRR("s3", cls=Spine, enable_daemons=["bgpd", "isisd", "pathd"])
    s4 = net.addFRR("s4", cls=Spine, enable_daemons=["bgpd", "isisd", "pathd"])
    # Leaf
    l1 = net.addFRR("l1", cls=Leaf, enable_daemons=["bgpd", "isisd", "pathd"])
    l2 = net.addFRR("l2", cls=Leaf, enable_daemons=["bgpd", "isisd", "pathd"])
    l3 = net.addFRR("l3", cls=Leaf, enable_daemons=["bgpd", "isisd", "pathd"])
    l4 = net.addFRR("l4", cls=Leaf, enable_daemons=["bgpd", "isisd", "pathd"])
    # Host
    h1 = net.addHost("h1", cls=IPNode)
    h2 = net.addHost("h2", cls=IPNode)
    h3 = net.addHost("h3", cls=IPNode)
    h4 = net.addHost("h4", cls=IPNode)
    h5 = net.addHost("h5", cls=IPNode)
    h6 = net.addHost("h6", cls=IPNode)
    h7 = net.addHost("h7", cls=IPNode)
    h8 = net.addHost("h8", cls=IPNode)
    
    # set SRv6 SID
    sid_format = "fdbb:{node}::{func}:0:{args}/64"
    format_dict = {"node": -1, "func": 1, "args": 0}
    for i, n in enumerate(net.get_nodes_by_cls(Spine), start=1):
        format_dict["node"] = "a" + str(i)
        n.srv6_locator = sid_format.format(**format_dict)
    for i, n in enumerate(net.get_nodes_by_cls(Leaf), start=1):
        format_dict["node"] = "b" + str(i)
        n.srv6_locator = sid_format.format(**format_dict)
    
    def set_link(n1, n2, **params):
        """set link between node1 and node2"""
        intf1 = str(n1)+"_"+str(n2)
        intf2 = str(n2)+"_"+str(n1)
        net.addLink(n1, n2, intfName1=intf1, intfName2=intf2, **params)
    
    def set_link_spine():
        """set link spine to leaf"""
        spines = [n for n in net.nameToNode.values() if isinstance(n, Spine)]
        leafs = [n for n in net.nameToNode.values() if isinstance(n, Leaf)]
        for s in spines:
            for l in leafs:
                set_link(s, l)
    
    def set_link_hosts(r, h1, block):
        def set_link_host(r, n, block):
            ipv6_1 = "fd00:{}::1/64".format(block)
            ipv6_2 = "fd00:{}::2/64".format(block)
            ipv4_1 = "192.168.{}.1/24".format(block)
            ipv4_2 = "192.168.{}.2/24".format(block)
            intf1 = str(r)+"_"+str(n)
            intf2 = str(n)+"_"+str(r)
            net.addLink(r, n, 
                        intfName1=intf1, params1={"ip": ipv4_1},
                        intfName2=intf2, params2={"ip": ipv4_2})
            r.set_ipv6_cmd(ipv6_1, intf1)
            n.set_ipv6_cmd(ipv6_2, intf2)
            
            n.cmd("ip route add default dev {} via {}".format(intf2, ipv4_1.split("/")[0]))
            n.cmd("ip -6 route add default dev {} via {}".format(intf2, ipv6_1.split("/")[0]))
            
        set_link_host(r, h1, block)

    # Setup Spine link
    set_link_spine()

    # Set hosts
    set_link_hosts(l1, h1, 1)
    set_link_hosts(l1, h2, 2)
    set_link_hosts(l2, h3, 3)
    set_link_hosts(l2, h4, 4)
    set_link_hosts(l3, h5, 5)
    set_link_hosts(l3, h6, 6)
    set_link_hosts(l4, h7, 7)
    set_link_hosts(l4, h8, 8)
    
    # VRF config
    add_vrf_cmd(l1, vrf_name="group1", table_id=10, enslaved_intf="l1_h1", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l2, vrf_name="group1", table_id=10, enslaved_intf="l2_h3", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l3, vrf_name="group1", table_id=10, enslaved_intf="l3_h5", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l4, vrf_name="group1", table_id=10, enslaved_intf="l4_h7", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l1, vrf_name="group2", table_id=20, enslaved_intf="l1_h2", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l2, vrf_name="group2", table_id=20, enslaved_intf="l2_h4", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l3, vrf_name="group2", table_id=20, enslaved_intf="l3_h6", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l4, vrf_name="group2", table_id=20, enslaved_intf="l4_h8", keep_addr_on_down=1, verbose=True)


    # Start Network
    net.start()

    # FRRouting setup
    def set_frr_spine(id, ss, router_id, as_number, srv6_locator_pre):
        r = ss.vtysh_cmd(spine_conf.format(
            id=id,
            as_number=as_number,
            router_id=router_id,
            s_name=str(ss),
            srv6_locator_pre=srv6_locator_pre,
        ))
        print(r)
        
    def set_frr_leaf(id, s, router_id, as_number, srv6_locator_pre, h_name1, h_name2):
        r = s.vtysh_cmd(leaf_conf.format(
            id=id,
            as_number=as_number,
            router_id=router_id,
            l_name=str(s),
            srv6_locator_pre=srv6_locator_pre,
            h_name1=h_name1,
            h_name2=h_name2,
        ))
        print(r)
    
    # Set FRR config
    set_frr_spine(1, s1, "1.1.1.1", 65000, s1.srv6_locator)
    set_frr_spine(2, s2, "1.1.1.2", 65000, s2.srv6_locator)
    set_frr_spine(3, s3, "1.1.1.3", 65000, s3.srv6_locator)
    set_frr_spine(4, s4, "1.1.1.4", 65000, s4.srv6_locator)
    
    set_frr_leaf(11, l1, "2.2.2.1", 65101, l1.srv6_locator, "h1", "h2")
    set_frr_leaf(12, l2, "2.2.2.2", 65102, l2.srv6_locator, "h3", "h4")
    set_frr_leaf(13, l3, "2.2.2.3", 65103, l3.srv6_locator, "h5", "h6")
    set_frr_leaf(14, l4, "2.2.2.4", 65104, l4.srv6_locator, "h7", "h8")

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
