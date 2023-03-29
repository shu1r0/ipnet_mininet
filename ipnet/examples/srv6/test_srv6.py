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
        self.net.get("r1").cmd("ip -6 route add fd00:2::1/128 encap seg6 mode inline segs fd00:a::2,fd00:d::2 dev r1_r2")
        self.net.get("r4").cmd("ip -6 route add fd00:1::1/128 encap seg6 mode inline segs fd00:e::1,fd00:b::1 dev r4_r3")

    def test_reachability(self):
        sleep(5)
        _, r = self.net.ping_to_ipv6(self.net.get("h1"), "fd00:2::1")
        self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()