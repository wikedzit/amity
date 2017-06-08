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

    """-----------------------------------------------------------------------
    save()  method, used for storing edited and new records
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    if an object has _id attribute it means we are editing the document, otherwise we insert it as new
    Successul save operation return a saved object
    """
    def save(self):
        tb = str(self.table)
        try:
            if '_id' in self.data.keys():
                oid = ObjectId(self.oid())
                #del self.data['_id'] # Remove the iD since ID of an existing document/record cant be replaced in Mongo
                Amity.db[tb].update_one({'_id':oid},{"$set":self.data})
            else:
                oid =  Amity.db[tb].insert_one(self.data).inserted_id
            self.data.update({'_id':oid})#update  data Dict with an id to be used for referencing in code
        except Exception as e:
            return "Failed to save the data"
        else:
            return self

    """------------------------------------------------------------------
    delete() method, used for deleting a single document/record in a collection/table
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    Called on an individual object / record to delete it
    Returns True if delete operation is successfull and false otherwise
    """
    def delete(self):
        try:
            oid = ObjectId(self.oid())
            Amity.db[self.table].delete_one({'_id':oid})
        except Exception as e:
            return False
        else:
            return True


    """-------------------------------------------------------------------
    find(ID) method, used to finding records with specific Id in a collection/Table
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It takes in object ID for a record to find
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    """
    @classmethod
    def find(cls,oid):
        oid = ObjectId(oid)
        record = Amity.db[cls._table].find_one({'_id':oid})
        if record:
                return cls(record) ## Return a record that is mapped to a proper python class
        return None


    """-------------------------------------------------------------------
    findWhere(FILTER) method, used to finding one record that matches the unique filter
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It takes in object string name for a record to find
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    """
    @classmethod
    def findWhere(cls,fltr={}):
        record = Amity.db[cls._table].find_one(fltr)
        if record:
                return cls(record) ## Return a record that is mapped to a proper python class
        return None


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
            data= Amity.[tb].find(cls.fltr)
            records = []
            for datum in data:# Get datum as a  dictionary 
                if len(datum) > 0: #Check if datum contains an item
                    if flag == "ids":
                        record = str(datum['_id'])
                    else:
                        record = cls(datum)
                    records.append(record)
        except Exception as e:
            raise
        else:
            return records
        return []


    """-------------------------------------------------------------------
    where(FILTER) method, used for fetching all records/documents from a given collection/table base of Filtering condition
    It is a class variable, can be called by immediate and Deep Subclassed of Amity Class
    It mapped it self to a class that is calling it effect the right setting including the collection/table to be used
    It returns a list of records mapped to respective class type 
    """        
    @classmethod
    def where(cls, fltr = {}):
        data= Amity.db[cls._table].find(fltr)
        records = []
        for datum in data:# Get datum as a  dictionary 
            record = cls(datum)
            records.append(record)
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
    oid() method, used returns an objectId for a record
    It is an instance variable, can be called by immediate and Deep Amity Subclassed objects
    """
    def oid(self):
        return str(self.get('_id'))


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









