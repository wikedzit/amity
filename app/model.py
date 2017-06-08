import time
from amity import Amity

from bson.objectid import ObjectId



class People(Amity):
    """docstring for Room"""
    _table = "people"
    fltr = {}# It is a black filter because this will return both staff and fellows
    validators = {"firstname":r"([a-zA-Z]+)", 
                            "lastname": r"([a-zA-Z]+)",
                            "file":r"([a-zA-Z]+)"
                        }
    def __init__(self):
        super(People,self).__init__(People._table)


    @classmethod
    def getAllPeople(cls):
        staff = Staff.all()
        fellow = Fellow.all()
        return staff + fellow


    """-----------------------------------------------------------------------
    load_data()  method, loads state of the DB
    Successul save operation return a saved object
    """
    @classmethod
    def load_people(cls):
       people = People.getAllPeople()
       Amity['people '] = people

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
        super(Room,self).__init__(Room._table)


    @classmethod
    def getAllRooms(cls):
        offices = Office.getRooms()
        living = Living.getRooms()
        return offices + living

    @classmethod
    def loadRooms(cls):
        rooms = Room.getAllRooms()
        Amity["rooms"] = rooms

    @classmethod
    def getRooms(cls):
        return cls.where({'type':cls.room_type})


    def getOccupants(self):
        occupants = []
        allocations = self.get("allocations");
        for allocation in allocations:
            occupants.append(str(allocation))

        return occupants

    def hasOccupant(self,person):
        return person.oid() in self.getOccupants()


    @classmethod
    def getAllAllocatedPeople(cls):
        rooms = cls.getRooms()
        occupants = []
        for room in rooms:
            occupants += room.data["allocations"]
        return occupants


    #@classmethod
    #def locatePerson(cls,person):
        #rooms = Amity.db['rooms']
        #foundin= {}
        #for room in rooms:
            #if person.oid in room.data['allocations']:
                #foundin.update({room.data['type']:room.data['name']})

        #return foundin


class Office(Room):
    """docstring for Office"""
    room_type = "office"
    fltr = {"type": "office"}

    def __init__(self, dt={}):
        super(Office, self).__init__()
        self.data = dt
        if not "capacity" in dt.keys():
            self.data.update({"type":"office","capacity":6,"allocations":[]})
        else:
            self.data.update({"type":"office","allocations":[]})


class Living(Room):
    """docstring for Office"""
    room_type = "living"
    fltr = {"type": "living"}

    def __init__(self, dt={}):
        super(Living, self).__init__()
        if not "capacity" in dt.keys():
            dt.update({"type":"living","capacity":4,"allocations":[]})
        else:
            dt.update({"type":"living","allocations":[]})
        self.data = dt







