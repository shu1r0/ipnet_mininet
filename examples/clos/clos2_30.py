import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from mininet.nodelib import NAT
from mininet.log import setLogLevel

from ipnet import IPNetwork, SRv6Node, FRR, CLIX


spine_conf = """\
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
  neighbor {s_name}_l1 interface peer-group CLOS
  neighbor {s_name}_l2 interface peer-group CLOS
  neighbor {s_name}_l3 interface peer-group CLOS
  neighbor {s_name}_l4 interface peer-group CLOS
  neighbor {s_name}_l5 interface peer-group CLOS
  neighbor {s_name}_l6 interface peer-group CLOS
  neighbor {s_name}_l7 interface peer-group CLOS
  neighbor {s_name}_l8 interface peer-group CLOS
  neighbor {s_name}_e1 interface peer-group CLOS
  neighbor {s_name}_e2 interface peer-group CLOS
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
  address-family ipv4 unicast
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
  neighbor {l_name}_s1 interface peer-group CLOS
  neighbor {l_name}_s2 interface peer-group CLOS
  neighbor {l_name}_s3 interface peer-group CLOS
  neighbor {l_name}_s4 interface peer-group CLOS
  neighbor {l_name}_s5 interface peer-group CLOS
  neighbor {l_name}_s6 interface peer-group CLOS
  neighbor {l_name}_s7 interface peer-group CLOS
  neighbor {l_name}_s8 interface peer-group CLOS
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
  address-family ipv4 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
"""

external_conf = """\
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
  neighbor {e_name}_s1 interface peer-group CLOS
  neighbor {e_name}_s2 interface peer-group CLOS
  neighbor {e_name}_s3 interface peer-group CLOS
  neighbor {e_name}_s4 interface peer-group CLOS
  neighbor {e_name}_s5 interface peer-group CLOS
  neighbor {e_name}_s6 interface peer-group CLOS
  neighbor {e_name}_s7 interface peer-group CLOS
  neighbor {e_name}_s8 interface peer-group CLOS
  neighbor {e_name}_co1 interface peer-group CLOS
  neighbor {e_name}_co2 interface peer-group CLOS
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
  address-family ipv4 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
"""


core_conf = """\
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
  neighbor CLOS default-originate
  neighbor {co_name}_e1 interface peer-group CLOS
  neighbor {co_name}_e2 interface peer-group CLOS
  address-family ipv6 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
  address-family ipv4 unicast
    redistribute connected
    neighbor CLOS activate
  exit-address-family
"""


class Leaf(SRv6Node):
    pass


class Spine(SRv6Node):
    pass


class ExternalRouter(SRv6Node):
    pass


class CoreRouter(SRv6Node):
    pass


def run():
    setLogLevel("info")
    net = IPNetwork()

    # Spine
    s1 = net.addFRR("s1", cls=Spine, enable_daemons=["bgpd"])
    s2 = net.addFRR("s2", cls=Spine, enable_daemons=["bgpd"])
    s3 = net.addFRR("s3", cls=Spine, enable_daemons=["bgpd"])
    s4 = net.addFRR("s4", cls=Spine, enable_daemons=["bgpd"])
    s5 = net.addFRR("s5", cls=Spine, enable_daemons=["bgpd"])
    s6 = net.addFRR("s6", cls=Spine, enable_daemons=["bgpd"])
    s7 = net.addFRR("s7", cls=Spine, enable_daemons=["bgpd"])
    s8 = net.addFRR("s8", cls=Spine, enable_daemons=["bgpd"])

    # Leaf
    l1 = net.addFRR("l1", cls=Leaf, enable_daemons=["bgpd"])
    l2 = net.addFRR("l2", cls=Leaf, enable_daemons=["bgpd"])
    l3 = net.addFRR("l3", cls=Leaf, enable_daemons=["bgpd"])
    l4 = net.addFRR("l4", cls=Leaf, enable_daemons=["bgpd"])
    l5 = net.addFRR("l5", cls=Leaf, enable_daemons=["bgpd"])
    l6 = net.addFRR("l6", cls=Leaf, enable_daemons=["bgpd"])
    l7 = net.addFRR("l7", cls=Leaf, enable_daemons=["bgpd"])
    l8 = net.addFRR("l8", cls=Leaf, enable_daemons=["bgpd"])

    # External
    e1 = net.addFRR("e1", cls=ExternalRouter, enable_daemons=["bgpd"])
    e2 = net.addFRR("e2", cls=ExternalRouter, enable_daemons=["bgpd"])

    # Core
    co1 = net.addFRR("co1", cls=CoreRouter, enable_daemons=["bgpd"])
    co2 = net.addFRR("co2", cls=CoreRouter, enable_daemons=["bgpd"])

    # Host
    h1 = net.addHost("h1", cls=SRv6Node)
    h2 = net.addHost("h2", cls=SRv6Node)
    h3 = net.addHost("h3", cls=SRv6Node)
    h4 = net.addHost("h4", cls=SRv6Node)
    h5 = net.addHost("h5", cls=SRv6Node)
    h6 = net.addHost("h6", cls=SRv6Node)
    h7 = net.addHost("h7", cls=SRv6Node)
    h8 = net.addHost("h8", cls=SRv6Node)

    # NAT for VM
    nat1 = net.addHost("nat1", cls=NAT, ip="192.168.100.1/24", subnet='192.168.0.0/16', inNamespace=False)
    nat2 = net.addHost("nat2", cls=NAT, ip="192.168.200.1/24", subnet='192.168.0.0/16', inNamespace=False)
    
    # set SRv6 SID
    sid_format = "fc00:bbbb:bbbb:bbbb:{node}:{func}:0:{args}/80"
    format_dict = {"node": -1, "func": 1, "args": 0}
    for i, n in enumerate(net.nameToNode.values(), start=1):
        if isinstance(n, Spine):
            format_dict["node"] = "a" + str(i)
            n.setIPv6Cmd(sid_format.format(**format_dict), "lo")
        if isinstance(n, Leaf):
            format_dict["node"] = "b" + str(i)
            n.setIPv6Cmd(sid_format.format(**format_dict), "lo")
        if isinstance(n, ExternalRouter):
            format_dict["node"] = "c" + str(i)
            n.setIPv6Cmd(sid_format.format(**format_dict), "lo")
    
    def set_link(n1, n2, **params):
        """set link between node1 and node2"""
        intf1 = str(n1)+"_"+str(n2)
        intf2 = str(n2)+"_"+str(n1)
        net.addLink(n1, n2, intfName1=intf1, intfName2=intf2, **params)
    
    def set_link_spine():
        spines = [n for n in net.nameToNode.values() if isinstance(n, Spine)]
        leafs = [n for n in net.nameToNode.values() if isinstance(n, Leaf)]
        for s in spines:
            for l in leafs:
                set_link(s, l)
        externals = [n for n in net.nameToNode.values() if isinstance(n, ExternalRouter)]
        for s in spines:
            for e in externals:
                set_link(s, e)
    
    def set_link_hosts(r, h1, block):
        def set_link_host(r, n, block):
            ipv6_1 = "fc00:{}::1/64".format(block)
            ipv6_2 = "fc00:{}::2/64".format(block)
            ipv4_1 = "192.168.{}.1/24".format(block)
            ipv4_2 = "192.168.{}.2/24".format(block)
            intf1 = str(r)+"_"+str(n)
            intf2 = str(n)+"_"+str(r)
            net.addLink(r, n, 
                        intfName1=intf1, params1={"ip": ipv4_1},
                        intfName2=intf2, params2={"ip": ipv4_2})
            r.setIPv6Cmd(ipv6_1, intf1)
            n.setIPv6Cmd(ipv6_2, intf2)
            
            n.cmd("ip route add default dev {} via {}".format(intf2, ipv4_1.split("/")[0]))
            n.cmd("ip -6 route add default dev {} via {}".format(intf2, ipv6_1.split("/")[0]))
            
        set_link_host(r, h1, block)

    # setup
    set_link_spine()

    # set hosts
    set_link_hosts(l1, h1, 1)
    set_link_hosts(l2, h2, 2)
    set_link_hosts(l3, h3, 3)
    set_link_hosts(l4, h4, 4)
    set_link_hosts(l5, h5, 5)
    set_link_hosts(l6, h6, 6)
    set_link_hosts(l7, h7, 7)
    set_link_hosts(l8, h8, 8)
    
    # set external
    set_link(e1, co1)
    set_link(e1, co2)
    set_link(e2, co1)
    set_link(e2, co2)

    # set NAT
    set_link(co1, nat1, params1={"ip": "192.168.100.3/24"})
    set_link(co2, nat2, params1={"ip": "192.168.200.3/24"})
    nat1.configDefault()
    nat2.configDefault()
    co1.cmd("ip route add default dev {} via {}".format("co1_nat1", "192.168.100.1"))
    co2.cmd("ip route add default dev {} via {}".format("co2_nat2", "192.168.200.1"))
    nat1.cmd("ip route add 192.168.0.0/16 nexthop via 192.168.100.3 dev nat1_co1 weight 1 nexthop via 192.168.200.3 dev nat2_co2 weight 1")

    net.start()

    # FRRouting setup
    def set_frr_spine(ss, router_id):
        ss.vtysh_cmd(spine_conf.format(
            router_id=router_id,
            s_name=str(ss)
        ))
        
    def set_frr_leaf(s, router_id, as_number):
        s.vtysh_cmd(leaf_conf.format(
            as_number=as_number,
            router_id=router_id,
            l_name=str(s),
        ))
    
    def set_frr_external(e, router_id, as_number):
        e.vtysh_cmd(external_conf.format(
            as_number=as_number,
            router_id=router_id,
            e_name=str(e),
        ))
    
    def set_frr_core(co, router_id, as_number):
        co.vtysh_cmd(core_conf.format(
            as_number=as_number,
            router_id=router_id,
            co_name=str(co),
        ))
    
    set_frr_spine(s1, "1.1.1.1")
    set_frr_spine(s2, "1.1.1.2")
    set_frr_spine(s3, "1.1.1.3")
    set_frr_spine(s4, "1.1.1.4")
    set_frr_spine(s5, "1.1.1.5")
    set_frr_spine(s6, "1.1.1.6")
    set_frr_spine(s7, "1.1.1.7")
    set_frr_spine(s8, "1.1.1.8")
    
    set_frr_leaf(l1, "2.2.2.1", 65101)
    set_frr_leaf(l2, "2.2.2.2", 65102)
    set_frr_leaf(l3, "2.2.2.3", 65103)
    set_frr_leaf(l4, "2.2.2.4", 65104)
    set_frr_leaf(l5, "2.2.2.5", 65105)
    set_frr_leaf(l6, "2.2.2.6", 65106)
    set_frr_leaf(l7, "2.2.2.7", 65107)
    set_frr_leaf(l8, "2.2.2.8", 65108)
    
    set_frr_external(e1, "3.3.3.1", 65100)
    set_frr_external(e2, "3.3.3.2", 65100)
    
    set_frr_core(co1, "4.4.4.1", 65200)
    set_frr_core(co2, "4.4.4.2", 65200)

    CLIX(net)
    
    net.stop()


if __name__ == "__main__":
    run()
