from model import Amity,Room,Office,Living, People, Staff, Fellow
from controller import PeopleController,RoomController,OfficeController, LivingController, FellowController, StaffController


class Core():
    def __init__(self):
      pass

    def add_room(self, typ="office", rooms=[]):
      message = ""
      for room in rooms:
        if typ == "office" or typ == "o" :
          typ = "office"
          message =  OfficeController.new(Office,{"name": room.title()})
        elif typ =="living" or typ == "l":
          typ = "living"
          message =  LivingController.new(Living,{"name": room.title()})
        else:

          print( typ, " is wrong room type")

        if isinstance(message,Room):
          print(room," ", typ ,"room has been created!!")
        else:
          print(message)

    def show_rooms(self):
      rooms = Room.getAllRooms()
      count = 0
      print("----------------------------------------------------------")
      print("SN", "\t| ", "Name", '\t\t| ', "Type" )
      print("----------------------------------------------------------")
      for room in rooms: 
        count+=1
        print(count, "\t| ", str(room.get('name')), '\t\t| ', str(room.get('type')))


    def delete_room(self, name):
        room = Room.find({"name":name})
        if room:
          if RoomController.delete(room):
            print(room.get("name"), " delete successfull")
          else:
            print("Failed to delete the room")
        else:
          print("Room not found")


    def add_person(self, typ="fellow", fname="",lname="",accomodation="N"):
      person = None
      message= ""
      fname = fname.title(); lname = lname.title()
      accomodation = accomodation.title()

      accm = "N"
      if accomodation and accomodation=="Y":
        accm = "Y"

      if typ == "staff" or typ =="s" :
        typ = "staff"
        message = StaffController.new(Staff,{"firstname":fname, "lastname":lname,"accomodation":accm})
      if typ  == "fellow" or "f":
        typ = "fellow"
        message = FellowController.new(Fellow, {"firstname":fname, "lastname":lname,"accomodation":accm})

      if isinstance(message,People):
        print(typ.title(), " " , fname, " " , lname , " Added successfully")
        person = message # assign the returned person objet to a variable
        office = OfficeController.getRoom(Office)
        if isinstance(office,Room):
          message = OfficeController.allocate(office,person)
          if isinstance(message,bool):
            print(fname , " ", lname, " placed in ", office.get("name"))
          else:
            print(message)
        else:
          print("Could not allocate ", fname , " ", lname, " a room, will be in a waiting list")
      else:
        print(message)

      if isinstance(person,People) and accm=="Y":
        living = LivingController.getRoom(Living)
        if isinstance(living,Room):
          message = LivingController.allocate(living,person)
          if isinstance(message,bool):
            print(fname , " ", lname, " placed in ", living.get("name"))
          else:
            print(message)
        else: 
          print("Could not allocate ", fname , " ", lname, " a living space, will be in a waiting list")


    def show_people(self):
      people = People.getAllPeople()
      count = 0
      print("--------------------------------------------------------------------------------------")
      print("SN", "\t| ", "Firstname", "\t\t| ","Lastname",'\t\t| ', "Type" )
      print("---------------------------------------------------------------------------------------")
      for person in people: 
        count+=1
        print(count, "\t| ", str(person.get('firstname')),'\t\t| ',str(person.get('lastname')),'\t\t| ', str(person.get('type')))


    def delete_person(self, firstname,lastname):
      person = People.find({"firstname":firstname,"lastname":lastname})
      if person:
        if PeopleController.delete(person):
          print(firstname, " ", lastname, " record has delete successfull")
        else:
          print("Failed to delete  ", person_name)
      else:
        print(firstname, " ", lastname, " Room not found")


    def reallocate(self, fname="",lname="",room_name=""):
      fname = str(fname)
      lname = str(lname)
      room_name = str(room_name)
      room = Room.find({"name":room_name})
      if not room:
        print("Room named ",room_name," does not exists")
      else:
        person = People.find({"firstname":fname,"lastname":lname})
        if not person:
          print("Person with the names ",fname + lname," does not exists")
        else:
          if RoomController.reallocate(room,person):
            print(fname," ", lname, " reallocated to " ,room_name)


    def auto_reallocate(self):
      rooms = Room.getAllRooms()
      allocated = []

      for room in rooms:
        allocated +=room.getOccupants()

      people = People.getAllPeople()
      for person in people:
        found = False
        for person_id in allocated:
          if str(person_id) == str(person.oid()):
            found = True
        
        if not found:
          office = OfficeController.getRoom(Office)
          if isinstance(office,Room):
            message = OfficeController.allocate(office,person)
            if isinstance(message,bool):
              print(person.get("firstname") , " ", person.get("lastname"), " placed in ", office.get("name"))
            else:
              print(message)
          else:
            print("Could not allocate ", person.get("firstname") , " ",person.get("lastname"), " a room this time")


          if person.get("accomodation") == "Y":
            living = LivingController.getRoom(Living)
            if isinstance(living,Room):
              message = LivingController.allocate(living,person)
              if isinstance(message,bool):
                print(person.get("firstname") , " ", person.get("lastname"), " placed in ", living.get("name"))
              else:
                print(message)
            else:
              print("Could not allocate ", person.get("firstname") , " ",person.get("lastname"), " a room this time")

    def print_allocations(self, save_to_file=None):
      rooms = Room.getAllRooms()
      
      #loop through the rooms to get the ids of people who have been assigned
      out = []
      for room in rooms:
        allocations =room.getOccupants()
        out.append("-------------------------------------------------------------------")
        out.append( room.get("name")  + " Total occupants " + str(len(room.getOccupants())))
        out.append("-------------------------------------------------------------------")
        out.append("SN\t| Firstname\t\t| Lastname\t\t| Type" )
        out.append("-------------------------------------------------------------------")
        count = 0
        for person_id in allocations:
          person = Staff.find(person_id)
          if person is None:
            person = Fellow.find(person_id)
          if not person is None:
            count+=1
            s = str(count)+ "\t| "+ str(person.get('firstname')) +  "\t| " + str(person.get('lastname'))+  "\t| " + str(person.get('type'))
            out.append(s)

      if not save_to_file is None: # Prepare data for saving to file
        if(Amity.writeToFile(save_to_file,out)):
          print("Data written to file ", save_to_file)
        else:
          print("Data could not be written")
      else:
        for s in out:
          print(s)

    def print_unallocated(self, save_to_file=None):
      rooms = Room.getAllRooms()
      allocated = []

      count = 0
      out=[]

      out.append("-------------------------------------------------------------")
      out.append("List of unallocated people")
      out.append("--------------------------------------------------------------")
      out.append("SN\t| Firstname\t\t| Lastname\t\t| Type" )
      out.append("--------------------------------------------------------------")
      for room in rooms:
        allocated +=room.getOccupants()

      people = People.getAllPeople()
      for person in people:
        found = False
        if person.name() in allocated:
            found = True
        if not found:
          count+=1
          s = str(count)+ "\t| " + str(person.get('firstname'))+ "\t\t| " + str(person.get('lastname'))+ "\t\t| " + str(person.get('type'))
          out.append(s)

      if not save_to_file is None: # Prepare data for saving to file
        if(Amity.writeToFile(save_to_file,out)):
          print("Data written to file ", save_to_file)
        else:
          print("Data could not be written")
      else:
        for s in out:
          print(s)


    def print_room(self, room_name="",save_to_file=None ):
      room = Room.find({"name":room_name})
      if not room is None:
        allocations = room.getOccupants()
        count = 0
        out = []
        out.append("------------------------------------------------------------------------------------")
        out.append(room.get("name") + " Total occupants " + str(len(room.getOccupants())))
        out.append("------------------------------------------------------------------------------------")
        out.append("SN\t| Firstname\t\t| Lastname\t\t| Type")   
        out.append("------------------------------------------------------------------------------------")
        for person_name in allocations:
          person = People.find(person_name)
          if not person is None:
            count+=1
            s = str(count)+"\t| "+ str(person.get('firstname'))+ "\t\t| "+ str(person.get('lastname'))+ "\t\t| "+ str(person.get('type'))
            out.append(s)

        if not save_to_file is None: # Prepare data for saving to file
          if(Amity.writeToFile(save_to_file,out)):
            print("Data written to file ", save_to_file)
          else:
            print("Data could not be written")
        else:
          for s in out:
            print(s)
      else:
        print("Room ", room_name , " does not exist")


    def load_people(self, filename):
      data = ""
      try:
        data = PeopleController.importPeople(filename)
      except Exception as e:
        print("Couldnt load the file, make sure it exists and try again")
        return
      
      if isinstance(data,list):
        for datum in data:
          if len(datum) == 4:
            fname = datum[0].title()
            lname = datum[1].title()
            typ = datum[2].lower()
            accomodation = datum[3].title()

          if len(datum) == 3:
            fname = datum[0].title()
            lname = datum[1].title()
            typ = datum[2].lower()
            accomodation = "N"

          if not (typ == "fellow" or "f" or typ == "staff" or "s"):
            print("Wrong Person type ")
          elif not (accomodation == "N" or accomodation=="Y"):
            print("Want accomodation not properly set")
          else:
            self.add_person(typ,fname,lname,accomodation)
        else:
          print("Wrong Data")

    def load_rooms(self, filename):
      data = ""
      try:
        data = RoomController.importRooms(filename)
      except Exception as e:
        print("Couldnt load the file, make sure it exists and try again")
        return
      
      if isinstance(data,list):
        for datum in data:
          if len(datum) == 2:
            name = datum[0].title()
            typ = datum[1].lower()

          if len(datum) == 1:
            name= datum[0].title()
            typ = "office"

          if not (typ == "office" or "o" or typ == "living" or "l"):
            print("Wrong Room type ")
          else:
            self.add_room(typ,[name])
        else:
          print("Wrong Data")


    def help(self):
      usage = """
      Usage:
        app.py add_room <type> <name>... 
        app.py delete_room  <name>
        app.py show_rooms
        app.py add_person <firstname> <lastname> <type> [<accomodation>]
        app.py delete_person <person_identifier>
        app.py show_people
        app.py auto_reallocate
        app.py reallocate <firstname> <lastname> <new_room_name>
        app.py load_people <people_file>
        app.py load_rooms <room_file>
        app.py print_allocations [-o FILE]
        app.py print_unallocated [-o FILE]
        app.py print_room  <print_room_name>  [-o FILE]
      """
      print(usage)

