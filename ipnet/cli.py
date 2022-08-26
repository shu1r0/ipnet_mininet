from mininet.cli import CLI
from mininet.term import makeTerm


class CLIX(CLI):
    """CLI extension"""

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
