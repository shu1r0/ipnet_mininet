from typing import Tuple
from mininet.net import Mininet
from mininet.node import Node, OVSBridge
from mininet.log import setLogLevel, info, output

from .node import RouterBase, SimpleBGPRouter, FRR, SRv6Router


class IPNetwork(Mininet):

    def __init__(self, **params):
        super().__init__(**params)
        self.frr_routers = []

    def addRouter(self, name, cls=RouterBase, **params) -> RouterBase:
        return self.addHost(name=name, cls=cls, **params)

    def addFRR(self, name, cls=FRR, **params) -> FRR:
        """add FRR"""
        r = self.addHost(name=name, cls=cls, **params)
        self.frr_routers.append(r)
        return r

    def addBGPRouter(self, name, as_number=None, router_id=None, bgp_networks=None, bgp_peers=None, **params) -> SimpleBGPRouter:
        r = self.addFRR(name=name, cls=SimpleBGPRouter, as_number=as_number, router_id=router_id, bgp_networks=bgp_networks,
                        bgp_peers=bgp_peers, **params)
        return r

    def addSRv6Router(self, name, cls=SRv6Router, **params) -> SRv6Router:
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
                         cls=RouterBase, ip_base="10.10.{subnet}.{node}/24"):
        info('*** Set MGMT Network:\n')
        ip_count = 1
        controller = self.addRouter(controller_name, cls=controller_cls, inNamespace=inNamespace)
        for name, node in self.nameToNode.items():
            if name != controller_name and isinstance(node, cls):
                self.addLink(node.name, controller,
                             intfName1="{}_{}".format(node.name, controller.name), params1={"ip": ip_base.format(subnet=ip_count, node=1)},
                             intfName2="{}_{}".format(controller.name, node.name), params2={"ip": ip_base.format(subnet=ip_count, node=2)})
                info("{}'s mgmt inteface ip address : {}\n".format(name, ip_base.format(subnet=ip_count, node=1)))
                ip_count += 1
        return controller

    def add_mgmt_l2network(self, controller_name, controller_cls=RouterBase, inNamespace=False,
                           cls=RouterBase, ip_base="10.10.0.{node}/24"):
        info('*** Set MGMT Network:\n')
        node_count = 1
        controller = self.addRouter(controller_name, cls=controller_cls, inNamespace=inNamespace)
        sw = self.addSwitch("s255", cls=OVSBridge)
        
        self.addLink(controller, sw,
                        intfName1="{}_{}".format(controller.name, sw.name), params1={"ip": ip_base.format(node=node_count)},
                        intfName2="{}_{}".format(sw.name, controller.name))
        node_count += 1
        
        for name, node in self.nameToNode.items():
            if name != controller_name and isinstance(node, cls):
                self.addLink(node.name, sw,
                             intfName1="{}_{}".format(node.name, sw.name), params1={"ip": ip_base.format(node=node_count)},
                             intfName2="{}_{}".format(sw.name, node.name))
                info("{}'s mgmt inteface ip address : {}\n".format(name, ip_base.format(node=node_count)))
                node_count += 1
        return controller

    def get_nodes_by_cls(self, cls=Node):
        return [n for n in self.nameToNode.values() if isinstance(n, cls)]

    def cmd_nodes(self, cmd, cls=None):
        for n in self.nameToNode.values():
            if cls is None or isinstance(n, cls):
                n.cmd(cmd)

    def cmd_print_nodes(self, cmd, cls=None):
        for n in self.nameToNode.values():
            if cls is None or isinstance(n, cls):
                n.cmdPrint(cmd)
    
    @classmethod
    def ping_to_ip(cls, node: Node, dst_ip: str, times=1, timeout=None) -> Tuple[int, int]:
        """simple ping"""
        cmd = 'LANG=C ping -c {} {}'.format(times, dst_ip)
        cmd += " -W {}".format(timeout) if timeout is not None else ""
        result = node.cmd(cmd)
        sent, received = cls._parsePing(result)
        output("ping %s -> %s (sent: %s, received: %s, dropped: %s) \n" % (str(node), dst_ip, sent, received, sent - received))
        return sent, received

    @classmethod
    def ping_to_ipv6(cls, node: Node, dst_ipv6: str, times=1, timeout=None) -> Tuple[int, int]:
        """simple ping -6"""
        cmd = 'LANG=C ping -6 -c {} {}'.format(times, dst_ip)
        cmd += " -W {}".format(timeout) if timeout is not None else ""
        result = node.cmd(cmd)
        sent, received = cls._parsePing(result)
        output("ping %s -> %s (sent: %s, received: %s, dropped: %s) \n" % (str(node), dst_ipv6, sent, received, sent - received))
        return sent, received
