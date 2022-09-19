from time import sleep
from unittest import main, TestCase

from . import sr_mpls_10, sr_mpls_isis_12


class SR_MPLS_10Test(TestCase):

    def setUp(self) -> None:
        self.net = sr_mpls_10.setup()

    def test_reachability(self):
        sleep(50)
        for h_i in range(1, 5):
            h = "h{}".format(h_i)
            for h_j in range(h_i, 5):
                _, r = self.net.ping_to_ip(self.net.get(h), "192.168.{}.2".format(h_j))
                self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


class SR_MPLS_ISIS_12Test(TestCase):

    def setUp(self) -> None:
        self.net = sr_mpls_isis_12.setup()

    def test_reachability(self):
        sleep(50)
        for h_i in range(1, 5):
            _, r = self.net.ping_to_ip(self.net.get("h1"), "192.168.{}.2".format(h_i))
            self.assertEqual(True, r > 0)

    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()