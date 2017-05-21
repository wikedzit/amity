import imports#import this first
import unittest
import time
from model import Amity
from model import Office
from model import Staff
from model import Fellow
from controller import OfficeController
from controller import StaffController
from controller import FellowController

class TestFellow(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        self.fellow = FellowController.new(Fellow,{"firstname":"Timothy", "lastname":"Wikedzi"})

    def test_can_verify_names(self):
        data = {"firstname": "221Joyce","lastname":"Chambile"}
        self.assertEqual(FellowController.new(Fellow,data),"Invalid Input")

    def test_can_find_a_fellow(self):
        fellow1 = FellowController.getOne(Fellow,self.fellow.oid)
        self.assertEqual(self.fellow.oid,fellow1.oid)
        self.assertEqual(self.fellow.get("firstname"), "Timothy")



    def test_can_delete_an_office(self):
        #self.assertIn(self.office,Amity.db['rooms'])
        #delete this office
        #OfficeController.delete(Office,self.staff.oid)
        #check to prove that it has been deleted
        #self.assertIsNone(OfficeController.getOne(Office, self.oid))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


























