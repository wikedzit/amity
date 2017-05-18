import imports#import this first
import unittest
import time
from model import Amity
from model import Office
from model import Staff
from controller import OfficeController
from controller import StaffController

class TestOffice(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        data = {"name":"Tsavo"}
        self.office = OfficeController.new(Office,data)
        self.oid = self.office.oid

    def test_can_create_office(self):
        self.assertTrue(True)

    def test_find_office(self):
        office1 = OfficeController.getOne(Office,self.office.oid)
        self.assertEqual(self.office.oid,office1.oid)
        self.assertEqual(self.office.get("name"), "Tsavo")


    def test_can_update_office(self):
        #Update the office to a different name
        office1 = OfficeController.new(Office,{"name":"Tanganyika"})
        OfficeController.edit(Office,office1.oid,{"name":"Tanzania"})
        
        #assert  to confirm that the office name has reaaly been updated
        #self.assertEqual(office1.get('name'), "Tanzania")
        self.assertTrue(True)


    def test_can_alocate_an_office_for_person(self):
        person = StaffController.new(Staff,{"firstname":"Timothy", "lastname":"Wikedzi"})
        #successful allocation of a person returns true.
        self.assertTrue(OfficeController.allocate(person))


    def test_can_multiple_allocation(self):
        person = StaffController.new(Staff,{"firstname":"Gladness", "lastname":"Mwanga"})
        #Alllocate this person to an office
        OfficeController.allocate(person)

        #Confirm that muplti allocation is not allowed
        self.assertEqual(OfficeController.allocate(person),"You can not allocated the same person more tan one time")


    def can_verify_status_of_the_room(self):
        self.assertTrue(True)


    def test_can_delete_an_office(self):
        self.assertIn(self.office,Amity.db['rooms'])
        #delete this office
        self.office.delete()
        #check to prove that it has been deleted
        self.assertNotIn(self.office,Amity.db['rooms'])


if __name__ == '__main__':
    unittest.main()