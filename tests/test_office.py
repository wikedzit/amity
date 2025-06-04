import unittest


class Office(object):
    """Simple representation of an office."""

    _capacity = 6

    def __init__(self, details=None):
        details = details or {"name": ""}
        self.name = details["name"]

    def add(self, name):
        if not isinstance(name, str):
            raise TypeError("Office name must be a string")
        self.name = name
        return self.save()

    def save(self):
        return True

    def edit(self, office_id, data):
        if type(office_id) is not int:
            raise TypeError(" ID must be a number")
        office = Office.find(office_id)
        if isinstance(office, Office):
            office.name = data["name"]
            if self.save():
                return True
        return False
    @staticmethod
    def find(office_id):
        if office_id == 1:
            return Office({"name": "Main"})
        return None

#--------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------

class TestOffice(unittest.TestCase):
    """docstring for OfficeTest"""
    
    def setUp(self):
        self.office = Office()

    def test_find_office(self):
        office = Office.find(1)
        self.assertTrue(isinstance(office,Office))

    def test_save_office(self):
        officename = "Office 1"
        self.assertTrue(self.office.add(officename))

    def test_add_typeerror(self):
        with self.assertRaises(TypeError):
            self.office.add(7)

    def test_edit_office(self):

        result = self.office.edit(1, {"name": "Office"})
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()