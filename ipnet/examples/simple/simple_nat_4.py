from mininet.log import setLogLevel
from mininet.nodelib import NAT
from ipnet import IPNetwork, CLIX


r1_conf = """\
configure terminal
interface lo
  ip address 1.1.1.1/32
interface r1_r2
  ip address 192.168.1.1/24
router ospf
  network 1.1.1.1/32 area 0.0.0.0
  network 192.168.1.0/24 area 0.0.0.0
"""

r2_conf = """\
configure terminal
interface lo
  ip address 2.2.2.2/32
interface r2_r1
  ip address 192.168.1.2/24
router ospf
  network 2.2.2.2/32 area 0.0.0.0
  network 192.168.1.0/24 area 0.0.0.0
"""


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()
    r1 = net.addFRR('r1', enable_daemons=["ospfd"])
    r2 = net.addFRR('r2', enable_daemons=["ospfd"])
    net.addLink(r1, r2, intfName1="r1_r2", intfName2="r2_r1")
    
    # Create NAT node
    nat = net.addHost(
        "nat1",
        cls=NAT,
        ip="10.0.14.1",
        subnet='10.0.0.0/16',
        localInf="r1_nat",
        inNamespace=False,
    )
    
    net.addLink(r1, nat, intfName1="r1_nat", intfName2="nat_r1")
    
    net.start()
    r1.vtysh_cmd(r1_conf)
    r2.vtysh_cmd(r2_conf)

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()
