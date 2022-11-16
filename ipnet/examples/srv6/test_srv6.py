from time import sleep
from unittest import main, TestCase

from ipnet.examples.srv6 import srv6_vpn_10, simple_srv6_6


class Srv6_VPN_10Test(TestCase):

    def setUp(self) -> None:
        self.net = srv6_vpn_10.setup()

    def test_reachability(self):
        sleep(60)
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


class Simple_Srv6_6(TestCase):

    def setUp(self) -> None:
        self.net = simple_srv6_6.setup()

    def test_reachability(self):
        sleep(5)
        _, r = self.net.ping_to_ipv6(self.net.get("h1"), "fd00:2::1")
        self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()