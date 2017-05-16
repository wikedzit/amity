
from model import Model

class Controller(object):
    """docstring for Controler"""
    def __init__(self):
        pass

#-----------------------------------------------

class LivingController(Controller):
    """docstring for ClassName"""
    def __init__(self, arg):
        super(LivingController, self).__init__()
        self.arg = arg
       


#-----------------------------------------------
class OfficeController(Controller):
    """docstring for ClassName"""
    def __init__(self):
        super(OfficeController, self).__init__()

    def new():
        office = Office()
        office._data = "Hogwart"
        office.save()

    def index():
        offices = Office.all(Office)

    def edit(o_id):
        office = Office.find(o_id,Office)



#---------------------------------------------
class StaffController(Controller):
    """docstring for ClassName"""
    def __init__(self):
        super(StaffController, self).__init__()

    def new():
        staff = Staff()
        staff._data = "Maureen "
        staff.save()

    def index():
        staff = Staff.all(Staff)

    def edit(o_id):
        staff = Staff.find(o_id,Staff)



