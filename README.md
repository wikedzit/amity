[![Build Status](https://travis-ci.org/wikedzit/amity.svg?branch=master)](https://travis-ci.org/wikedzit/amity)
[![Coverage Status](https://coveralls.io/repos/github/wikedzit/amity/badge.png?branch=dev-core)](https://coveralls.io/github/wikedzit/amity?branch=dev-core)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)]()
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/wikedzit)

# Amity (Room Allocation App)
Smart room allocator, a simple but yet powerfull room allocator 

## 1. About the App.

This is a basic Command line application that can be used to mange room allocations in a office or schoolenviroment where offices and accomodation rooms are shared. 
The app implementes functionalities for two main components Rooms and People. Rooms are of two types Offices and Living Space (refered to living in the app)

## 2. Constraints
>An office can contain a maximum of 6 people 
>A living space takes in a maximum of 4 people.
>Offices can be shared by both Staff and Fellows
>Staff can not be allocated a living space

## 3. Implementation
Amity has been implemented  and tested using Python 3.6, other versions of python have been tested to work fine and can be supported too. The app features two main tiers the User Interface (CLI) and the database (MngoDb and text files)


## 4. Requirements
Amit app runs on a desktop computer. To run this App you need python 3.x and MongoDb v3.2+ installed on your Computer.


## 5. Commands.

Command | Argument 
--- | ---
app.py add_room | (type) (name)...
app.py delete_room | (name)
app.py show_rooms |
app.py add_person | (firstname) (lastname) (type) [(accomodation)]
app.py delete_person | (firstname) (lastname) 
app.py show_people | 
app.py auto_reallocate | 
app.py reallocate | (irstname) (lastname) (new_room_name)
app.py load_people | (people_file)
app.py load_rooms | (room_file)
app.py print_allocations | [(room_file)]
app.py print_unallocated | [(room_file)] 
app.py print_room | (print_room_name)  [(room_file)]

## 6. Installation and set up.

1. Confirm that Python is installed on your PC
2. Download and install MongoDB [Click here for detailed instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/) I recommend using Homebrew
3. Configure python to supprt virtual environment
4. Copy or Clone this repository to your local machine using `git clone https://github.com/wikedzit/amity.git`
5. Create a **virtualenv** on your machine and activate it
6. install the dependencies via `pip install -r requirements.txt`.
7. Once all the requirements have been installed, navigate to amity/app and run python app.py

## 7. Usage

The following screencast shows how to run the different commands. Check it out:
[![asciicast](https://asciinema.org/a/8835hldn9g3y2rosclvp840t9.png)](https://asciinema.org/a/8835hldn9g3y2rosclvp840t9)


## 8. Tests.

To run nosetests ensure that you are within the *virtual environment* and have the following installed:

1. *nose*

2. *coveralls*

3. *coverage*


## Credits

1. [Timothy Wikedzi](https://github.com/wikedzit)

2. [Andela](https://www.andela.com) community.

3. [Roger Tarache]

## License

### The MIT License (MIT)

Copyright (c) 2017 [BUSINGE SCOTT [ANDELA]]

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
