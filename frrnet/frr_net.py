import pkgutil
from jinja2 import Template

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import Node
from mininet.term import makeTerm


class FRR(Node):
    """FRR Node"""

    PrivateDirs = ["/etc/frr", "/var/run/frr"]

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
        super().__init__(name, inNamespace, **params)

        # config files
        self.daemons = daemons 
        self.vtysh_conf =  vtysh_conf 
        self.frr_conf =  frr_conf
        
        # frr conf content
        self.frr_conf_content = frr_conf_content

        # default daemons config
        self.daemons_param = {
            "zebra": "yes", "bgpd": "no", "ospfd": "no", "ospf6d": "no", "ripd": "no", "ripngd": "no", "isisd": "no",
            "pimd": "no", "ldpd": "no", "nhrpd": "no", "eigrpd": "no", "babeld": "no", "sharpd": "no", "staticd": "no",
            "pbrd": "no", "bfdd": "no", "fabricd": "no"
        }
        if isinstance(enable_daemons, list):
            for daemon in enable_daemons:
                self.daemons_param[daemon] = "yes"

    def start_frr_service(self):
        """start FRR"""
        self.cmd("sysctl net.ipv4.ip_forward=1")

        self.set_daemons()
        self.set_vtysh_conf()
        self.set_frr_conf()
        self.cmd("/usr/lib/frr/frrinit.sh start")

    def terminate(self):
        super(FRR, self).terminate()
        self.cmd("sysctl net.ipv4.ip_forward=0")

    def set_daemons(self):
        """set daemons conf"""
        if self.daemons:
            self.render_conf_file("/etc/frr/daemons", self.daemons, self.daemons_param)
        else:
            self.render_conf("/etc/frr/daemons", Template(pkgutil.get_data(__name__, "conf/daemons.j2").decode()), self.daemons_param)

    def set_vtysh_conf(self):
        """set vtysh conf"""
        if self.vtysh_conf:
            self.render_conf_file("/etc/frr/vtysh.conf", self.vtysh_conf, {"name": self.name})
        else:
            self.render_conf("/etc/frr/vtysh.conf", Template(pkgutil.get_data(__name__, "conf/vtysh.conf.j2").decode()), {"name": self.name})

    def set_frr_conf(self):
        """set FRR conf"""
        if self.frr_conf:
            self.render_conf_file("/etc/frr/frr.conf", self.frr_conf, {"content": self.frr_conf_content})
        else:
            self.render_conf("/etc/frr/frr.conf",  Template(pkgutil.get_data(__name__, "conf/frr.conf.j2").decode()), {"content": self.frr_conf_content})

    def render_conf_file(self, file, template_file, params=None):
        """set file"""
        template = None
        with open(template_file) as t:
            template = Template(t.read())
        self.render_conf(file, template, params)

    def render_conf(self, file, template, params=None):
        """render conf"""
        if params is None:
            params = {}
        rendered = template.render(**params)
        self.cmd( """\
cat << 'EOF' | tee {}
{}
EOF""".format(file, rendered))

    def vtysh_cmd(self, cmd=""):
        """exec vtysh commands"""
        cmds = cmd.split("\n")
        vtysh_cmd = "vtysh"
        for c in cmds:
            vtysh_cmd += " -c \"{}\"".format(c)
        return self.cmd(vtysh_cmd)
    
    def tcpdump(self, intf):
        cmd = "tcppdump -i " + intf + " -w " + intf + ".pcap &"
        return self.cmd(cmd)


class BGPRouter(FRR):
    """Simple BGP Router"""

    def __init__(self, name, inNamespace=True, as_number=None, router_id=None, bgp_networks=None, bgp_peers=None, **params):
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
            self.render_conf("/etc/frr/frr.conf", Template(pkgutil.get_data(__name__, "conf/frr_bgp.conf.j2").decode()), params)


class FRRNetwork(Mininet):

    def __init__(self, **params):
        super().__init__(**params)
        self.frr_routers = []

    def addFRR(self, name, cls=FRR, **params):
        """add FRR"""
        params["ip"] = None
        r = self.addHost(name=name, cls=cls, **params)
        self.frr_routers.append(r)
        return r

    def addBGPRouter(self, name, as_number=None, router_id=None, bgp_networks=None, bgp_peers=None, **params):
        r = self.addFRR(name=name, cls=BGPRouter, as_number=as_number, router_id=router_id, bgp_networks=bgp_networks,
                        bgp_peers=bgp_peers, **params)
        return r

    def start(self):
        """start mininet and FRR"""
        super().start()
        info('*** Start FRR service:\n')
        for r in self.frr_routers:
            r.start_frr_service()
            info(r.name + " ")
        info("\n")


class CLIWithVtysh(CLI):
    """CLI for VTYSH"""

    def do_vtysh(self, line):
        """start vtysh

        Examples:
            mininet> vtysh r1 r2 r3
        """
        args = line.split()
        for a in args:
            if a in [r.name for r in self.mn.frr_routers]:
                term = makeTerm(self.mn[a], cmd="vtysh")
                self.mn.terms += term


def main():
    setLogLevel("info")
    net = FRRNetwork()

    h1 = net.addHost("h1")
    r1 = net.addFRR("r1", enable_daemons=["bgpd", "staticd"])
    r2 = net.addFRR("r2", enable_daemons=["bgpd", "staticd"])
    h2 = net.addHost("h2")

    net.addLink(h1, r1)
    net.addLink(r1, r2)
    net.addLink(r2, h2)

    net.start()
    CLIWithVtysh(net)
    net.stop()


if __name__ == '__main__':
    main()

