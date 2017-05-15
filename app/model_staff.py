
from model_people import People
class Staff(People):
    """docstring for Office"""
    _table = "people"
    def __init__(self):
        super(Staff, self).__init__()

