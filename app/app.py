
import os
from core import Core
from docopt import docopt, DocoptExit
import templating
import cmd


templating.app_intro()
templating.intro_header()
core = Core()

class App(cmd.Cmd):
    prompt = "-> "
    # commads

    def do_help(self,  args):
      core.help()

    def do_add_room(self,  args):
        """
        Usage: add_room <type>  <name>...
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_add_room.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        room_type = parsed_input["<type>"].lower()
        room_names = parsed_input["<name>"]
        core.add_room(room_type,room_names)


    def do_show_rooms(self,  args):
        """
        Usage: show_rooms
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_show_rooms.__doc__, args)
            core.show_rooms()
        except DocoptExit  as e:
            print(e)
            return


    def do_delete_room(self,  args):
        """
        Usage: delete_room <name>
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_delete_room.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        room_name = parsed_input["<name>"]
        if room_name:
          core.delete_room(room_name)
        else:
          print("Room name can not be empty")


    def do_add_person(self, args):
      """
      Usage: add_person <firstname>  <lastname>  <type> [<accomodation>]
      """
      parsed_input = None
      try:
          parsed_input = docopt(self.do_add_person.__doc__, args)
      except DocoptExit  as e:
          print(e)
          return

      firstname = parsed_input["<firstname>"].title()
      lastname = parsed_input["<lastname>"].title()
      person_type = parsed_input["<type>"].lower()
      accomodation = parsed_input["<type>"].title()
      core.add_person(person_type,firstname,lastname,accomodation)


    def do_delete_person(self,  args):
      """
      Usage: delete_person <firstname> <lastname>
      """
      parsed_input = None
      try:
          parsed_input = docopt(self.do_delete_person.__doc__, args)
      except DocoptExit  as e:
          print(e)
          return

      firstname = parsed_input["<firstname>"]
      lastname = parsed_input["<lastname>"]

      if firstname and lastname:
        core.delete_person(firstname,lastname)
      else:
        print("Provide firstname and lastname of a person you want to delete")

    def do_show_people(self,  args):
        """
        Usage: show_people
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_show_people.__doc__, args)
            core.show_people()
        except DocoptExit  as e:
            print(e)
            return

    def do_reallocate(self, args):
      """
      Usage: reallocate <firstname>  <lastname>  <to_room_name>
      """
      parsed_input = None
      try:
          parsed_input = docopt(self.do_reallocate.__doc__, args)
      except DocoptExit  as e:
          print(e)
          return

      firstname = parsed_input["<firstname>"].title()
      lastname = parsed_input["<lastname>"].title()
      to_room_name = parsed_input["<to_room_name>"].title()
      core.reallocate(firstname,lastname,to_room_name)

    def do_auto_reallocate(self,  args):
        """
        Usage: auto_reallocate
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_auto_reallocate.__doc__, args)
            core.auto_reallocate()
        except DocoptExit  as e:
            print(e)
            return

    def do_print_allocations(self,  args):
        """
        Usage: print_allocation [<file_name>]
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_print_allocations.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        file_name = parsed_input["<file_name>"]
        core.print_allocations(file_name)

    def do_print_unallocated(self,  args):
        """
        Usage: print_unallocated [<file_name>]
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_print_unallocated.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        file_name = parsed_input["<file_name>"]
        core.print_unallocated(file_name)


    def do_print_room(self,  args):
        """
        Usage: print_room <name> [<file_name>]
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_print_room.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        room_name = parsed_input["<name>"]
        file_name = parsed_input["<file_name>"]
        core.print_room(room_name,file_name)

    def do_load_people(self,  args):
        """
        Usage: load_people <file_name>
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_load_people.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        file_name = parsed_input["<file_name>"]
        core.load_people(file_name)


    def do_load_rooms(self,  args):
        """
        Usage: load_rooms <file_name>
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_load_rooms.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return

        file_name = parsed_input["<file_name>"]
        core.load_rooms(file_name)


if  __name__ ==  "__main__" :
  app = App()
  app.cmdloop()




'''

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
          response = input(" Are you sure you want to delete this room [y/n] n ?")
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

'''

