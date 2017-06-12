import time
import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads

#-----------------------DB----CONNECTION----------------------------------#
client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
datab = client.amity


class Amity(object):
    """
        Amity is the root Model class. Defines data management functions
        that are inherited by all its subclasses
    """
    db = {
        "rooms":[],
        "people":[]
    }

    def __init__(self):
        pass

    @classmethod
    def cleanDb(cls):
        try:
            datab["rooms"].delete_many({})
            datab["people"].delete_many({})
        except Exception as e:
            False
        else:
            True

    """-------------------------------------------------------------------
    load() method, used for fetching all records/documents from a given collection/table
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    It returns a list of records mapped to respective class type 
    """        
    @classmethod
    def load(cls):
        tb = str(cls._table)
        try:
            data= datab[tb].find(cls.fltr)
            records = []
            for datum in data:# Get datum as a  dictionary 
                if len(datum) > 0: #Check if datum contains an item
                    del datum['_id']
                    record = cls(datum)
                    records.append(record)
        except Exception as e:
            raise
        else:
            return records
        return []


    """-----------------------------------------------------------------------
    save_state()  method, used for storing edited and new records
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    if an object has _id attribute it means we are editing the document, otherwise we insert it as new
    Successul save operation return a saved object
    """
    def save_state(self):
        tb = str(self.table)
        try:
            datab[tb].insert_one(self.data)
        except Exception as e:
            return "Failed to save the data"
        else:
            return self


    """-----------------------------------------------------------------------
    save()  method, used for storing edited and new records
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    if an object has _id attribute it means we are editing the document, otherwise we insert it as new
    Successul save operation return a saved object
    """
    def save(self):
        tb = str(self.table)
        try:
            Amity.db[tb].append(self)
        except Exception as e:
            return "Failed to save the data"
        else:
            return self


    """-------------------------------------------------------------------
    all() method, used for fetching all records/documents from a given collection/table
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    It returns a list of records mapped to respective class type 
    """        
    @classmethod
    def all(cls,flag=None):
        tb = str(cls._table)
        try:
            objs = cls.where(cls.fltr)
            records = []
            for obj in objs:# Get datum as a  dictionary 
                if flag == "names":
                    obj = obj.name()
                records.append(obj)
        except Exception as e:
            return []
        else:
            return records
        

    """-------------------------------------------------------------------
    find(ID) method, used to finding records with specific Id in a collection/Table
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    """
    @classmethod
    def find(cls,fltr={}):
        record = cls.where(fltr)
        if len(record) > 0:
                return record[0]
        return None

    """-------------------------------------------------------------------
    where(FILTER) method, used for fetching all records/documents from a given collection/table base of Filtering condition
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    It returns a list of records mapped to respective class type 
    """        
    @classmethod
    def where(cls, fltr = {}):
        tb = cls._table
        data = Amity.db[tb]
        records = []
        for datum in data:# Get datum as a  dictionary 
            if len(fltr) > 0:
                found = 0
                for f in fltr.values():
                    if f in datum.data.values():
                        found+=1
                if found == len(fltr):
                    records.append(datum)
            if len(fltr)<=0:
                records.append(datum)
        return records

    """------------------------------------------------------------------
    get(attribute) method, used for fetching a value of specific Keyed item from a record
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    Returns the value for that key
    """
    def get(self,attrib):
        if attrib in self.data.keys():
            return self.data[attrib]
        else:
            return None


    """------------------------------------------------------------------
    setData(DATA) method, used for updating object data 
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    Returns an object with updated data.
    """
    def setData(self,dt):
        for key in dt.keys():
            self.data[key] = dt[key]
        return self


    """------------------------------------------------------------------
    typeIs(type) method, tests if a specific record is of Type Room(Office/Living) or People (Fellow/Staff)
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    Returns true if this object is of the type tested and false otherwise
    """
    def typeIs(self,typ):
        if self.get('type')== typ:
            return True
        return False



    """------------------------------------------------------------------
    delete() method, used for deleting a single document/record in a collection/table
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    Called on an individual object / record to delete it
    Returns True if delete operation is successfull and false otherwise
    """
    def delete(self):
        try:
            Amity.db[self.table].remove(self)
        except Exception as e:
            return False
        else:
            return True


    """-------------------------------------------------------------------
    write(fiLE,DATA) method, used for writing data to a file
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It returnTrue if data is saved and false otherwise
    """        
    @classmethod       
    def writeToFile(cls, file,data):
        if type(data) is list:
            f = open(file, 'w')
            for datum in data:
                line = str(datum) + "\n"
                f.write(line)
            return True
        return False  









