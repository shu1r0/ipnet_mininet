from mininet.log import setLogLevel

from ipnet import IPNetwork, FRR, CLIX, IPNode


super_spine_conf = """\
enable
configure terminal
router bgp 65000
  bgp router-id {router_id}
  no bgp default ipv4-unicast
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
  neighbor {ss_name}_s7 interface peer-group CLOS
  neighbor {ss_name}_s8 interface peer-group CLOS
  neighbor {ss_name}_s9 interface peer-group CLOS
  neighbor {ss_name}_s10 interface peer-group CLOS
  neighbor {ss_name}_s11 interface peer-group CLOS
  neighbor {ss_name}_s12 interface peer-group CLOS
  neighbor {ss_name}_s13 interface peer-group CLOS
  neighbor {ss_name}_s14 interface peer-group CLOS
  neighbor {ss_name}_s15 interface peer-group CLOS
  neighbor {ss_name}_s16 interface peer-group CLOS
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
"""

spine_conf = """\
enable
configure terminal
router bgp {as_number}
  bgp router-id {router_id}
  no bgp default ipv4-unicast
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
  neighbor {s_name}_ss7 interface peer-group CLOS
  neighbor {s_name}_ss8 interface peer-group CLOS
  neighbor {s_name}_ss9 interface peer-group CLOS
  neighbor {s_name}_ss10 interface peer-group CLOS
  neighbor {s_name}_ss11 interface peer-group CLOS
  neighbor {s_name}_ss12 interface peer-group CLOS
  neighbor {s_name}_ss13 interface peer-group CLOS
  neighbor {s_name}_ss14 interface peer-group CLOS
  neighbor {s_name}_ss15 interface peer-group CLOS
  neighbor {s_name}_ss16 interface peer-group CLOS
  neighbor {s_name}_{l_name1} interface peer-group CLOS
  neighbor {s_name}_{l_name2} interface peer-group CLOS
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
"""

leaf_conf = """\
enable
configure terminal
router bgp {as_number}
  bgp router-id {router_id}
  no bgp default ipv4-unicast
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
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
"""

class Leaf(FRR):
    pass


class Spine(FRR):
    pass


class SuperSpine(FRR):
    pass


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()
    
    ss1 = net.addFRR("ss1", cls=SuperSpine, enable_daemons=["bgpd"])
    ss2 = net.addFRR("ss2", cls=SuperSpine, enable_daemons=["bgpd"])
    ss3 = net.addFRR("ss3", cls=SuperSpine, enable_daemons=["bgpd"])
    ss4 = net.addFRR("ss4", cls=SuperSpine, enable_daemons=["bgpd"])
    ss5 = net.addFRR("ss5", cls=SuperSpine, enable_daemons=["bgpd"])
    ss6 = net.addFRR("ss6", cls=SuperSpine, enable_daemons=["bgpd"])
    ss7 = net.addFRR("ss7", cls=SuperSpine, enable_daemons=["bgpd"])
    ss8 = net.addFRR("ss8", cls=SuperSpine, enable_daemons=["bgpd"])
    ss9 = net.addFRR("ss9", cls=SuperSpine, enable_daemons=["bgpd"])
    ss10 = net.addFRR("ss10", cls=SuperSpine, enable_daemons=["bgpd"])
    ss11 = net.addFRR("ss11", cls=SuperSpine, enable_daemons=["bgpd"])
    ss12 = net.addFRR("ss12", cls=SuperSpine, enable_daemons=["bgpd"])
    ss13 = net.addFRR("ss13", cls=SuperSpine, enable_daemons=["bgpd"])
    ss14 = net.addFRR("ss14", cls=SuperSpine, enable_daemons=["bgpd"])
    ss15 = net.addFRR("ss15", cls=SuperSpine, enable_daemons=["bgpd"])
    ss16 = net.addFRR("ss16", cls=SuperSpine, enable_daemons=["bgpd"])
    
    s1 = net.addFRR("s1", cls=Spine, enable_daemons=["bgpd"])
    s2 = net.addFRR("s2", cls=Spine, enable_daemons=["bgpd"])
    s3 = net.addFRR("s3", cls=Spine, enable_daemons=["bgpd"])
    s4 = net.addFRR("s4", cls=Spine, enable_daemons=["bgpd"])
    s5 = net.addFRR("s5", cls=Spine, enable_daemons=["bgpd"])
    s6 = net.addFRR("s6", cls=Spine, enable_daemons=["bgpd"])
    s7 = net.addFRR("s7", cls=Spine, enable_daemons=["bgpd"])
    s8 = net.addFRR("s8", cls=Spine, enable_daemons=["bgpd"])
    s9 = net.addFRR("s9", cls=Spine, enable_daemons=["bgpd"])
    s10 = net.addFRR("s10", cls=Spine, enable_daemons=["bgpd"])
    s11 = net.addFRR("s11", cls=Spine, enable_daemons=["bgpd"])
    s12 = net.addFRR("s12", cls=Spine, enable_daemons=["bgpd"])
    s13 = net.addFRR("s13", cls=Spine, enable_daemons=["bgpd"])
    s14 = net.addFRR("s14", cls=Spine, enable_daemons=["bgpd"])
    s15 = net.addFRR("s15", cls=Spine, enable_daemons=["bgpd"])
    s16 = net.addFRR("s16", cls=Spine, enable_daemons=["bgpd"])
    
    l1 = net.addFRR("l1", cls=Leaf, enable_daemons=["bgpd"])
    l2 = net.addFRR("l2", cls=Leaf, enable_daemons=["bgpd"])
    l3 = net.addFRR("l3", cls=Leaf, enable_daemons=["bgpd"])
    l4 = net.addFRR("l4", cls=Leaf, enable_daemons=["bgpd"])
    l5 = net.addFRR("l5", cls=Leaf, enable_daemons=["bgpd"])
    l6 = net.addFRR("l6", cls=Leaf, enable_daemons=["bgpd"])
    l7 = net.addFRR("l7", cls=Leaf, enable_daemons=["bgpd"])
    l8 = net.addFRR("l8", cls=Leaf, enable_daemons=["bgpd"])
    l9 = net.addFRR("l9", cls=Leaf, enable_daemons=["bgpd"])
    l10 = net.addFRR("l10", cls=Leaf, enable_daemons=["bgpd"])
    l11 = net.addFRR("l11", cls=Leaf, enable_daemons=["bgpd"])
    l12 = net.addFRR("l12", cls=Leaf, enable_daemons=["bgpd"])
    l13 = net.addFRR("l13", cls=Leaf, enable_daemons=["bgpd"])
    l14 = net.addFRR("l14", cls=Leaf, enable_daemons=["bgpd"])
    l15 = net.addFRR("l15", cls=Leaf, enable_daemons=["bgpd"])
    l16 = net.addFRR("l16", cls=Leaf, enable_daemons=["bgpd"])
    

    # host
    h1 = net.addHost("h1", cls=IPNode)
    h2 = net.addHost("h2", cls=IPNode)
    h3 = net.addHost("h3", cls=IPNode)
    h4 = net.addHost("h4", cls=IPNode)
    h5 = net.addHost("h5", cls=IPNode)
    h6 = net.addHost("h6", cls=IPNode)
    h7 = net.addHost("h7", cls=IPNode)
    h8 = net.addHost("h8", cls=IPNode)
    h9 = net.addHost("h9", cls=IPNode)
    h10 = net.addHost("h10", cls=IPNode)
    h11 = net.addHost("h11", cls=IPNode)
    h12 = net.addHost("h12", cls=IPNode)
    h13 = net.addHost("h13", cls=IPNode)
    h14 = net.addHost("h14", cls=IPNode)
    h15 = net.addHost("h15", cls=IPNode)
    h16 = net.addHost("h16", cls=IPNode)
    h17 = net.addHost("h17", cls=IPNode)
    h18 = net.addHost("h18", cls=IPNode)
    h19 = net.addHost("h19", cls=IPNode)
    h20 = net.addHost("h20", cls=IPNode)
    h21 = net.addHost("h21", cls=IPNode)
    h22 = net.addHost("h22", cls=IPNode)
    h23 = net.addHost("h23", cls=IPNode)
    h24 = net.addHost("h24", cls=IPNode)
    h25 = net.addHost("h25", cls=IPNode)
    h26 = net.addHost("h26", cls=IPNode)
    h27 = net.addHost("h27", cls=IPNode)
    h28 = net.addHost("h28", cls=IPNode)
    h29 = net.addHost("h29", cls=IPNode)
    h30 = net.addHost("h30", cls=IPNode)
    h31 = net.addHost("h31", cls=IPNode)
    h32 = net.addHost("h32", cls=IPNode)
    
    # set SRv6 SID
    sid_format = "fdbb:{node}::{func}:0:{args}/80"
    format_dict = {"node": -1, "func": 1, "args": 0}
    ## fcbb:a<n>::
    for i, n in enumerate(net.get_nodes_by_cls(SuperSpine), start=1):
        format_dict["node"] = "a" + str(i)
        n.set_ipv6_cmd(sid_format.format(**format_dict), "lo")
    ## fcbb:b<n>::
    for i, n in enumerate(net.get_nodes_by_cls(Spine), start=1):
        format_dict["node"] = "b" + str(i)
        n.set_ipv6_cmd(sid_format.format(**format_dict), "lo")
    ## fcbb:c<n>::
    for i, n in enumerate(net.get_nodes_by_cls(Leaf), start=1):
        format_dict["node"] = "c" + str(i)
        n.set_ipv6_cmd(sid_format.format(**format_dict), "lo")
    
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
    
    def set_link_hosts(r, h1, h2, block):
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
        set_link_host(r, h2, int(block)+1)

    # setup
    set_link_super_spine()
    
    set_link_pod(s1, s2, l1, l2)
    set_link_pod(s3, s4, l3, l4)
    set_link_pod(s5, s6, l5, l6)
    set_link_pod(s7, s8, l7, l8)
    set_link_pod(s9, s10, l9, l10)
    set_link_pod(s11, s12, l11, l12)
    set_link_pod(s13, s14, l13, l14)
    set_link_pod(s15, s16, l15, l16)

    set_link_hosts(l1, h1, h2, 1)
    set_link_hosts(l2, h3, h4, 3)
    set_link_hosts(l3, h5, h6, 5)
    set_link_hosts(l4, h7, h8, 7)
    set_link_hosts(l5, h9, h10, 9)
    set_link_hosts(l6, h11, h12, 11)
    set_link_hosts(l7, h13, h14, 13)
    set_link_hosts(l8, h15, h16, 15)
    set_link_hosts(l9, h17, h18, 17)
    set_link_hosts(l10, h19, h20, 19)
    set_link_hosts(l11, h21, h22, 21)
    set_link_hosts(l12, h23, h24, 23)
    set_link_hosts(l13, h25, h26, 25)
    set_link_hosts(l14, h27, h28, 27)
    set_link_hosts(l15, h29, h30, 29)
    set_link_hosts(l16, h31, h32, 31)
    
    
    net.start()
    
    # FRRouting setup
    def set_frr_superspine(ss, router_id):
        ss.vtysh_cmd(super_spine_conf.format(
            router_id=router_id,
            ss_name=str(ss)
        ))
        
    def set_frr_spine(s, router_id, as_number, l1, l2):
        s.vtysh_cmd(spine_conf.format(
            as_number=as_number,
            router_id=router_id,
            s_name=str(s),
            l_name1=str(l1),
            l_name2=str(l2)
        ))
        
    def set_frr_leaf(l, router_id, as_number, s1, s2):
        l.vtysh_cmd(leaf_conf.format(
            as_number=as_number,
            router_id=router_id,
            l_name=str(l),
            s_name1=str(s1),
            s_name2=str(s2)
        ))
    
    set_frr_superspine(ss1, "1.1.1.1")
    set_frr_superspine(ss2, "1.1.1.2")
    set_frr_superspine(ss3, "1.1.1.3")
    set_frr_superspine(ss4, "1.1.1.4")
    set_frr_superspine(ss5, "1.1.1.5")
    set_frr_superspine(ss6, "1.1.1.6")
    set_frr_superspine(ss7, "1.1.1.7")
    set_frr_superspine(ss8, "1.1.1.8")
    set_frr_superspine(ss9, "1.1.1.9")
    set_frr_superspine(ss10, "1.1.1.10")
    set_frr_superspine(ss11, "1.1.1.11")
    set_frr_superspine(ss12, "1.1.1.12")
    set_frr_superspine(ss13, "1.1.1.13")
    set_frr_superspine(ss14, "1.1.1.14")
    set_frr_superspine(ss15, "1.1.1.15")
    set_frr_superspine(ss16, "1.1.1.16")
    
    set_frr_spine(s1, "2.2.2.1", 65103, l1, l2)
    set_frr_spine(s2, "2.2.2.2", 65104, l1, l2)
    set_frr_spine(s3, "2.2.2.3", 65203, l3, l4)
    set_frr_spine(s4, "2.2.2.4", 65204, l3, l4)
    set_frr_spine(s5, "2.2.2.5", 65303, l5, l6)
    set_frr_spine(s6, "2.2.2.6", 65304, l5, l6)
    set_frr_spine(s7, "2.2.2.7", 65403, l7, l8)
    set_frr_spine(s8, "2.2.2.8", 65404, l7, l8)
    set_frr_spine(s9, "2.2.2.9", 65503, l9, l10)
    set_frr_spine(s10, "2.2.2.10", 65504, l9, l10)
    set_frr_spine(s11, "2.2.2.11", 65603, l11, l12)
    set_frr_spine(s12, "2.2.2.12", 65604, l11, l12)
    set_frr_spine(s13, "2.2.2.13", 65703, l13, l14)
    set_frr_spine(s14, "2.2.2.14", 65704, l13, l14)
    set_frr_spine(s15, "2.2.2.15", 65803, l15, l16)
    set_frr_spine(s16, "2.2.2.16", 65804, l15, l16)
    
    set_frr_leaf(l1, "3.3.3.1", 65101, s1, s2)
    set_frr_leaf(l2, "3.3.3.2", 65102, s1, s2)
    set_frr_leaf(l3, "3.3.3.3", 65201, s3, s4)
    set_frr_leaf(l4, "3.3.3.4", 65202, s3, s4)
    set_frr_leaf(l5, "3.3.3.5", 65301, s5, s6)
    set_frr_leaf(l6, "3.3.3.6", 65302, s5, s6)
    set_frr_leaf(l7, "3.3.3.7", 65401, s7, s8)
    set_frr_leaf(l8, "3.3.3.8", 65402, s7, s8)
    set_frr_leaf(l9, "3.3.3.9", 65501, s9, s10)
    set_frr_leaf(l10, "3.3.3.10", 65502, s9, s10)
    set_frr_leaf(l11, "3.3.3.11", 65601, s11, s12)
    set_frr_leaf(l12, "3.3.3.12", 65602, s11, s12)
    set_frr_leaf(l13, "3.3.3.13", 65701, s13, s14)
    set_frr_leaf(l14, "3.3.3.14", 65702, s13, s14)
    set_frr_leaf(l15, "3.3.3.15", 65801, s15, s16)
    set_frr_leaf(l16, "3.3.3.16", 65802, s15, s16)

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
