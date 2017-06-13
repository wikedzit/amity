import time


class Amity(object):
    """
        Amity is the root Model class. Defines data management functions
        that are inherited by all its subclasses
    """
    db = {
        "rooms" :[],
        "people":[],
        "allocations":[],
        "unallocated":[]
    }

    cid = 0
    def __init__(self,oid=0, tb=None):
        Amity.cid+=1
        self.oid = Amity.cid
        self.table = tb
        self.data = {}

    def save(self):
        tb = str(self.table)
        try:
            if self in Amity.db[tb]:
                   # If this record alreasy exists in the db we skip saving a new one
                pass
            else:
                Amity.db[tb].append(self)
        except Exception as e:
            return None
        else:
            return self

    def delete(self):
        records = Amity.db[self.table]
        for record in records:
            if record.oid == self.oid:
                index = records.index(record)
                del Amity.db[self.table][index]
                return True
        return False


    @classmethod
    def find(cls,oid):
        tb = cls._table
        records = Amity.db[tb]
        for record in records:
            if record.oid == oid:
                return record
        return None


    @classmethod
    def all(cls):
        return Amity.db[cls._table]

    def get(self,attribute):
        return str(self.data[attribute])


    def setData(self,dt):
        for key in dt.keys():
            self.data[key] = dt[key]
        return self

#-----------------------------------------------------------

class People(Amity):
    """docstring for Room"""
    _table = "people"
    validators = {"firstname":r"([a-zA-Z]+)", 
                            "lastname": r"([a-zA-Z]+)",
                            "file":r"([a-zA-Z]+)"
                        }
    def __init__(self,oid=0):
        super(People,self).__init__(oid,People._table)


    def typeIs(self,type):
        if self.data['type'] == type:
            return True
        return False

#-------------------------------------------------------

class Fellow(People):
    """docstring for Office"""
    
    def __init__(self,oid=0,dt=None):
        if dt is None:
            dt = {}
        super(Fellow, self).__init__(oid)
        self.data = dt
        self.data.update({"type":"fellow"})

#----------------------------------------------------------

class Staff(People):
    """docstring for Office"""
    def __init__(self,oid=0,dt=None):
        if dt is None:
            dt = {}
        super(Staff, self).__init__(oid)
        self.data = dt
        self.data.update({"type":"staff"})
#----------------------------------------------

class Room(Amity):
    """docstring for Room"""
    _table = "rooms"
    validators = {"name":r"(\w+)"}

    def __init__(self,oid=0):
        super(Room,self).__init__(oid,Room._table)

    @classmethod
    def getRooms(cls):
        rooms = []
        for room in Amity.db["rooms"]:
            if room.data['type'] == cls.room_type:
                rooms.append(room)
        return rooms

    def getOccupants(self):
        return self.data["allocations"]


    def hasOccupant(self,person):
        return (person.oid in self.getOccupants())


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
    def __init__(self, oid=0, dt=None):
        if dt is None:
            dt = {}
        super(Office, self).__init__(oid)
        self.data = dt
        if not "capacity" in dt:
            self.data.update({"type":"office","capacity":6,"allocations":[]})
        else:
            self.data.update({"type":"office","allocations":[]})


class Living(Room):
    """docstring for Office"""
    room_type = "living"
    def __init__(self,oid=0, dt=None):
        if dt is None:
            dt = {}
        super(Living, self).__init__(oid)
        if not "capacity" in dt:
            dt.update({"type":"living","capacity":4,"allocations":[]})
        else:
            dt.update({"type":"living","allocations":[]})
        self.data = dt










