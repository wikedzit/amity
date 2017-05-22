import imports#import this first
import unittest
import time
from model import Amity
from model import People
from model import Office
from model import Staff
from model import Fellow
from model import Living
from controller import OfficeController
from controller import StaffController
from controller import FellowController
from controller import LivingController
from controller import RoomController

class TestRoom(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        self.office = OfficeController.new(Office,{"name":"Tsavo"})
        self.living = LivingController.new(Living,{"name":"Dojo"})
        self.staff = StaffController.new(Staff,{"firstname":"Roger", "lastname":"Taracha"})
        self.fellow = FellowController.new(Fellow,{"firstname":"Timothy", "lastname":"Wikedzi"})

    def test_office_is_created(self):
        office1 = OfficeController.new(Office,{"name":"People and Calture"})
        offices = Office.getRooms()
        self.assertIn(office1,offices)

    def test_living_space_is_created(self):
        living1 = LivingController.new(Living,{"name":"Safari Hotel"})
        living_rooms = Living.getRooms()
        self.assertIn(living1,living_rooms)  

    def test_can_find_an_room(self):
        #Finding an office(This same procedure works for a living space)
        office1 = OfficeController.getOne(Office,self.office.oid)
        self.assertEqual(self.office.oid,office1.oid)

    def test_can_update_details_of_an_office(self):
        office1 = OfficeController.new(Office,{"name":"Tanganyika"})
        OfficeController.edit(Office,office1.oid,{"name":"Kenya"})
        self.assertEqual(office1.get('name'), "Kenya")

    def test_can_update_details_of_a_living_room(self):
        living1 = LivingController.new(Living,{"name":"Dojo"})
        room_name_before = living1.get('name')
        LivingController.edit(Living,living1.oid,{"name":"St Catherine"})
        room_name_after  = living1.get('name')
        self.assertNotEqual(room_name_after, room_name_before)


    def test_can_allocate_an_office_to_a_staff(self):
        #The allocate emthod takes in two arguments an office and a person
        OfficeController.allocate(self.office, self.staff)
        #confirm that a staff is really in that office
        self.assertIn(self.staff.oid,self.office.getOccupants())

    def test_can_allocate_an_office_to_a_fellow(self):
        OfficeController.allocate(self.office, self.fellow)
        #confirm that a staff is really in that office
        self.assertIn(self.fellow.oid,self.office.getOccupants())


    def test_staff_and_fellow_can_share_an_office(self):
        hatari = OfficeController.new(Office,{"name":"Chapa Kazi"})
        staffx = StaffController.new(Staff,{"firstname":"Jimmy", "lastname":"Kimani"})
        fellowx = FellowController.new(Fellow,{"firstname":"Joseph", "lastname":"Ngugi"})

        OfficeController.allocate(hatari, staffx)
        OfficeController.allocate(hatari, fellowx)
        #confirm that a staff is really in that office

        staff_n_fellow = [staffx.oid,fellowx.oid]
        self.assertEqual(staff_n_fellow.sort(),hatari.getOccupants().sort())

    def test_can_not_allow_multiple_allocations(self):
        #Allocated a person to a room
        OfficeController.allocate(self.office, self.fellow)
        totaloccupants_before = self.office.getOccupants()
        #Confirm that multi allocation is not allowed
        self.assertEqual(OfficeController.allocate(self.office, self.fellow),"Multiple assignment")
        totaloccupants_after =  self.office.getOccupants()

        totaloccupants_before = self.office.getOccupants()
        self.assertEqual(totaloccupants_before,totaloccupants_after)


    def test_can_reallocated_a_person_to_a_different_office(self):
        #person = StaffController.new(Staff,{"firstname":"Genn", "lastname":"Wikedzi"})
        OfficeController.allocate(self.office, self.staff)
        #confirm if this person was really added to the office
        self.assertTrue(self.office.hasOccupant(self.staff))

        office2 = OfficeController.new(Office,{"name":"Finance"})
        OfficeController.reallocate(office2,self.staff)
        self.assertFalse(self.office.hasOccupant(self.staff))
        self.assertTrue(office2.hasOccupant(self.staff))

    def test_can_not_allocate_a_living_room_to_staff(self):
        person = StaffController.new(Staff,{"firstname":"Stephan", "lastname":"Wikedzi"})
        #successful allocation of a person returns true.
        self.assertEqual(LivingController.allocate(self.living, person),"Staff can't be assigned a living room")


    def test_can_verify_status_of_the_room_before_adding_occupants(self):
        #create a dummy office of size 2
        living3 = LivingController.new(Office,{"name":"St Catherine TRM", "capacity":2})

        #create two members of this room
        f1= FellowController.new(Fellow,{"firstname":"David", "lastname":"Mujibi"})
        f2= FellowController.new(Fellow,{"firstname":"Businge", "lastname":"Scott"})

        #Allocate the two fellows to their living room
        LivingController.allocate(living3,f1)
        LivingController.allocate(living3,f2)
       
       #create a third person
        f3= FellowController.new(Fellow,{"firstname":"Jackson", "lastname":"Onyango"})
        self.assertEqual(OfficeController.allocate(living3,f3),"Room is full. This person is placed in a waiting list")

    def test_can_validate_imported_data(self):
        data = [["Dojo","living"], ["Narnia","office","6" ],["Hogwart"]]
        response = RoomController.importRooms(data)
        self.assertEqual(response,"Data is not properly formated")
        #self.assertTrue(True)

    def test_can_delete_a_room(self):
        offices = Office.all()
        self.assertIn(self.office,offices)
        #delete this office
        
        OfficeController.delete(Office,self.office.oid)
        #check to prove that it has been deleted
        offices = Office.all()
        self.assertNotIn(self.office,offices)
        #self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()


























