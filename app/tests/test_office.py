import unittest


class Office(object):
    """docstring for Office"""
    _capacity = 6
    def __init__(self,details):
        self.name = details['name']

    def save(self):
        if  True:
            return True
        else:
            return False

    def edit(self,office_id,data):
        if type(office_id) is not int :
            raise TypeError(" ID must be a number")
        office = Office.find(office_id)
        if isinstance(office,Office):
            office.name = data['name']
            if self.save():return True
        return False

    def find(office_id):
        if office_id is 1:
            return Office()
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

        self.office.edit(1,{'name':'Office'})

        self.assertTrue()


if __name__ == '__main__':
    unittest.main()