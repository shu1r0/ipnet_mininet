from time import sleep
from unittest import main, TestCase

from ipnet.examples.clos import clos2_30, clos3_40


class Clos3_40Test(TestCase):
    
    def setUp(self) -> None:
        self.net = clos3_40.setup()
    
    def test_reachability(self):
        sleep(30)
        for h_i in range(1, 17):
            h = "h{}".format(h_i)
            for h_j in range(h_i, 17):
                _, r = self.net.ping_to_ipv6(self.net.get(h), "fd00:{}::2".format(h_j))
                self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


class Clos2_30Test(TestCase):

    def setUp(self) -> None:
        self.net = clos2_30.setup()

    def test_reachability(self):
        sleep(30)

        for h_i in range(1, 9):
            h = "h{}".format(h_i)
            for h_j in range(h_i, 9):
                _, r = self.net.ping_to_ip(self.net.get(h), "192.168.{}.2".format(h_j))
                self.assertEqual(True, r > 0)
                _, r = self.net.ping_to_ipv6(self.net.get(h), "fd00:{}::2".format(h_j))
                self.assertEqual(True, r > 0)
                # to nat
                _, r = self.net.ping_to_ip(self.net.get(h), "192.168.100.1")
                self.assertEqual(True, r > 0)
                _, r = self.net.ping_to_ip(self.net.get(h), "192.168.200.1")
                self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()