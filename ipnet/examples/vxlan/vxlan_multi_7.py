"""

References:
    * https://github.com/tinynetwork/tinet/blob/master/examples/basic_vxlan/vxlan_mcast.yaml
"""
from mininet.node import OVSBridge
from mininet.log import setLogLevel
from ipnet import IPNetwork, CLIX, IPNode, add_vxlan_bridge_cmd


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()

    s1 = net.addSwitch('s1', cls=OVSBridge)
    r1 = net.addRouter('r1')
    r2 = net.addRouter('r2')
    h1: IPNode = net.addHost("h1", cls=IPNode)
    h2: IPNode = net.addHost("h2", cls=IPNode)
    h3: IPNode = net.addHost("h3", cls=IPNode)
    h4: IPNode = net.addHost("h4", cls=IPNode)

    net.addLink(r1, h1, intfName1="r1_h1", intfName2="h1_r1", params2={"ip": "10.100.1.2/16"})
    net.addLink(r1, h2, intfName1="r1_h2", intfName2="h2_r1", params2={"ip": "10.200.1.2/16"})
    net.addLink(r2, h3, intfName1="r2_h3", intfName2="h3_r2", params2={"ip": "10.100.2.2/16"})
    net.addLink(r2, h4, intfName1="r2_h4", intfName2="h4_r2", params2={"ip": "10.200.2.2/16"})

    net.addLink(s1, r1, intfName1="s1_r1", intfName2="r1_s1", params2={"ip": "10.0.0.1/24"})
    net.addLink(s1, r2, intfName1="s1_r2", intfName2="r2_s1", params2={"ip": "10.0.0.2/24"})

    r1_vxlan100_br = add_vxlan_bridge_cmd(r1, vxlan_id=100, intf_ip="10.100.1.1/16", vxlan_dev="r1_s1", group_ip="239.0.1.1", verbose=True)
    r1_vxlan200_br = add_vxlan_bridge_cmd(r1, vxlan_id=200, intf_ip="10.200.1.1/16", vxlan_dev="r1_s1", group_ip="239.0.1.1", verbose=True)
    r2_vxlan100_br = add_vxlan_bridge_cmd(r2, vxlan_id=100, intf_ip="10.100.2.1/16", vxlan_dev="r2_s1", group_ip="239.0.1.1", verbose=True)
    r2_vxlan200_br = add_vxlan_bridge_cmd(r2, vxlan_id=200, intf_ip="10.200.2.1/16", vxlan_dev="r2_s1", group_ip="239.0.1.1", verbose=True)
    r1.cmd("ip link set dev {} master {}".format("r1_h1", r1_vxlan100_br))
    r1.cmd("ip link set dev {} master {}".format("r1_h2", r1_vxlan200_br))
    r2.cmd("ip link set dev {} master {}".format("r2_h3", r2_vxlan100_br))
    r2.cmd("ip link set dev {} master {}".format("r2_h4", r2_vxlan200_br))

    # r1.tcpdump("r1_s1")
    # r1.tcpdump("vxlan100")
    # r2.tcpdump("r2_s1")

    net.start()

    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()

