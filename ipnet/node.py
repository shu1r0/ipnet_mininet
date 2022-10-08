"""

References:
    * https://github.com/FRRouting/frr/blob/c143b875193c0ec4eaaeb1f0ddb2c744bd04ba3c/tests/topotests/lib/topogen.py
    * https://blog.bobuhiro11.net/2021/05-08-mininet_frr.html
"""

import pkgutil
import json
from jinja2 import Template
from mininet.node import Node

from .node_helpers import disable_forwarding, enable_forwarding, enable_srv6, disable_rp, set_arp_for_router, enable_mpls


class IPNode(Node):

    def config(self, **params):
        self.cmd("ifconfig lo up")

    def set_ip_cmd(self, ip, intf_name):
        self.cmd("ip addr add {} dev {}".format(ip, intf_name))

    def set_ipv6_cmd(self, ipv6, intf_name):
        self.cmd("ip -6 addr add {} dev {}".format(ipv6, intf_name))

    def add_default_route_cmd(self, intf: str, nexthop: str):
        self.cmd("ip route add default dev {} via {}".format(intf, nexthop))

    def add_v6_default_route_cmd(self, intf: str, nexthop: str):
        self.cmd("ip -6 route add default dev {} via {}".format(intf, nexthop))

    def tcpdump(self, intf):
        cmd = "tcpdump -i " + intf + " -w " + intf + ".pcap &"
        return self.cmd(cmd)


class RouterBase(IPNode):
    """Router Node"""

    def __init__(self, name, **params):
        super().__init__(name, **params)

    def config(self, **params):
        super(RouterBase, self).config(**params)
        enable_forwarding(self)
        set_arp_for_router(self)
        disable_rp(self)

    def terminate(self):
        disable_forwarding(self)
        super().terminate()


class SRv6Router(RouterBase):

    def config(self, **params):
        super(SRv6Router, self).config(**params)
        enable_srv6(self)


class FRR(SRv6Router):
    """FRR Node"""

    PrivateDirs = ["/etc/frr", "/etc/snmp", "/var/run/frr", "/var/log"]

    def __init__(self, name, inNamespace=True, enable_daemons=None,
                 daemons=None, vtysh_conf=None, frr_conf=None, frr_conf_content="", **params):
        """

        Args:
            name (str) : node name
            inNamespace (bool) : in Namespace
            enable_daemons (list) : daemons (ex. enable_daemons=["bgpd"])
            daemons (str) : daemos config template file name
            vtysh_conf (str) : vtysh config template file name
            frr_conf (str) : frr config template file name
            **params:
        """
        params.setdefault("privateDirs", [])
        params["privateDirs"].extend(self.PrivateDirs)
        super().__init__(name, inNamespace=inNamespace, **params)

        # config files
        self.daemons = daemons
        self.vtysh_conf = vtysh_conf
        self.frr_conf = frr_conf

        # frr conf content
        self.frr_conf_content = frr_conf_content

        # default daemons config
        self.daemons_param = {
            "zebra": "yes", "bgpd": "no", "ospfd": "no", "ospf6d": "no", "ripd": "no", "ripngd": "no", "isisd": "no",
            "pimd": "no", "ldpd": "no", "nhrpd": "no", "eigrpd": "no", "babeld": "no", "sharpd": "no", "staticd": "no",
            "pbrd": "no", "bfdd": "no", "fabricd": "no", "pathd": "no"
        }
        if isinstance(enable_daemons, list):
            if "*" in enable_daemons:
                for daemon in self.daemons_param.keys():
                    self.daemons_param[daemon] = "yes"
            else:
                for daemon in enable_daemons:
                    self.daemons_param[daemon] = "yes"

    def start_frr_service(self):
        """start FRR"""
        self.set_daemons()
        self.set_vtysh_conf()
        self.set_frr_conf()
        self.cmd("/usr/lib/frr/frrinit.sh start")

    def terminate(self):
        self.cmd("/usr/lib/frr/frrinit.sh stop")
        super().terminate()

    def set_daemons(self):
        """set daemons conf"""
        if self.daemons:
            self.render_conf_file("/etc/frr/daemons", self.daemons, self.daemons_param)
        else:
            self.render_conf("/etc/frr/daemons", Template(pkgutil.get_data(__name__, "conf/daemons.j2").decode()),
                             self.daemons_param)

    def set_vtysh_conf(self):
        """set vtysh conf"""
        if self.vtysh_conf:
            self.render_conf_file("/etc/frr/vtysh.conf", self.vtysh_conf, {"name": self.name})
        else:
            self.render_conf("/etc/frr/vtysh.conf", Template(pkgutil.get_data(__name__, "conf/vtysh.conf.j2").decode()),
                             {"name": self.name})

    def set_frr_conf(self):
        """set FRR conf"""
        if self.frr_conf:
            self.render_conf_file("/etc/frr/frr.conf", self.frr_conf, {"content": self.frr_conf_content})
        else:
            self.render_conf("/etc/frr/frr.conf", Template(pkgutil.get_data(__name__, "conf/frr.conf.j2").decode()),
                             {"content": self.frr_conf_content})

    def render_conf_file(self, file, template_file, params=None):
        """set file"""
        with open(template_file) as t:
            template = Template(t.read())
            self.render_conf(file, template, params)

    def render_conf(self, file, template, params=None) -> str:
        """render conf"""
        if params is None:
            params = {}
        rendered = template.render(**params)
        return self.cmd("cat << 'EOF' | tee {} \n".format(file) + rendered + "\n" + "EOF")

    def vtysh_cmd(self, cmd="", json_loads=False) -> str or dict:
        """exec vtysh commands"""
        cmds = cmd.split("\n")
        vtysh_cmd = "vtysh"
        for c in cmds:
            vtysh_cmd += " -c \"{}\"".format(c)
        if json_loads:
            return json.loads(self.cmd(vtysh_cmd))
        else:
            return self.cmd(vtysh_cmd)


class MPLSRouter(FRR):

    def config(self, **params):
        super().config(**params)
        enable_mpls(self)


class SimpleBGPRouter(FRR):
    """Simple BGP Router"""

    def __init__(self, name, inNamespace=True, as_number=None, router_id=None, bgp_networks=None, bgp_peers=None,
                 **params):
        super().__init__(name, inNamespace=inNamespace, enable_daemons=["bgpd"], frr_conf=None, **params)

        self.as_number = as_number
        self.router_id = router_id

        self.bgp_networks = bgp_networks if bgp_networks is not None else []
        self.bgp_peers = bgp_peers if bgp_peers is not None else []

    def start_frr_service(self):
        super().start_frr_service()
        self.cmd("ip addr add {} dev lo".format(self.router_id))

    def set_frr_conf(self, content=""):
        params = {
            "content": content,
            "router_id": self.router_id,
            "networks": self.bgp_networks,
            "as_number": self.as_number,
            "peers": self.bgp_peers
        }
        if self.frr_conf:
            self.render_conf_file("/etc/frr/frr.conf", self.frr_conf, params)
        else:
            self.render_conf("/etc/frr/frr.conf", Template(pkgutil.get_data(__name__, "conf/frr_bgp.conf.j2").decode()),
                             params)
