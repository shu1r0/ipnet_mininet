from mininet.node import Node


def enable_srv6(node: Node, seg6_require_hmac=0):
    node.cmd("sysctl -w net.ipv4.ip_forward=1")
    node.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")

    node.cmd("sysctl -w net.ipv6.conf.all.seg6_enabled=1")
    node.cmd("sysctl -w net.ipv6.conf.all.seg6_require_hmac={}".format(seg6_require_hmac))

    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.ipv6.conf.{}.seg6_enabled=1".format(i))
        node.cmd("sysctl -w net.ipv6.conf.{}.seg6_require_hmac={}".format(i, seg6_require_hmac))

    # set vrf conf
    node.cmd("sysctl -w net.vrf.strict_mode=1")


def disable_rp(node: Node):
    node.cmd("sysctl -w net.ipv4.conf.all.rp_filter=0")
    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.ipv4.conf.{}.rp_filter=0".format(i))


def enable_mpls(node: Node, platform_labels=1048575):
    node.cmd("modprobe mpls-router")
    node.cmd("modprobe mpls_gso")
    node.cmd("modprobe mpls-iptunnel")

    node.cmd("sysctl -w net.mpls.platform_labels={}".format(platform_labels))
    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.mpls.conf.{}.input=1".format(i))


def add_vxlan_intf_cmd(node: Node, intf: str, vxlan_id: int, intf_ip: str, remote_ip: str, dst_port: int = 4789):
    # assert subnet
    assert len(intf_ip.split("/")) > 1, "`intf_ip` needs prefix. eg) 192.168.0.1/24"
    
    vxlan_intf = "{node}-vxlan{vxlan_id}".format(node=str(node), vxlan_id=vxlan_id)
    node.cmdPrint("ip link add {vxlan_intf} type vxlan id {vxlan_id} remote {remote_ip} dstport {dst_port} dev {intf}".format(
        vxlan_intf=vxlan_intf, vxlan_id=vxlan_id, remote_ip=remote_ip, dst_port=dst_port, intf=intf
    ))
    node.cmdPrint("ip link set {} up".format(vxlan_intf))
    node.cmdPrint("ip address add {} dev {}".format(intf_ip, vxlan_intf))

