#!/usr/bin/env python
import character
import room
import os


def createRoomsFromDir(direc):
    #print("In createRoomsFromDir, direc: %s" % direc)
    rooms = []
    rooms_dict = {'item1' : 1}
    li = os.listdir(direc)
    print li
    for filename in os.listdir(direc):
        p = os.path.join(direc, filename)
        #print('Next filename %s' % p)
        r = createRoom(p)
        r.print_info()
        rooms_dict[r.name] = r

    del rooms_dict['item1']
    return rooms_dict


def createRoom(filename):
    #print('In createRoom, filename: %s' % filename)
    
    lines = open(filename).read().split('\n')
    r = room.Room(lines[0])
    s = lines[1].split(',')
    r.add_connectors(s)

    return r
    

def main():
    d = os.path.dirname(__file__)
    d_full = os.path.join(d, 'rooms')
    print d_full
    rooms = createRoomsFromDir(d_full)
    print 'Rooms found:'
    for key, value in rooms.items():
        value.print_info()

    # Once everything is initialized, begin game
    char = character.Character("sterling", rooms['Entrance'])
    begin(char, rooms)

def begin(char, rooms):
    str_wel = "\nWelcome %s!" % char.name
    print str_wel
    char.print_info()

    str_prompt = "\nChoose an action"
    str_actions = "\nMove, Interact"
    
    print str_prompt + str_actions

    
    while True:
        var = raw_input("Enter a choice\n")
        if var == 'm' or var == 'M':
            # List all rooms to move to
            s = len(char.room.connections)
            str_rooms = (" %s"*s % tuple(char.room.connections))
            print "\nConnecting rooms:" + str_rooms

            num = input("Enter a number\n")
            r = rooms[char.room.connections[num]]
            

            char.switch_room(rooms[ char.room.connections[num] ])
            char.print_info()

            
        elif var == 'q' or var == 'Q':
            break




    # List all people to talk to


    

if __name__ == '__main__':
    try:
        main()
    except:
        pass
