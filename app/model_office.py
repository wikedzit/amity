from model_room import Room
class Office(Room):
    """docstring for Office"""
    _table = "rooms"
    def __init__(self):
        super(Office, self).__init__()

