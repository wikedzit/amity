import click
from model import Amity,Room,Office,Living, People, Staff, Fellow
from controller import Controller, PeopleController,RoomController,OfficeController, LivingController, FellowController, StaffController


class Core():
    def __init__(self):
      pass

    def load_state(self,db):
      try:
        Controller.load_state(db)
      except Exception as e:
         click.secho("Failed to load data", fg='red')
         return       
      else:
        click.secho("Data Loaded", fg='green')

    def save_state(self, db):
      try:
        Controller.save_state(db)
      except Exception as e:
        click.secho("Failed to save data to the database", fg='red')
        return
      else:
        click.secho("Data successfully stored in database", fg='green')
      

    def add_room(self, typ="office", rooms=[]):
      message = ""
      for room in rooms:
        if typ == "office" or typ == "o" :
          typ = "Office "
          message =  OfficeController.new(Office,{"name": room.title()})
        elif typ =="living" or typ == "l":
          typ = "Living space "
          message =  LivingController.new(Living,{"name": room.title()})
        else:
          click.secho( typ + " is wrong room type", fg='red')

        if isinstance(message,Room):
           click.secho(typ + room + " has been created!!", fg='green')
        else:
          print(message)


    def show_rooms(self):
      rooms = Room.getAllRooms()
      if len(rooms) == 0:
        click.secho("No room has been added. Use comand add_room or load_rooms to add new rooms", fg='yellow')
      else:
        count = 0
        print("----------------------------------------------------------")
        print("SN", "\t| ", "Name", '\t\t| ', "Type" )
        print("----------------------------------------------------------")
        for room in rooms: 
          count+=1
          print(count, "\t| ", str(room.get('name')), '\t\t| ', str(room.get('type')))


    def delete_room(self, name):
        if isinstance(name,str):
          room = Room.find({"name":name.title()})
          if room:
            if RoomController.delete(room):
               click.secho(room.get("name") + " deleted successfull", fg='green')
            else:
              click.secho("Failed to delete the room",fg='red')
          else:
            click.secho("Room not found",fg='yellow')
        else:
          click.secho("Room not found",fg='yellow')


    def add_person(self, typ, fname="",lname="",accomodation="N"):
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
      
      if typ  == "fellow" or typ== "f":
        typ = "fellow"
        message = FellowController.new(Fellow, {"firstname":fname, "lastname":lname,"accomodation":accm})

      if isinstance(message,People):
        click.secho(typ.title()+ " " + fname+ " " + lname + " added successfully",fg='green')
        person = message # assign the returned person objet to a variable
        office = OfficeController.getRoom(Office)
        if isinstance(office,Room):
          message = OfficeController.allocate(office,person)
          if isinstance(message,bool):
            click.secho(fname + " " + lname + " placed in office " + office.get("name"),fg='green')
          else:
            click.secho(message,fg='red')
        else:
          click.secho("Could not allocate "+ fname + " " + lname +  " a room, will be in a waiting list", fg='red')
      else:
        click.secho(message,fg='red')

      if isinstance(person,People) and accm=="Y":
        living = LivingController.getRoom(Living)
        if isinstance(living,Room):
          message = LivingController.allocate(living,person)
          if isinstance(message,bool):
            click.secho(fname + " " + lname + " placed in a living space " + living.get("name"),fg='green')
          else:
            click.secho(message,fg='red')
        else: 
          click.secho("Could not allocate " + fname + " " +  lname + " a living space", fg='red')

    def show_people(self):
      people = People.getAllPeople()
      if len(people) == 0:
        click.secho("No person has been added. Use comand add_person or load_people to add new people", fg='yellow')
      else:
        count = 0
        print("--------------------------------------------------------------------------------------")
        print("SN", "\t| ", "Firstname", "\t\t| ","Lastname",'\t\t| ', "Type" )
        print("---------------------------------------------------------------------------------------")
        for person in people: 
          count+=1
          print(count, "\t| ", str(person.get('firstname')),'\t\t| ',str(person.get('lastname')),'\t\t| ', str(person.get('type')))


    def delete_person(self, firstname,lastname):
      person = People.find({"firstname":firstname.title(),"lastname":lastname.title()})
      if person:
        if PeopleController.delete(person):
          click.secho(firstname.title() + " " + lastname.title() + " record deleted successfull",fg='green')
        else:
          click.secho("Failed to delete  " + firstname + " " + lastname, fg='red')
      else:
        click.secho(firstname.title()+ " " + lastname.title() + " record not found",fg='yellow')


    def reallocate(self, fname="",lname="",room_name=""):
      fname = str(fname).title()
      lname = str(lname).title()
      room_name = str(room_name).title()
      room = Room.find({"name":room_name})
      if not room:
        click.secho("Reallocation failed!! room named " + room_name + " does not exists",fg='yellow' )
      else:
        person = People.find({"firstname":fname,"lastname":lname})
        if not person:
          click.secho("Reallocation failed!!! person named "+ fname + lname + " does not exists",fg='yellow')
        else:
          message = RoomController.reallocate(room,person)
          if isinstance(message,bool):
            click.secho( fname + " " + lname + " reallocated to " + room_name, fg='green')
          else:
            click.secho(message,fg='red')

    def auto_reallocate(self):
      #Auto allocate to office
      offices = Office.all()
      livings = Living.all()

      allocated = []
      allocatedLiving=[]

      for office in offices:
        allocated+=office.getOccupants()

      for living in livings:
        allocatedLiving+=living.getOccupants()

      people = People.getAllPeople()
      for person in people:        
        if not person.name() in allocated:
          office = OfficeController.getRoom(Office)
          if isinstance(office,Room):
            message = OfficeController.allocate(office,person)
            if isinstance(message,bool):
              click.secho(person.get("firstname") + " " + person.get("lastname") + " allocated to " + office.get("name"),fg='green')
            else:
              click.secho(message,fg='red')
          else:
            click.secho("Could not allocate "+ person.get("firstname") + " " + person.get("lastname")+ " a room this time", fg='yellow')

        if not person.name() in allocatedLiving:
          if person.get("accomodation") == "Y":
            living = LivingController.getRoom(Living)
            if isinstance(living,Room):
              message = LivingController.allocate(living,person)
              if isinstance(message,bool):
                click.secho(person.get("firstname") + " "+ person.get("lastname")+ " placed in a living room " + living.get("name"), fg='green')
              else:
                click.secho(message,fg='red')
            else:
              click.secho("Could not allocate "+ person.get("firstname") + " " + person.get("lastname") + " a room this time", fg='red')

    def print_allocations(self, save_to_file=None):
      rooms = Room.getAllRooms()

      
      if len(rooms) == 0:
        click.secho("Rooms are not available, use command add_room or load_rooms to add new rooms",fg='yellow')
      else:
        #loop through the rooms to get the ids of people who have been assigned
        out = []
        for room in rooms:
          allocations =room.getOccupants()
          out.append("-------------------------------------------------------------------")
          out.append( room.get("name")  + " Total occupants " + str(len(room.getOccupants())))
          out.append("-------------------------------------------------------------------")
          out.append("SN\t| Firstname \t\t| Lastname \t\t| Type" )
          out.append("-------------------------------------------------------------------")
          count = 0
          for person_id in allocations:
            person = Staff.find(person_id)
            if person is None:
              person = Fellow.find(person_id)
            if not person is None:
              count+=1
              s = str(count)+ "\t| "+ str(person.get('firstname')) +  " \t\t| " + str(person.get('lastname'))+  " \t\t| " + str(person.get('type'))
              out.append(s)

        if not save_to_file is None: # Prepare data for saving to file
          if(Amity.writeToFile(save_to_file,out)):
            click.secho("Data written to file " + save_to_file, fg='green')
          else:
            click.secho("Data could not be written", fg='red')
        else:
          for s in out:
            print(s)

    def print_unallocated(self, save_to_file=None):
      rooms = Room.getAllRooms()
      people = People.getAllPeople()

      allocated = []
      count = 0
      out=[]

      out.append("-------------------------------------------------------------")
      out.append("List of unallocated people")
      out.append("--------------------------------------------------------------")
      out.append("SN\t| Firstname \t\t| Lastname \t\t| Type" )
      out.append("--------------------------------------------------------------")
      for room in rooms:
        allocated +=room.getOccupants()

      for person in people:
        if not (person.name() in allocated):
          count+=1
          s = str(count)+ "\t| " + str(person.get('firstname'))+ " \t\t| " + str(person.get('lastname'))+ " \t\t| " + str(person.get('type'))
          out.append(s)


      if not save_to_file is None: # Prepare data for saving to file
        if(Amity.writeToFile(save_to_file,out)):
          click.secho("Data written to file " + save_to_file, fg='green')
        else:
          click.secho("Data could not be written", fg='red')
      else:
        for s in out:
          print(s)



    def print_unallocated_office(self, save_to_file=None):
      rooms = Office.all()
      people = People.getAllPeople()

      allocated = []
      count = 0
      out=[]

      out.append("-------------------------------------------------------------")
      out.append("List of people not placed in Offices")
      out.append("--------------------------------------------------------------")
      out.append("SN\t| Firstname \t\t| Lastname \t\t| Type" )
      out.append("--------------------------------------------------------------")
      for room in rooms:
        allocated +=room.getOccupants()

      for person in people:
        if not (person.name() in allocated):
          count+=1
          s = str(count)+ "\t| " + str(person.get('firstname'))+ " \t\t| " + str(person.get('lastname'))+ " \t\t| " + str(person.get('type'))
          out.append(s)

      if not save_to_file is None: # Prepare data for saving to file
        if(Amity.writeToFile(save_to_file,out)):
          click.secho("Data written to file " + save_to_file, fg='green')
        else:
          click.secho("Data could not be written", fg='red')
      else:
        for s in out:
          print(s)


    def print_unallocated_living(self, save_to_file=None):
      rooms = Living.all()
      people = Fellow.all()

      allocated = []
      count = 0
      out=[]

      out.append("-------------------------------------------------------------")
      out.append("List of pople not placed in living rooms")
      out.append("--------------------------------------------------------------")
      out.append("SN\t| Firstname \t\t| Lastname \t\t| Type" )
      out.append("--------------------------------------------------------------")
      for room in rooms:
        allocated +=room.getOccupants()

      for person in people:
        if not (person.name() in allocated):
          count+=1
          s = str(count)+ "\t| " + str(person.get('firstname'))+ " \t\t| " + str(person.get('lastname'))+ " \t\t| " + str(person.get('type'))
          out.append(s)

      if not save_to_file is None: # Prepare data for saving to file
        if(Amity.writeToFile(save_to_file,out)):
          click.secho("Data written to file " + save_to_file, fg='green')
        else:
          click.secho("Data could not be written", fg='red')
      else:
        for s in out:
          print(s)



    def print_room(self, room_name="",save_to_file=None ):
      room = Room.find({"name":room_name})
      if room:
        allocations = room.getOccupants()
        count = 0
        out = []
        out.append("-----------------------------------------------------------------------------------------------")
        out.append(room.get("name") + " Total occupants " + str(len(room.getOccupants())))
        out.append("-----------------------------------------------------------------------------------------------")
        out.append("SN\t| Firstname\t\t| Lastname\t\t| Type")   
        out.append("-----------------------------------------------------------------------------------------------")
        for person_name in allocations:
          person = People.find(person_name)
          if not person is None:
            count+=1
            s = str(count)+"\t| "+ str(person.get('firstname'))+ "\t\t| "+ str(person.get('lastname'))+ "\t\t| "+ str(person.get('type'))
            out.append(s)

        if not save_to_file is None: # Prepare data for saving to file
          if(Amity.writeToFile(save_to_file,out)):
            click.secho("Data written to file " + save_to_file, fg='green')
          else:
            click.secho("Data could not be written", fg='red')
        else:
          for s in out:
            print(s)

      else:
        click.secho("Room "+ room_name + " does not exist", fg='red')


    def load_people(self, filename):
      data = ""
      try:
        data = PeopleController.importPeople(filename)
      except Exception as e:
        click.secho("Couldnt load the file, make sure it exists and try again",fg='red')
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
            click.secho("Wrong Person type ",fg='red')
          elif not (accomodation == "N" or accomodation=="Y"):
            click.secho("Want accomodation not properly set",fg='red')
          else:
            self.add_person(typ,fname,lname,accomodation)
        else:
          click.secho("Wrong data format", fg='red')

    def load_rooms(self, filename):
      data = ""
      try:
        data = RoomController.importRooms(filename)
      except Exception as e:
        click.secho("Couldnt load the file, make sure it exists and try again", fg='red')
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
            click.secho("Wrong room type", fg='red')
          else:
            self.add_room(typ,[name])
        else:
          click.secho("Wrong data format", fg='red')


    def help(self):
      usage = """
      Usage:
        #Rooms Management
          add_room <type> <name>... 
          delete_room  <name>
          show_rooms
          load_rooms <room_file>

        #People Managment
          add_person <firstname> <lastname> <type> [<accomodation>]
          delete_person <firstname> <lastname> 
          show_people
          load_people <people_file>

        #Operations
          auto_reallocate
          reallocate <firstname> <lastname> <new_room_name>
          print_allocations [<room_file>]
          print_unallocated [<room_file>]
          print_unallocated_offices [<room_file>]
          print_unallocated_living [<room_file>]
          print_room  <print_room_name>  [<room_file>]
          save_state
          exit | quit
      """
      print(usage)

