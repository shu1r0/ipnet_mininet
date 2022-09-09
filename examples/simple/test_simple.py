from time import sleep
from unittest import main, TestCase

from . import simple_2, simple_mgmt_3


class Simple_2Test(TestCase):
    
    def setUp(self) -> None:
        self.net = simple_2.setup()
    
    def test_reachability(self):
        sleep(50)
        _, r = self.net.ping_to_ip(self.net.get("r1"), "192.168.1.2")
        self.assertEqual(True, r > 0)
        _, r = self.net.ping_to_ip(self.net.get("r1"), "2.2.2.2")
        self.assertEqual(True, r > 0)
    
    def tearDown(self):
        self.net.stop()

    
class Simple_Mgmt_3Test(TestCase):
    
    def setUp(self) -> None:
        self.net = simple_mgmt_3.setup()
    
    def test_reachability(self):
        sleep(50)
        _, r = self.net.ping_to_ip(self.net.get("r1"), "192.168.1.2")
        self.assertEqual(True, r > 0)
        _, r = self.net.ping_to_ip(self.net.get("r1"), "2.2.2.2")
        self.assertEqual(True, r > 0)
        
        _, r = self.net.ping_to_ip(self.net.get("r1"), "10.20.1.2")
        self.assertEqual(True, r > 0)
        _, r = self.net.ping_to_ip(self.net.get("r2"), "10.20.2.2")
        self.assertEqual(True, r > 0)
    
    def tearDown(self):
        self.net.stop()


if __name__ == "__main__":
    main()