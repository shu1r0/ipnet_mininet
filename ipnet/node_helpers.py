from mininet.node import Node


def enable_srv6(node: Node, seg6_require_hmac=0, verbose=False):
    node.cmd("sysctl -w net.ipv4.ip_forward=1", verbose=verbose)
    node.cmd("sysctl -w net.ipv6.conf.all.forwarding=1", verbose=verbose)

    node.cmd("sysctl -w net.ipv6.conf.all.seg6_enabled=1", verbose=verbose)
    node.cmd("sysctl -w net.ipv6.conf.all.seg6_require_hmac={}".format(seg6_require_hmac), verbose=verbose)

    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.ipv6.conf.{}.seg6_enabled=1".format(i), verbose=verbose)
        node.cmd("sysctl -w net.ipv6.conf.{}.seg6_require_hmac={}".format(i, seg6_require_hmac), verbose=verbose)

    # set vrf conf
    node.cmd("sysctl -w net.vrf.strict_mode=1", verbose=verbose)


def disable_rp(node: Node, verbose=False):
    node.cmd("sysctl -w net.ipv4.conf.default.rp_filter=0", verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.all.rp_filter=0", verbose=verbose)
    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.ipv4.conf.{}.rp_filter=0".format(i), verbose=verbose)


def set_arp_for_router(node: Node, verbose=False):
    """

    References:
        * https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-44/Layer-3/Address-Resolution-Protocol-ARP/
    """
    node.cmd("sysctl -w net.ipv4.conf.default.arp_accept=0", verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.default.arp_announce=2", verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.default.arp_filter=0", verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.default.arp_ignore=1", verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.default.arp_notify=1", verbose=verbose)
    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.ipv4.conf.{}.arp_accept=0".format(i), verbose=verbose)
        node.cmd("sysctl -w net.ipv4.conf.{}.arp_announce=2".format(i), verbose=verbose)
        node.cmd("sysctl -w net.ipv4.conf.{}.arp_filter=0".format(i), verbose=verbose)
        node.cmd("sysctl -w net.ipv4.conf.{}.arp_ignore=1".format(i), verbose=verbose)
        node.cmd("sysctl -w net.ipv4.conf.{}.arp_notify=1".format(i), verbose=verbose)


def enable_mpls(node: Node, platform_labels=1048575, verbose=False):
    node.cmd("modprobe mpls-router", verbose=verbose)
    node.cmd("modprobe mpls_gso", verbose=verbose)
    node.cmd("modprobe mpls-iptunnel", verbose=verbose)

    node.cmd("sysctl -w net.mpls.platform_labels={}".format(platform_labels), verbose=verbose)
    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.mpls.conf.{}.input=1".format(i), verbose=verbose)


def add_vxlan_intf_cmd(node: Node, vxlan_id: int, intf_ip: str, vxlan_dev: str, remote_ip: str = None, group_ip: str = None, dst_port: int = 4789, verbose=False) -> str:
    """vxlan intf

    Args:
        node (Node): node
        vxlan_id (int): vxlan id
        intf_ip (str): vxlan interface ip address
        vxlan_dev (str): vxlan dev
        remote_ip (str, optional): remote ip address. Defaults to None.
        group_ip (str, optional): group ip address. Defaults to None.
        dst_port (int, optional): dst port. Defaults to 4789.
        verbose (bool, optional): cmd verbose. Defaults to False.

    Returns:
        str: vxlan interface name
    """
    # assert subnet
    assert len(intf_ip.split("/")) > 1, "`intf_ip` needs prefix. eg) 192.168.0.1/24"
    
    vxlan_intf = "vxlan{}".format(vxlan_id)
    if group_ip is None:
        node.cmd(
            "ip link add {vxlan_intf} type vxlan id {vxlan_id} local {local_ip} remote {remote_ip}  dstport {dst_port} nolearning dev {vxlan_dev}".format(
                vxlan_intf=vxlan_intf, vxlan_id=vxlan_id, local_ip=intf_ip.split("/")[0], remote_ip=remote_ip, dst_port=dst_port, vxlan_dev=vxlan_dev
            ), verbose=verbose)
    else:
        node.cmd(
            "ip link add {vxlan_intf} type vxlan id {vxlan_id} local {local_ip} group {group_ip} dstport {dst_port} nolearning dev {vxlan_dev}".format(
                vxlan_intf=vxlan_intf, vxlan_id=vxlan_id, local_ip=intf_ip.split("/")[0], group_ip=group_ip, dst_port=dst_port, vxlan_dev=vxlan_dev
            ), verbose=verbose)
    node.cmd("ip link set {} up".format(vxlan_intf), verbose=verbose)
    node.cmd("ip address add {} dev {}".format(intf_ip, vxlan_intf), verbose=verbose)
    
    return vxlan_intf


def add_vxlan_bridge_cmd(node: Node, vxlan_id: int, intf_ip: str, vxlan_dev: str, remote_ip: str = None, group_ip: str = None, dst_port: int = 4789, verbose=False) -> str:
    """vxlan bridge

    Args:
        node (Node): target node
        vxlan_id (int): vxlan id
        intf_ip (str): bridge ip address
        vxlan_dev (str): vxlan device
        remote_ip (str, optional): remote ip address. Defaults to None.
        group_ip (str, optional): vxlan group ip address. Defaults to None.
        dst_port (int, optional): vxlan dst port. Defaults to 4789.
        verbose (bool, optional): cmd verbose. Defaults to False.

    Returns:
        str : bridge name
    """
    # assert subnet
    assert len(intf_ip.split("/")) > 1, "`intf_ip` needs prefix. eg) 192.168.0.1/24"

    bridge = "br{}".format(vxlan_id)
    node.cmd("ip link add {} type bridge".format(bridge), verbose=verbose)
    node.cmd("ip link set dev {} up".format(bridge), verbose=verbose)

    vxlan_intf = "vxlan{vxlan_id}".format(node=str(node), vxlan_id=vxlan_id)
    if group_ip is None:
        node.cmd(
            "ip link add {vxlan_intf} type vxlan id {vxlan_id} local {local_ip} remote {remote_ip}  dstport {dst_port} nolearning dev {vxlan_dev}".format(
                vxlan_intf=vxlan_intf, vxlan_id=vxlan_id, local_ip=intf_ip.split("/")[0], remote_ip=remote_ip, dst_port=dst_port, vxlan_dev=vxlan_dev
            ), verbose=verbose)
    else:
        node.cmd(
            "ip link add {vxlan_intf} type vxlan id {vxlan_id} local {local_ip} group {group_ip} dstport {dst_port} nolearning dev {vxlan_dev}".format(
                vxlan_intf=vxlan_intf, vxlan_id=vxlan_id, local_ip=intf_ip.split("/")[0], group_ip=group_ip, dst_port=dst_port, vxlan_dev=vxlan_dev
            ), verbose=verbose)

    node.cmd("ip link set dev {} master {}".format(vxlan_intf, bridge), verbose=verbose)
    node.cmd("ip link set dev {} up".format(vxlan_intf), verbose=verbose)
    
    node.cmd("ip addr add {} dev {}".format(intf_ip, bridge), verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.{}.arp_accept=1".format(bridge), verbose=verbose)
    node.cmd("sysctl -w net.ipv4.conf.{}.proxy_arp=1".format(bridge), verbose=verbose)
    
    node.cmd("ip link set dev {} promisc on".format(vxlan_intf), verbose=verbose)
    return bridge

