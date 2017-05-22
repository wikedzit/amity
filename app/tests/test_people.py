import imports#import this first
import unittest
import time

from model import Amity,People,Office,Staff,Fellow
from controller import OfficeController, StaffController, FellowController, PeopleController


class TestStaff(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        self.staff = StaffController.new(Staff,{"firstname":"James", "lastname":"Ndiga"})
        self.fellow = FellowController.new(Fellow,{"firstname":"Timothy", "lastname":"Wikedzi"})
   
    def test_person_is_created(self):
        fellow1 = FellowController.new(Fellow,{"firstname":"Akia", "lastname":"Mwanga"})
        all_people = People.all()
        self.assertIn(fellow1,all_people)

    def test_can_verify_names(self):
        data = {"firstname": "221Jimmy","lastname":"Kimani"}
        self.assertEqual(StaffController.new(Staff,data),"Invalid Input")

    def test_can_find_a_person(self):
        staff1 = StaffController.getOne(Staff,self.staff.oid)
        self.assertEqual(self.staff.oid,staff1.oid)
        self.assertEqual(self.staff.get("firstname"), "James")


    ##########separate the tests to include both tests for loding the file and validate thedata
    def test_can_validate_imported_data(self):
        data = [["Timothy","Wikedzi"], ["Dayse","Machari","FELLOW","Y" ]]
        response = PeopleController.importPeople(data)
        self.assertEqual(response,"Data is not properly formated")
        #self.assertTrue(True)


    def test_can_delete_a_person(self):
        andelans_before = PeopleController.getAll(People)
        self.assertIn(self.fellow,andelans_before)
        
        #delete this person
        FellowController.delete(Fellow,self.fellow.oid)
        #check to prove that it has been deleted
        andelans_after = PeopleController.getAll(People)
        self.assertNotIn(self.fellow,andelans_after)


if __name__ == '__main__':
    unittest.main()


























