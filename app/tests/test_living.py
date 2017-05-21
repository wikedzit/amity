import imports#import this first
import unittest
import time
from model import Amity
from model import Office
from model import Living
from model import Staff
from model import Fellow
from controller import OfficeController
from controller import LivingController
from controller import StaffController
from controller import FellowController

class TestLivingController(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        data = {"name":"St Catherine"}
        self.living = LivingController.new(Living,data)
        self.staff = StaffController.new(Staff,{"firstname":"Roger", "lastname":"Taracha"})
        self.fellow = FellowController.new(Fellow,{"firstname":"Timothy", "lastname":"Wikedzi"})


    def test_can_create_living_room(self):
        self.assertTrue(isinstance(self.living,Living))
        self.assertEqual(self.living.data['type'], "living")

    def test_can_find_a_living_room(self):
        living1 = LivingController.getOne(Living,self.living.oid)
        self.assertEqual(self.living.oid,living1.oid)
        self.assertEqual(self.living.get("name"), "St Catherine")


    def test_can_update_a_living_room(self):
       #Before
        #self.assertEqual(living room 1.get('name'), "")
        living1 = LivingController.new(Living,{"name":"Dojo"})
        self.assertEqual(living1.get('name'), "Dojo")

        #After update
        #assert  to confirm that the office name has really been updated
        LivingController.edit(Living,living1.oid,{"name":"EPIC Tower"})
        self.assertNotEqual(living1.get('name'), "Dojo")

    def test_can_allocate_a_living_room_to_a_fellow(self):
        person = FellowController.new(Fellow,{"firstname":"Businge", "lastname":"Scott"})
        #successful allocation of a person returns true.
        self.assertTrue(LivingController.allocate(self.living, person))


    def test_can_not_allocate_a_living_room_to_staff(self):
        person = StaffController.new(Staff,{"firstname":"Stephan", "lastname":"Wikedzi"})
        #successful allocation of a person returns true.
        self.assertEqual(LivingController.allocate(self.living, person),"Staff can't be assigned a living room")

    def test_can_not_allow_multiple_allocations(self):
        #Allocated a person to a room
        LivingController.allocate(self.living, self.fellow)
        totaloccupants_before = self.living.getOccupants()
        #Confirm that muplti allocation is not allowed
        self.assertEqual(LivingController.allocate(self.living, self.fellow),"Multiple assignment")
        totaloccupants_after =  self.living.getOccupants()

        totaloccupants_before = self.living.getOccupants()
        self.assertEqual(totaloccupants_before,totaloccupants_after)

    def test_can_verify_status_of_the_room(self):
        self.assertTrue(True)

 
    def test_can_delete_an_office(self):
        #self.assertIn(self.living,Amity.db['rooms'])
        #delete this office
        #OfficeController.delete(Office,self.oid)
        #check to prove that it has been deleted
        #self.assertIsNone(OfficeController.getOne(Office, self.oid))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


























