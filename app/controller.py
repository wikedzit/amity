import time
import re

from amity import Amity
from model import Room,Office,Living ,People,Staff, Fellow


class Controller(object):

    @classmethod
    def getAll(cls,model_cls):
        return model_cls.all()

    @classmethod
    def new(cls,model_cls,data={"name":""}): 
        validators = model_cls.validators
        for key, value in validators.items():
            p = re.compile(value)
            if key in data and (not p.match(data[key])):
                return "Invalid Input" 
        obj = model_cls(data)
        return obj.save()

    @classmethod
    def edit(cls,ob,dt):
        obj = ob.__class__.find(ob.oid())
        if not obj is None:
            obj.setData(dt)
            return obj.save()
        return False

    @classmethod
    def getOne(cls,model_cls,o_id):
        return model_cls.find(o_id)

    @classmethod
    def delete(cls,obj):
        obj1 = obj.__class__.find(obj.get('_id'))
        if not obj1 is None:
            obj.delete()
            # Call thi method to cascade person delete on rooms allocations
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
            room.data['allocations'].append(person.oid())#Add person to a list
            if isinstance(room.save(), room.__class__):
                return True
            return "Failed to reallocate this person"
        else:
            #Amity.db["unallocated"].append([person.oid,"living"])
            return "Room is full. This person is placed in a waiting list"


    @classmethod
    def reallocate(cls,room,person):
        if len(room.get('allocations')) < int(room.get('capacity')):
            prev_room = cls.personRoom(room.get('type'), person)
            if isinstance(prev_room, room.__class__):#This means that this person was placed in this room
                #delete any previous placements
                indx = prev_room.get('allocations').index(person.oid())
                del prev_room.data["allocations"][indx]
                prev_room.save()

            #call for new reallocations
            return cls.allocate(room,person)
        else:
            #Reaching here it means all the rooms are full
            #Place this person in the waiting list while stating the tyoe of room
            #Amity.db["unallocated"].append([person.oid,"office"])
            return "This room is full. Can't reallocate this person, "


    @classmethod
    def clean(cls):
        """    
            This method loops through all rooms to delete all Ids for people that have been deleted 
        """
        office = Office.getRooms()
        living  = Living.getRooms()

        rooms = office + living
        for room in rooms:
            allocations = room.getOccupants()
            if len(allocations) > 0 :
                for person_id  in allocations:
                    person = Staff.find(person_id)
                    if person is None:
                        person = Fellow.find(person_id)
                        
                    p_index = allocations.index(person_id)
                    del room.data['allocations'][p_index]
                    room.save()
        return True


    @classmethod
    def personRoom(cls,typ,person):
        offices = Office.getRooms()
        living = Living.getRooms()
        rooms = offices + living

        for room in rooms:
            if (person.oid() in room.get('allocations') ) and room.get("type") == typ:
                return room
        return None

    """
    Returns one room for random allocation
    """
    @classmethod
    def getRoom(cls, model_cls):
        rooms = model_cls.all()
        for room in rooms:
            if len(room.get("allocations")) < room.get("capacity"):
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



office = OfficeController.new(Office,{"name":"Tsavo"})
staff = StaffController.new(Staff,{"firstname":"Roger", "lastname":"Taracha"})
OfficeController.edit(office, {"name":"Hei"})

#print(office.data)
#OfficeController.allocate(office,staff)

