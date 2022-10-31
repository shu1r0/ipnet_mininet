from mininet.log import info, output, error
from mininet.cli import CLI
from mininet.term import makeTerm, tunnelX11


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

    def do_xtermfs(self, line):
        """do xtrem specific fontsize

        Args:
            line (str): args
            
        References:
            * https://github.com/mininet/mininet/blob/3f5503d7737a0f07eafce03594cf9ed5112e5ae8/mininet/term.py#L38
        """
        fs = line.split()[0]
        args = line.split()[1:]
        if len(args) <= 0:
            error('usage: xtermfs <fontsize> <node1> <node2> ...\n')
        for a in args:
            if a in self.mn:
                node = self.mn[a]
                display, tunnel = tunnelX11(node)
                cmd =  ['xterm', "-fa", "Monospace", "-fs", fs, '-title', '"%s: %s"' % ("Node", node.name ), '-display', display, "-e", "env TERM=ansi bash"]
                term = node.popen(cmd)
                self.mn.terms += [tunnel, term] if tunnel else [term]
