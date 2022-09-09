from mininet.log import setLogLevel
from ipnet import IPNetwork, CLIX, IPNode, add_vxlan_intf_cmd


def setup() -> IPNetwork:
    setLogLevel("info")
    net = IPNetwork()
    
    r1 = net.addFRR('r1')
    h1: IPNode = net.addHost("h1", cls=IPNode)
    h2: IPNode = net.addHost("h2", cls=IPNode)
    
    net.addLink(r1, h1, 
                intfName1="r1_h1", params1={"ip": "192.168.10.1/24"},
                intfName2="h1_r1", params2={"ip": "192.168.10.2/24"})
    net.addLink(r1, h2, 
                intfName1="r1_h2", params1={"ip": "192.168.20.1/24"},
                intfName2="h2_r1", params2={"ip": "192.168.20.2/24"})
    
    add_vxlan_intf_cmd(h1, "h1_r1", 100, intf_ip="172.16.10.1/24", remote_ip="192.168.20.2")
    add_vxlan_intf_cmd(h2, "h2_r1", 100, intf_ip="172.16.10.2/24", remote_ip="192.168.10.2")
    
    h1.add_default_route_cmd("h1_r1", "192.168.10.1")
    h2.add_default_route_cmd("h2_r1", "192.168.20.1")
    
    h1.tcpdump("h1_r1")
    h2.tcpdump("h2_r1")
    
    net.start()
    
    return net


if __name__ == "__main__":
    net = setup()
    CLIX(net)
    net.stop()

