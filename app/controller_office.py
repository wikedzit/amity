from controller import Controller
from model_office import Office

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


OfficeController.new()
        