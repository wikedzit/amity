import time
from amity import Amity

from bson.objectid import ObjectId


class People(Amity):
    """docstring for Room"""
    _table = "people"
    fltr = {} # It is a black filter because this will return both staff and fellows
    validators = {"firstname":r"([a-zA-Z]+)", 
                            "lastname": r"([a-zA-Z]+)",
                            "file":r"([a-zA-Z]+)"
                        }


    def __init__(self):
        super(People,self).__init__()
        self.table = "people"

    @classmethod
    def getAllPeople(cls):
        staff = Staff.all()
        fellow = Fellow.all()
        return staff + fellow

    @classmethod
    def loadPeople(cls):
        staff = Staff.load()
        fellow = Fellow.load()
        Amity.db['people'] = staff + fellow

    def name(self):
        return {"firstname":self.get('firstname'),"lastname":self.get("lastname")}

#-------------------------------------------------------

class Fellow(People):
    """docstring for Office"""
    fltr = {"type": "fellow"}

    def __init__(self,dt={}):
        super(Fellow, self).__init__()
        self.data = dt
        self.data.update({"type":"fellow"})

#----------------------------------------------------------
class Staff(People):
    """docstring for Office"""
    fltr = {"type": "staff"}

    def __init__(self,dt={}):
        super(Staff, self).__init__()
        self.data = dt
        self.data.update({"type":"staff"})
#----------------------------------------------


class Room(Amity):
    """docstring for Room"""
    _table = "rooms"
    validators = {"name":r"(\w+)"}
    fltr = {}# it is a black filter because this is will fetch both offices and living spaces

    def __init__(self):
        super(Room,self).__init__()
        self.table = "rooms"

    def name(self):
        return {"name":self.get('name')}

    @classmethod
    def getAllRooms(cls):
        offices = Office.all()
        living = Living.all()
        return offices + living

    @classmethod
    def loadRooms(cls): 
        offices = Office.load()
        living = Living.load()
        Amity.db["rooms"] = offices + living

    def getOccupants(self):
        return self.get("allocations")

    def hasOccupant(self,person):
        return person.name() in self.getOccupants()

    @classmethod
    def getAllAllocatedPeople(cls):
        rooms = cls.getRooms()
        occupants = []
        for room in rooms:
            occupants += room.data["allocations"]
        return occupants


class Office(Room):
    """docstring for Office"""
    room_type = "office"
    fltr = {"type": "office"}

    def __init__(self, dt={}):
        super(Office, self).__init__()
        if not "capacity" in dt.keys():
            dt.update({"capacity":6})
       
        if not "type" in dt.keys():
            dt.update({"type":"office"})
        
        if not "allocations" in dt.keys():
            dt.update({"allocations":[]})
        self.data = dt


class Living(Room):
    """docstring for Office"""
    room_type = "living"
    fltr = {"type": "living"}

    def __init__(self, dt={}):
        super(Living, self).__init__()
        if not "capacity" in dt.keys():
            dt.update({"capacity":4})
       
        if not "type" in dt.keys():
            dt.update({"type":"living"})
        
        if not "allocations" in dt.keys():
            dt.update({"allocations":[]})
        self.data = dt








