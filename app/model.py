
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