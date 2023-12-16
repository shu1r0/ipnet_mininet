from mininet.log import setLogLevel

from ipnet import IPNetwork, FRR, CLIX, IPNode, add_vrf_cmd


super_spine_conf = """\
enable
configure terminal

interface lo
  ipv6 address {srv6_locator_pre}

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
  neighbor CLOS peer-group
  neighbor CLOS remote-as external
  neighbor CLOS capability extended-nexthop
  neighbor CLOS bfd
  neighbor {ss_name}_s1 interface peer-group CLOS
  neighbor {ss_name}_s2 interface peer-group CLOS
  neighbor {ss_name}_s3 interface peer-group CLOS
  neighbor {ss_name}_s4 interface peer-group CLOS
  neighbor {ss_name}_s5 interface peer-group CLOS
  neighbor {ss_name}_s6 interface peer-group CLOS

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
    rt vpn both 65103:10 65104:10 65203:10 65204:10 65303:10 65304:10 65403:10 65404:10 65101:10 65102:10 65201:10 65202:10 65301:10 65302:10 65401:10 65402:10
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
    rt vpn both 65103:20 65104:20 65203:20 65204:20 65303:20 65304:20 65403:20 65404:20 65101:20 65102:20 65201:20 65202:20 65301:20 65302:20 65401:20 65402:20
    export vpn
    import vpn
  exit-address-family
exit
"""

spine_conf = """\
enable
configure terminal

interface lo
  ipv6 address {srv6_locator_pre}

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
  neighbor {s_name}_ss1 interface peer-group CLOS
  neighbor {s_name}_ss2 interface peer-group CLOS
  neighbor {s_name}_ss3 interface peer-group CLOS
  neighbor {s_name}_ss4 interface peer-group CLOS
  neighbor {s_name}_ss5 interface peer-group CLOS
  neighbor {s_name}_ss6 interface peer-group CLOS
  neighbor {s_name}_{l_name1} interface peer-group CLOS
  neighbor {s_name}_{l_name2} interface peer-group CLOS

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
    rt vpn both 65103:10 65104:10 65203:10 65204:10 65303:10 65304:10 65403:10 65404:10 65101:10 65102:10 65201:10 65202:10 65301:10 65302:10 65401:10 65402:10
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
    rt vpn both 65103:20 65104:20 65203:20 65204:20 65303:20 65304:20 65403:20 65404:20 65101:20 65102:20 65201:20 65202:20 65301:20 65302:20 65401:20 65402:20
    export vpn
    import vpn
  exit-address-family
exit
"""

leaf_conf = """\
enable
configure terminal

interface lo
  ipv6 address {srv6_locator_pre}

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
  neighbor {l_name}_{s_name1} interface peer-group CLOS
  neighbor {l_name}_{s_name2} interface peer-group CLOS
  neighbor {l_name}_{s_name1} capability extended-nexthop
  neighbor {l_name}_{s_name2} capability extended-nexthop

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
    rt vpn both 65103:10 65104:10 65203:10 65204:10 65303:10 65304:10 65403:10 65404:10 65101:10 65102:10 65201:10 65202:10 65301:10 65302:10 65401:10 65402:10
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
    rt vpn both 65103:20 65104:20 65203:20 65204:20 65303:20 65304:20 65403:20 65404:20 65101:20 65102:20 65201:20 65202:20 65301:20 65302:20 65401:20 65402:20
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


class SuperSpine(FRR):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.srv6_locator = kwargs.get("srv6_locator", "")


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()
    
    # Super Spine
    ss1 = net.addFRR("ss1", cls=SuperSpine, enable_daemons=["bgpd", "pathd"])
    ss2 = net.addFRR("ss2", cls=SuperSpine, enable_daemons=["bgpd", "pathd"])
    ss3 = net.addFRR("ss3", cls=SuperSpine, enable_daemons=["bgpd", "pathd"])
    ss4 = net.addFRR("ss4", cls=SuperSpine, enable_daemons=["bgpd", "pathd"])
    ss5 = net.addFRR("ss5", cls=SuperSpine, enable_daemons=["bgpd", "pathd"])
    ss6 = net.addFRR("ss6", cls=SuperSpine, enable_daemons=["bgpd", "pathd"])
    
    # Spine
    s1 = net.addFRR("s1", cls=Spine, enable_daemons=["bgpd", "pathd"])
    s2 = net.addFRR("s2", cls=Spine, enable_daemons=["bgpd", "pathd"])
    s3 = net.addFRR("s3", cls=Spine, enable_daemons=["bgpd", "pathd"])
    s4 = net.addFRR("s4", cls=Spine, enable_daemons=["bgpd", "pathd"])
    s5 = net.addFRR("s5", cls=Spine, enable_daemons=["bgpd", "pathd"])
    s6 = net.addFRR("s6", cls=Spine, enable_daemons=["bgpd", "pathd"])
    
    # Leaf
    l1 = net.addFRR("l1", cls=Leaf, enable_daemons=["bgpd", "pathd"])
    l2 = net.addFRR("l2", cls=Leaf, enable_daemons=["bgpd", "pathd"])
    l3 = net.addFRR("l3", cls=Leaf, enable_daemons=["bgpd", "pathd"])
    l4 = net.addFRR("l4", cls=Leaf, enable_daemons=["bgpd", "pathd"])
    l5 = net.addFRR("l5", cls=Leaf, enable_daemons=["bgpd", "pathd"])
    l6 = net.addFRR("l6", cls=Leaf, enable_daemons=["bgpd", "pathd"])
    

    # Host
    h1 = net.addHost("h1", cls=IPNode)
    h2 = net.addHost("h2", cls=IPNode)
    h3 = net.addHost("h3", cls=IPNode)
    h4 = net.addHost("h4", cls=IPNode)
    h5 = net.addHost("h5", cls=IPNode)
    h6 = net.addHost("h6", cls=IPNode)
    
    # set SRv6 SID
    sid_format = "fdbb:{node}::{func}:0:0:{args}/64"
    format_dict = {"node": -1, "func": 1, "args": 0}
    ## fcbb:a<n>::
    for i, n in enumerate(net.get_nodes_by_cls(SuperSpine), start=1):
        format_dict["node"] = "a" + str(i)
        n.srv6_locator = sid_format.format(**format_dict)
    ## fcbb:b<n>::
    for i, n in enumerate(net.get_nodes_by_cls(Spine), start=1):
        format_dict["node"] = "b" + str(i)
        n.srv6_locator = sid_format.format(**format_dict)
    ## fcbb:c<n>::
    for i, n in enumerate(net.get_nodes_by_cls(Leaf), start=1):
        format_dict["node"] = "c" + str(i)
        n.srv6_locator = sid_format.format(**format_dict)
    
    def set_link(n1, n2):
        """set link between node1 and node2"""
        intf1 = str(n1)+"_"+str(n2)
        intf2 = str(n2)+"_"+str(n1)
        net.addLink(n1, n2, intfName1=intf1, intfName2=intf2)
    
    def set_link_super_spine():
        sspines = [n for n in net.nameToNode.values() if isinstance(n, SuperSpine)]
        spines = [n for n in net.nameToNode.values() if isinstance(n, Spine)]
        for ss in sspines:
            for s in spines:
                set_link(ss, s)
    
    def set_link_pod(s1, s2, l1, l2):
        for s in [s1, s2]:
            for l in [l1, l2]:
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

    # setup
    set_link_super_spine()
    set_link_pod(s1, s2, l1, l2)
    set_link_pod(s3, s4, l3, l4)
    set_link_pod(s5, s6, l5, l6)
    set_link_hosts(l1, h1, 1)
    set_link_hosts(l2, h2, 2)
    set_link_hosts(l3, h3, 3)
    set_link_hosts(l4, h4, 4)
    set_link_hosts(l5, h5, 5)
    set_link_hosts(l6, h6, 6)

    # VRF config
    add_vrf_cmd(l1, vrf_name="group1", table_id=10, enslaved_intf="l1_h1", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l2, vrf_name="group1", table_id=10, enslaved_intf="l2_h2", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l3, vrf_name="group1", table_id=10, enslaved_intf="l3_h3", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l4, vrf_name="group1", table_id=10, enslaved_intf="l4_h4", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l5, vrf_name="group1", table_id=10, enslaved_intf="l5_h5", keep_addr_on_down=1, verbose=True)
    add_vrf_cmd(l6, vrf_name="group1", table_id=10, enslaved_intf="l6_h6", keep_addr_on_down=1, verbose=True)
    
    # Start Network
    net.start()
    
    # FRRouting setup
    def set_frr_superspine(ss, router_id):
        ss.vtysh_cmd(super_spine_conf.format(
            as_number=65000,
            router_id=router_id,
            ss_name=str(ss),
            srv6_locator_pre=ss.srv6_locator,
        ), verbose=True)
        
    def set_frr_spine(s, router_id, as_number, l1, l2):
        s.vtysh_cmd(spine_conf.format(
            as_number=as_number,
            router_id=router_id,
            s_name=str(s),
            l_name1=str(l1),
            l_name2=str(l2),
            srv6_locator_pre=s.srv6_locator,
        ), verbose=True)
        
    def set_frr_leaf(l, router_id, as_number, s1, s2):
        l.vtysh_cmd(leaf_conf.format(
            as_number=as_number,
            router_id=router_id,
            l_name=str(l),
            s_name1=str(s1),
            s_name2=str(s2),
            srv6_locator_pre=l.srv6_locator,
        ), verbose=True)
    
    set_frr_superspine(ss1, "1.1.1.1")
    set_frr_superspine(ss2, "1.1.1.2")
    set_frr_superspine(ss3, "1.1.1.3")
    set_frr_superspine(ss4, "1.1.1.4")
    set_frr_superspine(ss5, "1.1.1.5")
    set_frr_superspine(ss6, "1.1.1.6")
    
    set_frr_spine(s1, "2.2.2.1", 65103, l1, l2)
    set_frr_spine(s2, "2.2.2.2", 65104, l1, l2)
    set_frr_spine(s3, "2.2.2.3", 65203, l3, l4)
    set_frr_spine(s4, "2.2.2.4", 65204, l3, l4)
    set_frr_spine(s5, "2.2.2.5", 65303, l5, l6)
    set_frr_spine(s6, "2.2.2.6", 65304, l5, l6)
    
    set_frr_leaf(l1, "3.3.3.1", 65101, s1, s2)
    set_frr_leaf(l2, "3.3.3.2", 65102, s1, s2)
    set_frr_leaf(l3, "3.3.3.3", 65201, s3, s4)
    set_frr_leaf(l4, "3.3.3.4", 65202, s3, s4)
    set_frr_leaf(l5, "3.3.3.5", 65301, s5, s6)
    set_frr_leaf(l6, "3.3.3.6", 65302, s5, s6)

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
