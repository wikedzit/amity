
class Model(object):
    """docstring for Model"""
    def __init__(self,dt={},tb=None):
        self._data = dt
        self._table = tb
        print("Init")
    
    def save(self):
        print("save ",self._data)
        return self

    def delete(self):
        print("delete")

    def find(id, source):
        print("find ", id ," on table ", source._table)

    def all(source):
        table = source._table
        return {}

    def get(source,attributes={}):
        print("get")
#-----------------------------------------------------------



class People(Model):
    """docstring for Room"""

    def __init__(self):
        super(People,self).__init__()
        self._name = ""
#-------------------------------------------------------

class Fellow(People):
    """docstring for Office"""
    _table = "people"
    def __init__(self):
        super(Fellow, self).__init__()

#----------------------------------------------------------

class Staff(People):
    """docstring for Office"""
    _table = "people"
    def __init__(self):
        super(Staff, self).__init__()
#----------------------------------------------


class Room(Model):
    """docstring for Room"""
    def __init__(self):
        super(Room,self).__init__()
        self._name = ""


class Office(Room):
    """docstring for Office"""
    _table = "rooms"
    def __init__(self):
        super(Office, self).__init__()


class Living(Room):
    """docstring for Office"""
    _table = "rooms"
    def __init__(self):
        super(Living, self).__init__()









