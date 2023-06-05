import pkgutil
from jinja2 import Template

from ipnet import FRR


def run_gobgpd(node, verbose=False):
    node.cmd("/usr/bin/gobgpd -f /etc/gobgpd/gobgpd.conf -d", verbose=verbose)
    node.cmd("/usr/bin/gobgpd -f /etc/gobgpd/gobgpd.conf --sdnotify --disable-stdlog --syslog yes &", verbose=verbose)


class FRRgoBGP(FRR):

    PrivateDirs = ["/etc/frr", "/etc/gobgpd" "/etc/snmp", "/var/run/frr", "/var/log"]
    GoBGPdConf = "/etc/gobgpd/gobgpd.conf"

    def __init__(self, *args, as_num=0, router_id="10.0.0.1", gobgpd_conf=None, **params):
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
        super().__init__(*args, **params)
        self.gobgpd_conf = gobgpd_conf
        self.gobgpd_conf_param = {
            "as_num": as_num,
            "router_id": router_id
        }

    def start_frr_service(self):
        super().start_frr_service()
        self.set_gobgpd()
        run_gobgpd(self)

    def set_gobgpd(self):
        if self.gobgpd_conf:
            self.render_conf_file(FRRgoBGP.GoBGPdConf, self.gobgpd_conf, self.gobgpd_conf_param)
        else:
            self.render_conf(FRRgoBGP.GoBGPdConf, Template(pkgutil.get_data(__name__, "gobgpd.conf").decode()),
                             self.gobgpd_conf_param)
