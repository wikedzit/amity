import imports#import this first
import unittest
import time

from amity import Amity
from model import People,Office,Staff,Fellow
from controller import OfficeController, StaffController, FellowController, PeopleController


class TestPerson(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        self.staff = StaffController.new(Staff,{"firstname":"James", "lastname":"Ndiga"})
        self.fellow = FellowController.new(Fellow,{"firstname":"Timothy", "lastname":"Wikedzi"})
   
    def test_person_is_created(self):
        fellow1 = FellowController.new(Fellow,{"firstname":"Akia", "lastname":"Mwanga"})
        all_fellows = Fellow.all("names")
        self.assertIn(fellow1.name(),all_fellows)

    def test_can_verify_names(self):
        data = {"firstname": "221Jimmy","lastname":"Kimani"}
        self.assertEqual(StaffController.new(Staff,data),"Invalid Input")

    def test_can_find_a_person(self):
        staff1 = StaffController.getOne(Staff,self.staff.name())
        self.assertEqual(self.staff,staff1)
        self.assertEqual(staff1.get("firstname"), "James")

    ##########separate the tests to include both tests for loding the file and validate thedata
    def test_can_validate_imported_data(self):
        data = [["Timothy","Wikedzi"], ["Dayse","Machari","FELLOW","Y" ]]
        response = PeopleController.importPeople(data)
        self.assertEqual(response,"Data is not properly formated")
        #self.assertTrue(True)


    def test_can_delete_a_person(self):
        fellow1 = FellowController.new(Fellow,{"firstname":"Ayoub", "lastname":"Mugube"})
        andelans_before = Fellow.all()
        self.assertIn(fellow1,andelans_before)
        
        #delete this person
        FellowController.delete(fellow1)
        #check to prove that it has been deleted
        andelans_after = Fellow.all()
        self.assertNotIn(fellow1,andelans_after)

    def tearDown(self):
        self.staff.delete()
        self.fellow.delete()

if __name__ == '__main__':
    unittest.main()


























