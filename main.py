#!/usr/bin/env python
import character
import room
import os


def createRoomsFromDir(direc):
    #print("In createRoomsFromDir, direc: %s" % direc)
    rooms = []
    li = os.listdir(direc)
    print li
    for filename in os.listdir(direc):
        p = os.path.join(direc, filename)
        #print('Next filename %s' % p)
        rooms.append(createRoom(p))

    return rooms


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
    for r in rooms:
        r.print_info()
    

def begin(char):
    str_wel = "Welcome!"
    

    print str_wel

if __name__ == '__main__':
    try:
        main()
    except:
        pass
