from model import Amity,Room,Office,Living, People, Staff, Fellow
from controller import PeopleController,RoomController,OfficeController, LivingController, FellowController, StaffController

#choice1
def add_room(typ="office", rooms=[]):
  message = ""
  for room in rooms:
    if typ == "office" or typ is None:
      message =  OfficeController.new(Office,{"name": room})
    elif typ =="living":
      message =  LivingController.new(Living,{"name": room})
    else:
      print( typ, " is wrong room type")

    if isinstance(message,Room):
      print(room," ", typ ," room has been created!!")
    else:
      print(message)

def show_rooms():
  rooms = Room.getAllRooms()
  count = 0
  print("----------------------------------------------------------")
  print("SN", "\t| ", "Name", '\t\t| ', "Type" )
  print("----------------------------------------------------------")
  for room in rooms: 
    count+=1
    print(count, "\t| ", str(room.get('name')), '\t\t| ', str(room.get('type')))


def delete_room(index):
  index = int(index) - 1
  rooms = Room.getAllRooms()
  count_rooms = len(rooms)
  if count_rooms >0 and index < count_rooms:
    room = rooms[index]
    room_name = room.get('name')
    if RoomController.delete(room):
      print(room_name, " room delete successfull")
    else:
      print("Failed to delete the room")


def add_person(typ="fellow", fname="",lname="",accomodation="N"):
  person = None
  message= ""
  accm = "N"
  if accomodation.lower() == "y":
    accm = "Y"

  if typ == "staff":
    message = StaffController.new(Staff,{"firstname":fname, "lastname":lname,"accomodation":accm})
  if typ  == "fellow":
    message = FellowController.new(Fellow, {"firstname":fname, "lastname":lname,"accomodation":accm})


  if isinstance(message,People):
    print(fname, " " , lname , " Added successfully")
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


def show_people():
  people = People.getAllPeople()
  count = 0
  print("--------------------------------------------------------------------------------------")
  print("SN", "\t| ", "Firstname", "\t\t| ","Lastname",'\t\t| ', "Type" )
  print("---------------------------------------------------------------------------------------")
  for person in people: 
    count+=1
    print(count, "\t| ", str(person.get('firstname')),'\t\t| ',str(person.get('lastname')),'\t\t| ', str(person.get('type')))


def delete_person(index):
  index = int(index) - 1
  people = People.getAllPeople()
  count_people = len(people)
  if count_people >0 and index < count_people:
    person = people[index]
    person_name = person.get('firstname') + " " + person.get("lastname")
    if PeopleController.delete(person):
      print(person_name, " record has delete successfull")
    else:
      print("Failed to delete the ", person_name)


def reallocate(fname="",lname="",room_name=""):
  fname = str(fname)
  lname = str(lname)
  room_name = str(room_name)
  room = Office.findWhere({"name":room_name})
  if room is None:
    room = Living.findWhere({"name":room_name})
  if room is None:
    print("Room with the name ",room_name," does not exists")
  else:
    person = Staff.findWhere({"firstname":fname,"lastname":lname})
    if person is None:
      person = Fellow.findWhere({"firstname":fname,"lastname":lname})
    if person is None:
      print("Person with the names ",fname + lname," does not exists")
    else:
      if RoomController.reallocate(room,person):
        print(fname," ", lname, " reallocated to " ,room_name)


def auto_reallocate():
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

def print_allocations(save_to_file=None):
  rooms = Room.getAllRooms()
  
  #loop through the rooms to get the ids of people who have been assigned
  for room in rooms:
    allocations=room.getOccupants()
    out = []

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

def print_unallocated(save_to_file=None):
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
    for person_id in allocated:
      if str(person_id) == str(person.oid()):
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


def print_room(room_name="",save_to_file=None ):
  room = Office.findWhere({"name":room_name})
  if room is None:
    room = Living.findWhere({"name":room_name})
  
  if not room is None:
    allocations = room.getOccupants()
    count = 0
    out = []

    out.append("---------------------------------------------------------------------")
    out.append(room.get("name") + " Total occupants " + str(len(room.getOccupants())))
    out.append("---------------------------------------------------------------------")
    out.append("SN\t| Firstname\t\t| Lastname\t\t| Type")   
    out.append("---------------------------------------------------------------------")
    for person_id in allocations:
      person = Staff.find(person_id)
      if person is None:
        person = Fellow.find(person_id)

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


def load_people(filename):
  data = PeopleController.importPeople(filename)
  if isinstance(data,list):
    for datum in data:
      if len(datum) == 4:
        fname = datum[0]
        lname = datum[1]
        typ = datum[2].lower()
        accomodation = datum[3].title()

      if len(datum) == 3:
        fname = datum[0]
        lname = datum[1]
        typ = datum[2].lower()
        accomodation = "N"

      if not (typ == "fellow" or typ == "staff"):
        print("Wrong Person type ")
      elif not (accomodation == "N" or accomodation=="Y"):
        print("Want accomodation not properly set")
      else:
        add_person(typ,fname,lname,accomodation)


