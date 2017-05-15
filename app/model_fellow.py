from model_people import People
class Fellow(People):
    """docstring for Office"""
    _table = "people"
    def __init__(self):
        super(Fellow, self).__init__()

