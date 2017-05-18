import time
from model import Amity
from model import Office
from model import Living 
from model import Staff
from model import Fellow


class Controller(object):
    """docstring for Controler"""
    def __init__(self):
        pass

    def getAll(model_cls):
        return model_cls.all()

    @classmethod
    def new(cls,model_cls,data={"name":""}): 
        oid = int(round(time.time() * 1000))
        obj = model_cls(oid,data)
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
    def delete(model_cls,o_id):
        obj = model_cls.find(o_id)
        if isinstance(obj,model_cls):
            obj.delete()
            return True
        return False

#-----------------------------------------------

class RoomController(Controller):
    """docstring for ClassName"""
    def __init__(self):
        super(RoomController, self).__init__()


#---------------------------------------------
class OfficeController(RoomController):
    """docstring for ClassName"""
    def __init__(self):
        super(OfficeController, self).__init__()

    
    @classmethod
    def allocate(cls,person):
        rooms = Office.getOffices()
        if len(rooms) == 0 :
            return "No room is available"

        if person in Office.getAllAllocatedPeople():
            return "You can not allocated the same person more tan one time"

        for room in rooms:
            if len(room.data['allocations']) < int(room.data['capacity']):
                (room.data['allocations']).append(person)
                return True
        return False

#-----------------------------------------------

#---------------------------------------------
class LivingController(Controller):
    """docstring for ClassName"""
    def __init__(self):
        super(LivingController, self).__init__()
       
#-----------------------------------------------


class StaffController(Controller):
    """docstring for ClassName"""
    def __init__(self):
        super(StaffController, self).__init__()




