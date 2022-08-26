from mininet.net import Mininet
from mininet.log import setLogLevel, info

from .node import RouterBase, SimpleBGPRouter, FRR, SRv6Node


class IPNetwork(Mininet):

    def __init__(self, **params):
        super().__init__(**params)
        self.frr_routers = []

    def addRouter(self, name, cls=RouterBase, **params) -> RouterBase:
        return self.addHost(name=name, cls=cls, **params)

    def addFRR(self, name, cls=FRR, **params) -> FRR:
        """add FRR"""
        params["ip"] = None
        r = self.addHost(name=name, cls=cls, **params)
        self.frr_routers.append(r)
        return r

    def addBGPRouter(self, name, as_number=None, router_id=None, bgp_networks=None, bgp_peers=None, **params) -> SimpleBGPRouter:
        r = self.addFRR(name=name, cls=SimpleBGPRouter, as_number=as_number, router_id=router_id, bgp_networks=bgp_networks,
                        bgp_peers=bgp_peers, **params)
        return r

    def addSRv6Node(self, name, cls=SRv6Node, **params) -> SRv6Node:
        return self.addFRR(name, cls=cls, **params)

    def start(self):
        """start mininet and FRR"""
        super().start()
        info('*** Start FRR service:\n')
        for r in self.frr_routers:
            r.start_frr_service()
            info(r.name + " ")
        info("\n")

    def add_mgmt_network(self, controller_name, controller_cls=RouterBase, inNamespace=False,
                         cls=RouterBase, ip_base="10.10.{}.{}/24"):
        ip_count = 1
        controller = self.addRouter(controller_name, cls=controller_cls, inNamespace=inNamespace)
        for name, node in self.nameToNode.items():
            if name != controller_name and isinstance(node, cls):
                self.addLink(node.name, controller,
                             intfName1="{}_{}".format(node.name, controller.name), params1={"ip": ip_base.format(ip_count, 1)},
                             intfName2="{}_{}".format(controller.name, node.name), params2={"ip": ip_base.format(ip_count, 2)})
                ip_count += 1
        return controller

    def cmd_nodes(self, cmd, cls=None):
        for n in self.nameToNode.values():
            if cls is None or isinstance(n, cls):
                n.cmd(cmd)

    def cmd_print_nodes(self, cmd, cls=None):
        for n in self.nameToNode.values():
            if cls is None or isinstance(n, cls):
                n.cmdPrint(cmd)
