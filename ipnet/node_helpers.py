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
    node.cmd("sysctl -w net.mpls.platform_labels={}".format(platform_labels))
    for i in [*node.nameToIntf.keys(), "lo"]:
        node.cmd("sysctl -w net.mpls.conf.{}.input=1".format(i))
