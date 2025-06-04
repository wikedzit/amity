import time
import re
from model import Amity
from model import Office
from model import Living 
from model import People
from model import Staff
from model import Fellow


class Controller:
    """docstring for Controler"""
    def __init__(self):
        pass

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

        obj = model_cls(0,data)
        return obj.save()

    @classmethod
    def getOne(cls,model_cls,o_id):
        return model_cls.find(o_id)

    @classmethod
    def edit(cls,model_cls,o_id,dt):
        obj = model_cls.find(o_id)
        if isinstance(obj,model_cls):
            obj.setData(dt)
            obj.save()
            return True
        return False

    @classmethod
    def delete(cls,model_cls,o_id):
        obj = model_cls.find(o_id)
        if isinstance(obj,model_cls):
            obj.delete()

            # Call thi method to cascade person delete on rooms allocations
            RoomController.clean()
            return True
        return False

#-----------------------------------------------

class RoomController(Controller):
    """docstring for ClassName"""
    def __init__(self):
        super().__init__()


    @classmethod
    def clean(cls):
        """    This method loops through all rooms to delete all Ids for people that have been deleted """
        rooms  = Amity.db['rooms']
        for room in rooms:
            allocations = room.data['allocations'] 
            r_index = rooms.index(room)
            for person_id  in allocations:
                staff = StaffController.getOne(Staff,person_id)
                fellow = FellowController.getOne(Fellow,person_id)
                if staff is None and fellow is None:
                    p_index = allocations.index(person_id)
                    del Amity.db['rooms'][r_index].data["allocations"][p_index]
        return True

    @classmethod
    def personRoom(cls,typ,person):
        rooms = Amity.db['rooms']
        for room in rooms:
            if person.oid in room.data['allocations'] and room.data["type"] == typ:
                return room
        return None

    @classmethod

    def importRooms(cls, data):
        #data imported from the file is paased as a multi dimension array to this method
        #confirm that atleast each array item has three elements

        for datum in data:
            l = len(datum)
            if l< 2 or l >3:
                return "Data is not properly formated"

        #Process data import
#---------------------------------------------
class OfficeController(RoomController):
    """docstring for ClassName"""
    def __init__(self):
        super().__init__()

    
    @classmethod
    def allocate(cls,room,person):
       
        if person.oid in Office.getAllAllocatedPeople():
            return "Multiple assignment"

        if len(room.data['allocations']) < int(room.data['capacity']):
            (room.data['allocations']).append(person.oid)
            return True
        else:
            Amity.db["unallocated"].append([person.oid,"office"])
            return "Room is full. This person is placed in a waiting list"

    @classmethod
    def reallocate(cls,room,person):
        if len(room.data['allocations']) < int(room.data['capacity']):
            prev_room = OfficeController.personRoom("office", person)
            if isinstance(prev_room, Office):
                indx = prev_room.data['allocations'].index(person.oid)
                del prev_room.data['allocations'][indx]

            return OfficeController.allocate(room,person)
        else:
            #Reaching here it means all the rooms are full
            #Place this person in the waiting list while stating the tyoe of room
            #Amity.db["unallocated"].append([person.oid,"office"])
            return "This room is full. Can't reallocate this person, "
#-----------------------------------------------

#---------------------------------------------
class LivingController(RoomController):
    """docstring for ClassName"""
    def __init__(self):
        super().__init__()

    @classmethod
    def allocate(cls,room,person):
        if person.typeIs('staff'):
            return "Staff can't be assigned a living room"

        if person.oid in Living.getAllAllocatedPeople():
            return "Multiple assignment"

        if len(room.data['allocations']) < int(room.data['capacity']):
            (room.data['allocations']).append(person.oid)
            return True
        else:
            Amity.db["unallocated"].append([person.oid,"living"])
            return "Room is full. This person is placed in a waiting list"

    @classmethod
    def reallocate(cls,room,person):
        if len(room.data['allocations']) < int(room.data['capacity']):
            prev_room = LivingController.personRoom("living", person)
            if isinstance(prev_room, Living):
                #delete any previous placements
                indx = prev_room.data['allocations'].index(person.oid)
                del prev_room.data['allocations'][indx]

            #call for new reallocations
            return LivingController.allocate(room,person)
        else:
            #Reaching here it means all the rooms are full
            #Place this person in the waiting list while stating the tyoe of room
            #Amity.db["unallocated"].append([person.oid,"office"])
            return "This room is full. Can't reallocate this person, "
#-----------------------------------------------


class PeopleController(Controller):
    """docstring for PeopleController"""
    def __init__(self):
        super().__init__()
    
    @classmethod
    def importPeople(cls, data):
        #data imported from the file is paased as a multi dimension array to this method
        #confirm that atleast each array item has three elements

        for datum in data:
            l = len(datum)
            if l<3 or l >4:
                return "Data is not properly formated"

        #Process data import

class StaffController(PeopleController):
    """docstring for ClassName"""
    def __init__(self):
        super().__init__()


class FellowController(PeopleController):
    """docstring for ClassName"""
    def __init__(self):
        super().__init__()

