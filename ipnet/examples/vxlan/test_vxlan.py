from time import sleep
from unittest import main, TestCase

from ipnet.examples.vxlan import vxlan_uni_3, vxlan_multi_7


class VXLAN_Uni_3Test(TestCase):
    
    def setUp(self) -> None:
        self.net = vxlan_uni_3.setup()
    
    def test_reachability(self):
        sleep(1)
        _, r = self.net.ping_to_ip(self.net.get("h1"), "172.16.10.2")
        self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


class VXLAN_MULTI_7Test(TestCase):

    def setUp(self) -> None:
        self.net = vxlan_multi_7.setup()

    def test_reachability(self):
        sleep(1)
        _, r = self.net.ping_to_ip(self.net.get("h1"), "10.200.1.2")
        self.assertEqual(True, r == 0)
        _, r = self.net.ping_to_ip(self.net.get("h1"), "10.100.2.2")
        self.assertEqual(True, r > 0)
        _, r = self.net.ping_to_ip(self.net.get("h1"), "10.200.2.2")
        self.assertEqual(True, r == 0)
        
        _, r = self.net.ping_to_ip(self.net.get("h2"), "10.100.1.2")
        self.assertEqual(True, r == 0)
        _, r = self.net.ping_to_ip(self.net.get("h2"), "10.100.2.2")
        self.assertEqual(True, r == 0)
        _, r = self.net.ping_to_ip(self.net.get("h2"), "10.200.2.2")
        self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()