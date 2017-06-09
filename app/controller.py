import time
import re

from amity import Amity
from model import Room,Office,Living ,People,Staff, Fellow


class Controller(object):

    @classmethod
    def new(cls,model_cls,data={}): 
        validators = model_cls.validators
        #validate inputs
        for key, value in validators.items():
            p = re.compile(value)
            if key in data and (not p.match(data[key])):
                return "Invalid Input" 
        #check if record exists
        if model_cls.find(data):
            return "Duplicated record"

        obj = model_cls(data)
        return obj.save()

    @classmethod
    def edit(cls,obj,dt):
        try:
            obj.setData(dt)
        except Exception as e:
            return False
        else:
            return True

    @classmethod
    def getOne(cls,model_cls,fltr={}):
        return model_cls.find(fltr)

    @classmethod
    def delete(cls,obj):
        obj1 = obj.__class__.find(obj.data)
        if not obj1 is None:
            obj.delete()
            # Call thi method to cascade person delete on rooms allocations
            if isinstance(obj1,People):
                RoomController.clean()
            return True
        return False

#-----------------------------------------------
class RoomController(Controller):

    def __init__(self):
        super(RoomController, self).__init__()


    @classmethod
    def allocate(cls,room,person):
        if person.typeIs('staff') and room.typeIs('living'):
            return "Staff can't be assigned a living room"

        if room.hasOccupant(person):
               return "Multiple assignments"

        if len(room.getOccupants()) < int(room.get('capacity')):
            occupant = {"firstname":person.get("firstname"),";lastname":person.get("lastname")}
            room.data['allocations'].append(occupant)#Add person to a list
            return "Room allocation was successful"
        else:
            #Amity.db["unallocated"].append([person.oid,"living"])
            return "Room is full. This person is placed in a waiting list"


    @classmethod
    def reallocate(cls,room,person):
        if len(room.getOccupants()) < int(room.get('capacity')):
            prev_room = cls.personRoom(room.get('type'), person)
            if prev_room:#This means that this person was placed in this room
                if prev_room.get("type") == room.get("type"):
                    #delete any previous placements
                    indx = prev_room.getOccupants().index(person.name())
                    del prev_room.data["allocations"][indx]
                    #call for new reallocations after deleting
                return "Room reallocation can only be done between rooms of the same type"
            return RoomController.allocate(room,person) + " (Reallocation)"
        else:
            return "This room is full. can't reallocate this person, "

    @classmethod
    def clean(cls):
        rooms = Room.getAllRooms()
        for room in rooms:
            allocations = room.getOccupants()
            if len(allocations) > 0 :
                for name  in allocations:
                    person = Staff.find(name)
                    if person is None:
                        person = Fellow.find(name)
                    if not person is None:
                        p_index = allocations.index(name)
                        del room.data['allocations'][p_index]
        return True

    @classmethod
    def personRoom(cls,typ,person):
        rooms = Room.getAllRooms()

        for room in rooms:
            if (room.hasOccupant(person)) and room.get("type") == typ:
                return room
        return None

    """
    Returns one room for random allocation
    """
    @classmethod
    def getRoom(cls, model_cls):
        rooms = model_cls.all()
        for room in rooms:
            if len(room.getOccupants()) < int(room.get("capacity")):
                return room
        return None


    @classmethod
    def importRooms(cls, source):
        #data imported from the file is paased as a multi dimension array to this method
        #confirm that atleast each array item has three elements
        if isinstance(source,list):
            data = source
        else:
            data = []
            with open(source, "r") as lines:
                for line in lines:
                    data.append(line.split())

        for datum in data:
            l = len(datum)
            if l< 2 or l >3:
                return "Data is not properly formated" 
        return  data

#---------------------------------------------
class OfficeController(RoomController):
    """docstring for ClassName"""
    def __init__(self):
        super(OfficeController, self).__init__()

class LivingController(RoomController):
    """docstring for ClassName"""
    def __init__(self):
        super(LivingController, self).__init__()

#-----------------------------------------------


class PeopleController(Controller):
    """docstring for PeopleController"""
    def __init__(self):
        super(PeopleController, self).__init__()
    

    @classmethod
    def importPeople(cls, source):
        #data imported from the file is paased as a multi dimension array to this method
        if isinstance(source,list):
            data = source
        else:
            data = []
            with open(source, "r") as lines:
                for line in lines:
                    data.append(line.split())

        for datum in data:
            l = len(datum)
            if l< 3 or l >4:
                return "Data is not properly formated"
        return  data

class StaffController(PeopleController):
    """docstring for ClassName"""
    def __init__(self):
        super(StaffController, self).__init__()


class FellowController(PeopleController):
    """docstring for ClassName"""
    def __init__(self):
        super(FellowController, self).__init__()



office1 = OfficeController.new(Office,{"name":"Tsavo"})
office2 = OfficeController.new(Office,{"name":"Hogwart"})
living = LivingController.new(Living,{"name":"Kampala"})


staff = StaffController.new(Staff,{"firstname":"Timothy", "lastname":"Wikedzi"})
fellow = FellowController.new(Fellow,{"firstname":"Gladness", "lastname":"Mwanga"})

print(RoomController.allocate(office1,fellow))
print(RoomController.allocate(office1,staff))
print(office1.getOccupants())
#print(RoomController.reallocate(office2,staff))
#print(office2.getOccupants())

PeopleController.delete(fellow)
print(office1.getOccupants())
#print(Amity.db)
#office2.delete()      
#print(Amity.db)

#p = Fellow.find({"firstname":"Timothy", "lastname":"Wikedzi"})

#print(p.get("firstname"))

#office1.save_state()




