from time import sleep
from unittest import main, TestCase

from . import srv6_vpn_10


class Srv6_VPN_10Test(TestCase):

    def setUp(self) -> None:
        self.net = srv6_vpn_10.setup()

    def test_reachability(self):
        sleep(50)
        _, r = self.net.ping_to_ipv6(self.net.get("h1"), "fd00:2::2")
        self.assertEqual(True, r == 0)
        _, r = self.net.ping_to_ipv6(self.net.get("h1"), "fd00:3::2")
        self.assertEqual(True, r > 0)
        _, r = self.net.ping_to_ipv6(self.net.get("h2"), "fd00:3::2")
        self.assertEqual(True, r == 0)
        _, r = self.net.ping_to_ipv6(self.net.get("h2"), "fd00:4::2")
        self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()