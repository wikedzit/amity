

"""Naval Fate.
Usage:
  app.py add_room [--room_type=<typ>] <room_name>... 
  app.py delete_room  <room_identifier>
  app.py show_rooms
  app.py add_person [--person_type=<typ>] <firstname> <lastname>  [--wants_accomodation=<yn>]
  app.py delete_person <person_identifier>
  app.py show_people
  app.py auto_reallocate
  app.py reallocate <firstname> <lastname> <new_room_name>
  app.py load_people <people_file>
  app.py load_rooms <room_file>
  app.py print_allocations [-o FILE]
  app.py print_unallocated [-o FILE]
  app.py print_room  <print_room_name>  [-o FILE]
  app.py -h | --help
  app.py -v |--version
Options:
  -h --help     Show this screen.
  -v --version  Show version.
  --room_type=<typ> Room type  [default: office].
  --person_type=<typ> Person type  [default: fellow].
  --wants_accomodation=<yn> Wants wants_accomodationn [default: N]
  -o FILE      specify output file
"""

from core import *
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Amity 1.0')
    #print(arguments)

    if arguments['add_room']:
      room_type = str(arguments['--room_type'])
      room_name = arguments['<room_name>']
      add_room(room_type,room_name)


    if arguments['show_rooms']:
      show_rooms()

    if arguments['delete_room']:
      index = arguments['<room_identifier>']
      if not index is None :
        index = int(index)
        if isinstance(index, int):
          index = (arguments['<room_identifier>'] )
          response = raw_input(" Are you sure you want to delete this room [y/n] n ?")
          if response == "n" or response == "N":
            print('Delete Cancelled')
          elif response == "y" or response == "Y": 
            delete_room(index)
          else:
            print("Wrong response. response can only be n or y")
        else:
          print("Room index should be an interger . Use command <show_rooms> to get the right index")
      else:
        print("Room index not provided. Use command <show_rooms> to get the right index")


    if arguments['add_person']:
      typ = arguments['--person_type']
      fname = arguments['<firstname>']
      lname  = arguments['<lastname>']
      accomodation = arguments['--wants_accomodation']
      add_person(typ, fname,lname,accomodation)


    if arguments['delete_person']:
      index = arguments['<person_identifier>']
      if not index is None :
        index = int(index)
        if isinstance(index, int):
          index = (arguments['<person_identifier>'] )
          response = input(" Are you sure you want to delete this person [y/n] n ?")
          if response == "n" or response == "N":
            print('Delete Cancelled')
          elif response == "y" or response == "Y": 
            delete_person(index)
          else:
            print("Wrong response. response can only be n or y")
        else:
          print("Person index should be an interger . Use command <show_people> to get the right index")
      else:
        print("Person index not provided. Use command <show_people> to get the right index")


    if arguments['show_people']:
      show_people()

    if arguments['reallocate']:
      fname = arguments['<firstname>']
      lname  = arguments['<lastname>']
      room_name = arguments['<new_room_name>']
      reallocate(fname,lname,room_name)
 
    if arguments['auto_reallocate']:
      auto_reallocate()
 
    if arguments['print_allocations']:
      filename =  arguments['-o']
      print_allocations(filename)

    if arguments['print_unallocated']:
      filename =  arguments['-o']
      print_unallocated(filename)

    if arguments['print_room']:
      room_name = arguments['<print_room_name>']
      filename =  arguments['-o']
      if room_name is None:
        print("You must specify a room")
      else:
        print_room(room_name)

    if arguments['load_people']:
      filename = arguments['<people_file>']
      if not filename is None:
        load_people(filename)
      else:
        print("Specify the file")

    if arguments['load_rooms']:
      print("Load command")


