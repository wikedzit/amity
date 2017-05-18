import time


class Amity(object):
    """
        Amity is the root Model class. Defines data management functions
        that are inherited by all its subclasses
    """
    db = {
        "rooms" :[],
        "people":[],
        "allocations":[]
    }


    def __init__(self,oid=0, tb=None):
        if oid == 0:
            self.oid = int(round(time.time() * 1000))
        else:
            self.oid = oid
        self.table = tb
        self.data = {}

    def save(self):
        tb = str(self.table)
        try:
            if self in Amity.db[tb]:
                   # i =  Amity.db[tb].index(self)
                   #Amity.db[tb][index].setData()
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
                del records[index]
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
        return self.data[attribute]

    def getData(self):
        return self.data

    def setData(self,dt):
        for key in dt.keys():
            self.data[key] = dt[key]
        return self

#-----------------------------------------------------------

class People(Amity):
    """docstring for Room"""
    _table = "people"
    def __init__(self,oid=0):
        super(People,self).__init__(oid,People._table)

#-------------------------------------------------------

class Fellow(People):
    """docstring for Office"""
    
    def __init__(self,oid=0,dt={}):
        super(Fellow, self).__init__(oid)
        self.data = dt
        self.data.update({"type":"fellow"})

#----------------------------------------------------------

class Staff(People):
    """docstring for Office"""
    def __init__(self,oid=0,dt={}):
        super(Staff, self).__init__(oid)
        self.data = dt
        self.data.update({"type":"staff"})
#----------------------------------------------

class Room(Amity):
    """docstring for Room"""
    _table = "rooms"
    def __init__(self,oid=0):
        super(Room,self).__init__(oid,Room._table)


class Office(Room):
    """docstring for Office"""
    def __init__(self, oid=0, dt={}):
        super(Office, self).__init__(oid)
        self.data = dt
        self.data.update({"type":"office","capacity":6,"allocations":[]})

    @classmethod
    def getOffices(cls):
        rooms = []
        for room in Amity.db["rooms"]:
            if room.data['type'] == "office":
                rooms.append(room)
        return rooms


    def getOccupants(self):
        return self.data["allocations"]

    @classmethod
    def getAllAllocatedPeople(cls):
        offices = Office.getOffices()
        occupants = []
        for office in offices:
            occupants += office.data["allocations"]
        return occupants

class Living(Room):
    """docstring for Office"""
    def __init__(self,oid=0, dt={}):
        super(Living, self).__init__(oid)
        self.data = dt
        self.data.update({"type":"living","capacity":4,"allocations":[]})









