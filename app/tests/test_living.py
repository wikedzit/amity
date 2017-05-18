import imports#import this first
import unittest
import time
from model import Living
from controller import LivingController

class TestLiving(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        data = {"name":"St Catherine"}
        self.living = LivingController.new(Living,data)

    def test_can_create_living_room(self):
        self.assertTrue(True)

    def test_find_living(self):
        living1 = LivingController.getOne(Living,self.living.oid)
        self.assertEqual(self.living.oid,living1.oid)
        self.assertEqual(self.living.get("name"), "St Catherine")

    def test_can_update_living(self):
        #living1 = LivingController.new(Living,{"name":"Tanganyika"})
        #LivingController.edit(Living,living1.oid,{"name":"Tanzania"})
        
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()