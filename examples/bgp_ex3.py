from mininet.log import setLogLevel

from frrnet.frr_net import FRRNetwork, CLIWithVtysh

r1_conf = """
enable
conf t
interface lo0
 ip address 192.168.0.1 255.255.255.255
 ip address 10.1.1.1 255.255.255.255
interface r1-e0
 ip address 192.168.13.1 255.255.255.0
 half-duplex
interface r1-e1
 ip address 10.1.14.1 255.255.255.0
 half-duplex
interface r1-e2
 ip address 10.1.41.1 255.255.255.0
 half-duplex
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
router bgp 65001
  neighbor 192.168.0.2 remote-as 65001
  neighbor 192.168.0.2 update-source lo0
  neighbor 192.168.0.3 remote-as 65001
  neighbor 192.168.0.3 update-source lo0
"""

r2_conf = """
enable
conf t
interface lo0
 ip address 192.168.0.2 255.255.255.255
interface r2-e0
 ip address 192.168.23.2 255.255.255.0
 half-duplex
interface r2-e1
 ip address 10.2.25.2 255.255.255.0
 half-duplex
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
router bgp 65001
  neighbor 192.168.0.1 remote-as 65001
  neighbor 192.168.0.1 update-source lo0
  neighbor 192.168.0.3 remote-as 65001
  neighbor 192.168.0.3 update-source lo0
"""

r3_conf = """
enable
conf t
interface lo0
 ip address 192.168.0.3 255.255.255.255
interface lo0
 ip address 100.1.1.3 255.255.255.0
interface r3-e0
 ip address 192.168.13.3 255.255.255.0
 half-duplex
interface r3-e1
 ip address 192.168.23.3 255.255.255.0
 ip ospf cost 1
 half-duplex
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
router bgp 65001
  neighbor 192.168.0.2 remote-as 65001
  neighbor 192.168.0.2 update-source lo0
  neighbor 192.168.0.1 remote-as 65001
  neighbor 192.168.0.1 update-source lo0
"""

r4_conf = """
enable
conf t
interface lo0
 ip address 192.168.0.4 255.255.255.255
interface lo0
 ip address 10.1.1.4 255.255.255.255
interface r4-e0
 ip address 192.168.46.4 255.255.255.0
 half-duplex
interface r4-e1
 ip address 10.1.14.4 255.255.255.0
 half-duplex
interface r4-e2
 ip address 10.1.41.4 255.255.255.0
 half-duplex
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
router bgp 65002
  neighbor 192.168.0.5 remote-as 65001
  neighbor 192.168.0.5 update-source lo0
  neighbor 192.168.0.6 remote-as 65002
  neighbor 192.168.0.6 update-source lo0
"""

r5_conf = """
enable
conf t
interface lo0
 ip address 192.168.0.5 255.255.255.255
interface r5-e0
 ip address 192.168.56.5 255.255.255.0
 half-duplex
interface r5-e1
 ip address 10.2.25.5 255.255.255.0
 half-duplex
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
router bgp 65002
  neighbor 192.168.0.4 remote-as 65001
  neighbor 192.168.0.4 update-source lo0
  neighbor 192.168.0.6 remote-as 65002
  neighbor 192.168.0.6 update-source lo0
"""

r6_conf = """
enable
conf t
interface lo0
 ip address 192.168.0.6 255.255.255.255
interface lo0
 ip address 100.2.2.6 255.255.255.0
interface r6-e0
 ip address 192.168.46.6 255.255.255.0
 half-duplex
interface r6-e1
 ip address 192.168.56.6 255.255.255.0
 half-duplex
router ospf 1
 network 192.168.0.0 0.0.255.255 area 0
router bgp 65002
  neighbor 192.168.0.5 remote-as 65001
  neighbor 192.168.0.5 update-source lo0
  neighbor 192.168.0.4 remote-as 65002
  neighbor 192.168.0.4 update-source lo0
"""




def main():
    setLogLevel("info")
    net = FRRNetwork()
    
    for i in range(1, 6):
        net.addFRR("r{}".format(i))

    net.addLink("r1", "r3", intfName1="r1-e0", intfName2="r3-e0")
    net.addLink("r2", "r3", intfName1="r2-e0", intfName2="r3-e1")
    net.addLink("r2", "r5", intfName1="r2-e1", intfName2="r5-e1")
    net.addLink("r5", "r6", intfName1="r5-e0", intfName2="r6-e1")
    net.addLink("r4", "r6", intfName1="r4-e0", intfName2="r6-e0")
    net.addLink("r1", "r3", intfName1="r1-e0", intfName2="r3-e0")

    net.start()
    CLIWithVtysh(net)
    net.stop()


if __name__ == '__main__':
    main()
