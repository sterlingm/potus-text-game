#!/usr/bin/env python
import character
import room
import time
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
    os.system('reset')
    str_wel = "\nWelcome %s!" % char.name
    str_intro = '''
        ######################################################
        ######################################################
        ######################################################
        
        Welcome %s!\n
        You are about to play POTUS!
        Your goal: Find the President and stop him from pushing
        the\n\n
    '''
    str_big = '''


        __/\\\\\\\\\\\\\\\\\\\\\\\\\\____/\\\\\\\\\\\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\\\\\\\\\\_                                                                 
        _\\/\\\\\\/////////\\\\\\_\\/////\\\\\\///____/\\\\\\//////////__                                                                
         _\\/\\\\\\_______\\/\\\\\\_____\\/\\\\\\______/\\\\\\_____________                                                               
          _\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\______\\/\\\\\\_____\\/\\\\\\____/\\\\\\\\\\\\\\_                                                              
           _\\/\\\\\\/////////\\\\\\_____\\/\\\\\\_____\\/\\\\\\___\\/////\\\\\\_                                                             
            _\\/\\\\\\_______\\/\\\\\\_____\\/\\\\\\_____\\/\\\\\\_______\\/\\\\\\_                                                            
             _\\/\\\\\\_______\\/\\\\\\_____\\/\\\\\\_____\\/\\\\\\_______\\/\\\\\\_                                                           
              _\\/\\\\\\\\\\\\\\\\\\\\\\\\\\/___/\\\\\\\\\\\\\\\\\\\\\\_\\//\\\\\\\\\\\\\\\\\\\\\\\\/__                                                          
               _\\/////////////____\\///////////___\\////////////____                                                         
               '''
    str_red = '''


       ____/\\\\\\\\\\\\\\\\\\______/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\\\____                                                             
        __/\\\\\\///////\\\\\\___\\/\\\\\\///////////__\\/\\\\\\////////\\\\\\__                                                            
         _\\/\\\\\\_____\\/\\\\\\___\\/\\\\\\_____________\\/\\\\\\______\\//\\\\\\_                                                           
          _\\/\\\\\\\\\\\\\\\\\\\\\\/____\\/\\\\\\\\\\\\\\\\\\\\\\_____\\/\\\\\\_______\\/\\\\\\_                                                          
           _\\/\\\\\\//////\\\\\\____\\/\\\\\\///////______\\/\\\\\\_______\\/\\\\\\_                                                         
            _\\/\\\\\\____\\//\\\\\\___\\/\\\\\\_____________\\/\\\\\\_______\\/\\\\\\_                                                        
             _\\/\\\\\\_____\\//\\\\\\__\\/\\\\\\_____________\\/\\\\\\_______/\\\\\\__                                                       
              _\\/\\\\\\______\\//\\\\\\_\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_\\/\\\\\\\\\\\\\\\\\\\\\\\\/___                                                      
               _\\///________\\///__\\///////////////__\\////////////_____                                                     
               '''

    str_button = '''
       __/\\\\\\\\\\\\\\\\\\\\\\\\\\____/\\\\\\________/\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_______/\\\\\\\\\\_______/\\\\\\\\\\_____/\\\\\\_        
        _\\/\\\\\\/////////\\\\\\_\\/\\\\\\_______\\/\\\\\\_\\///////\\\\\\/////__\\///////\\\\\\/////______/\\\\\\///\\\\\\____\\/\\\\\\\\\\\\___\\/\\\\\\_       
         _\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_____________\\/\\\\\\_________/\\\\\\/__\\///\\\\\\__\\/\\\\\\/\\\\\\__\\/\\\\\\_      
          _\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\__\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_____________\\/\\\\\\________/\\\\\\______\\//\\\\\\_\\/\\\\\\//\\\\\\_\\/\\\\\\_     
           _\\/\\\\\\/////////\\\\\\_\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_____________\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\\\//\\\\\\\\/\\\\\\_    
            _\\/\\\\\\_______\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_______\\/\\\\\\_____________\\/\\\\\\_______\\//\\\\\\______/\\\\\\__\\/\\\\\\_\\//\\\\\\/\\\\\\_   
             _\\/\\\\\\_______\\/\\\\\\_\\//\\\\\\______/\\\\\\________\\/\\\\\\_____________\\/\\\\\\________\\///\\\\\\__/\\\\\\____\\/\\\\\\__\\//\\\\\\\\\\\\_  
              _\\/\\\\\\\\\\\\\\\\\\\\\\\\\\/___\\///\\\\\\\\\\\\\\\\\\/_________\\/\\\\\\_____________\\/\\\\\\__________\\///\\\\\\\\\\/_____\\/\\\\\\___\\//\\\\\\\\\\_ 
              _\\/////////////_______\\/////////___________\\///______________\\///_____________\\/////_______\\///_____\\/////__
              '''

    print str_wel
    print str_intro
    print '\033[00;31m' + str_big
    time.sleep(1)
    print str_red
    time.sleep(1)
    print str_button
    #char.print_info()

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
