
import os
from core import Core
from docopt import docopt, DocoptExit
import templating
import cmd
import click


templating.app_intro()
templating.intro_header()
core = Core()

class App(cmd.Cmd):
    prompt = "Amity->>> "
    # commads

    def do_help(self,  args):
      core.help()

    def do_save_state(self,  args):
      """
      Usage: save_state [<database>]
      """
      parsed_input = None
      try:
          parsed_input = docopt(self.do_save_state.__doc__, args)
      except DocoptExit  as e:
          print(e)
          return

      db = parsed_input["<database>"].lower()
      if not db:
        db = core.currentDB()

      core.save_state(db)


    def do_load_state(self,  args):
      """
      Usage: load_state <database>
      """
      parsed_input = None
      try:
          parsed_input = docopt(self.do_load_state.__doc__, args)
      except DocoptExit  as e:
          print(e)
          return

      db = parsed_input["<database>"].lower()
      core.load_state(db)

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
          response = click.confirm("Are you sure you want to delete this room?")
          if response == "n" or response == False or response == "N":
              click.secho("Delete Cancelled", fg='cyan', bold=True)
          elif response == "y" or response == "Y" or response== True: 
              core.delete_room(room_name)
          else:
              click.secho("Wrong response. response can only be n or y", fg='yellow')
        else:
            click.secho("Room name can not be empty", fg='red', bold=True)


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
          response = click.confirm("Are you sure you want to delete this person ?")         
          if response == "n" or response == False or response == "N":
              click.secho("Delete Cancelled", fg='cyan', bold=True)
          elif response == "y" or response == "Y" or response== True: 
              core.delete_person(firstname,lastname)
          else:
              click.secho("Wrong response. response can only be n or y", fg='yellow')
      else:
          click.secho("Room name can not be empty", fg='red', bold=True)



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
    



    def do_print_unallocated_office(self,  args):
        """
        Usage: print_unallocated_office [<file_name>]
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_print_unallocated_office.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return
        
        file_name = parsed_input["<file_name>"]
        core.print_unallocated_office(file_name)




    def do_print_unallocated_living(self,  args):
        """
        Usage: print_unallocated_living [<file_name>]
        """
        parsed_input = None
        try:
            parsed_input = docopt(self.do_print_unallocated_living.__doc__, args)
        except DocoptExit  as e:
            print(e)
            return
        
        file_name = parsed_input["<file_name>"]
        core.print_unallocated_living(file_name)



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


    def do_quit(self, arg):
        click.secho('Thank you for using Amity Room Allocation App', fg='green')
        exit()


    def do_exit(self, arg):
        click.secho('Thank you for using Amity Room Allocation App', fg='green')
        exit()



if  __name__ ==  "__main__" :
  app = App()
  app.cmdloop()