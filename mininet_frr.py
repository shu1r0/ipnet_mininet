from jinja2 import Environment, FileSystemLoader

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import Node
from mininet.term import makeTerm


class FRR(Node):

    PrivateDirs = ["/etc/frr", "/var/run/frr"]

    def __init__(self, name, inNamespace=True, enable_daemons=None, **params):
        """
        Args:
            name: node name
            inNamespace: in Namespace ??
            enable_daemons: daemons (ex. enable_daemons={"bgpd": "yes"})
            **params:
        """
        params.setdefault("privateDirs", [])
        params["privateDirs"].extend(BGPRouter.PrivateDirs)
        super().__init__(name, inNamespace, **params)

        self.template_dir = params.get("template_dir", "./conf/")
        self.daemons = params.get("daemons", "daemons.j2")
        self.vtysh_conf = params.get("vtysh_conf", "vtysh.conf.j2")
        self.frr_conf = params.get("frr_conf", None)

        # default daemons config
        self.daemons_param = {
            "zebra": "no", "bgpd": "no", "ospfd": "no", "ospf6d": "no", "ripd": "no", "ripngd": "no", "isisd": "no",
            "pimd": "no", "ldpd": "no", "nhrpd": "no", "eigrpd": "no", "babeld": "no", "sharpd": "no", "staticd": "no",
            "pbrd": "no", "bfdd": "no", "fabricd": "no"
        }
        if enable_daemons:
            self.daemons_param.update(enable_daemons)

    def start_frr_service(self):
        """start FRR"""
        self.set_daemons()
        self.set_vtysh_conf()
        self.set_frr_conf()
        self.cmd("/usr/lib/frr/frrinit.sh start")

    def set_daemons(self):
        """set daemons conf"""
        self.render_conf_file("/etc/frr/daemons", self.daemons, self.daemons_param)

    def set_vtysh_conf(self):
        """set vtysh conf"""
        self.render_conf_file("/etc/frr/vtysh.conf", self.vtysh_conf, {"name": self.name})

    def set_frr_conf(self):
        """set FRR conf"""
        if self.frr_conf:
            self.render_conf_file("/etc/frr/frr.conf", self.frr_conf)

    def render_conf_file(self, file, template_file, params=None):
        """set file"""
        env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True
        )
        template = env.get_template(template_file)
        if params is None:
            params = {}
        rendered = template.render(**params)
        with open(self.template_dir + "tmp_conf", 'w') as f:
            f.write(rendered)
        self.cmd("cp {}tmp_conf {}".format(self.template_dir, file))


class BGPRouter(FRR):

    def __init__(self, name, inNamespace=True, as_number=None, router_id=None, bgp_network=None, **params):
        super().__init__(name, inNamespace=inNamespace, enable_daemons={"bgpd": "yes"}, frr_conf="frr_bgp.conf.j2", **params)

        self.as_number = as_number
        self.router_id = router_id
        self.bgp_network = bgp_network

    def set_frr_conf(self):
        params = {
            "router_id": self.router_id,
            "network": self.bgp_network,
            "as_number": self.as_number
        }
        self.render_conf_file("/etc/frr/frr.conf", self.frr_conf, params)


class FRRNetwork(Mininet):

    def __init__(self, **params):
        super().__init__(params)
        self.frr_routers = []

    def addFRR(self, name, cls=FRR, **params):
        params["ip"] = None
        r = self.addHost(name=name, cls=cls, **params)
        self.frr_routers.append(r)
        return r

    def addBGPRouter(self, name, as_number=None, router_id=None, bgp_network=None, **params):
        r = self.addFRR(name=name, cls=BGPRouter, as_number=as_number, router_id=router_id, bgp_network=bgp_network, **params)
        self.frr_routers.append(r)
        return r


    def start(self):
        """start mininet and FRR"""
        super().start()
        for r in self.frr_routers:
            r.start_frr_service()


class CLI_WITH_VTYSH(CLI):
    """CLI for VTYSH"""

    def do_vtysh(self, line):
        """start vtysh"""
        args = line.split()
        for a in args:
            if a in [r.name for r in self.mn.frr_routers]:
                term = makeTerm(self.mn[a], cmd="vtysh")
                self.mn.terms += term


def main():
    setLogLevel("info")
    net = FRRNetwork()

    h1 = net.addHost("h1")
    r1 = net.addFRR("r1", enable_daemons={"bgpd": "yes"})
    r2 = net.addFRR("r2", enable_daemons={"bgpd": "yes"})
    h2 = net.addHost("h2")

    net.addLink(h1, r1)
    net.addLink(r1, r2)
    net.addLink(r2, h2)

    net.start()
    CLI_WITH_VTYSH(net)
    net.stop()


if __name__ == '__main__':
    main()

