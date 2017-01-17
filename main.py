#!/usr/bin/env python
import character
import room
import time
import sys
import os
import printing
import enemy
import encounter
import random
import potus_battle

    


def populateRooms(rooms, fnames, lnames, enemy_types_dicts):
    """ Goes through the list of rooms and puts random enemies in each one

    Args:
        rooms: List of Room objects
    """
    print 'In populateRooms'
    
    for key, r in rooms.items():
        print 'Room %s' % r.name
        num_enemies = random.randint(1,3)
        print 'Number of enemies: %i' % num_enemies
        for i in range(num_enemies):
            # Randomly select type
            # TODO: Find better way to get list of types
            t = random.choice(enemy_types_dicts)
            print 'Type: %s' % t
            e = createEnemy(fnames, lnames, t)
            e.print_info()
            r.enemies.append(e)




def get_enemy_info_dicts(direc):
    """ Builds a list of dictionaries containing information for each enemy 
    type.

    Args:
        direc: Directory containing the enemy type files

    Return:
        result: List of dictionaries where each element corresponds to different 
        enemy type
    """
    print 'In get_enemy_info'
    result = []
    print direc
    li = os.listdir(direc)
    print li
    for filename in li:
        print filename
        p = os.path.join(direc, filename)
        # Follow code in createRoom(filename) below 
        lines = open(p).read().split('\n')
        print lines
        enemy_info = {'Type': lines[0], 'HP': int(lines[1]), 'Weakness': 
                lines[2], 'Strength': lines[3]}
        print enemy_info
        result.append(enemy_info)
    return result

def createEnemy(fnames, lnames, t):
    """ Create an instance of the Enemy class.

    Args:
        fnames: List of possible first names
        lnames: List of possible last names
        t: Dictionary containing enemy type information

    Return:
        Enemy instance
    """
    print 'In createEnemy'
    fname = random.choice(fnames)
    lname = random.choice(lnames)
    print fname
    print lname

    e = enemy.Enemy(t['Type'], fname + " " + lname, t['HP'], t['Weakness'], 
            t['Strength'])
    return e

    



def createRoomsFromDir(direc):
    #print("In createRoomsFromDir, direc: %s" % direc)
    rooms = []
    rooms_dict = {'item1' : 1}
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
    d_full_rooms = os.path.join(d, 'rooms')
    d_full_enemy_types_dict = os.path.join(d, 'enemy_types')
    print d_full_rooms
    print d_full_enemy_types_dict
    rooms = createRoomsFromDir(d_full_rooms)
    print 'Rooms found:'
    for key, value in rooms.items():
        value.print_info()

    # Once everything is initialized, begin game
    char = character.Character("sterling", rooms['Entrance'])

    enemy_types_dict = get_enemy_info_dicts(d_full_enemy_types_dict)
    #print enemy_types_dict

    d_names = os.path.join(d, 'names')
    fnames_male_filename = os.path.join(d_names, 'first_names_male.txt')
    fnames_female_filename = os.path.join(d_names, 'first_names_female.txt')
    lnames_filename = os.path.join(d_names, 'last_names.txt')
    print 'after getting filename'

    print fnames_male_filename

    fnames_male = open(fnames_male_filename).read().split('\n')
    fnames_female = open(fnames_female_filename).read().split('\n')
    lnames = open(lnames_filename).read().split('\n')

    # Remove '' from lists
    fnames_male.remove('')
    fnames_female.remove('')
    lnames.remove('')
    print fnames_male
    print fnames_female
    print lnames

    print '******Enemy Types*******'
    print enemy_types_dict
    e = createEnemy(fnames_male, lnames, enemy_types_dict[0])
    print e
    e.print_info()
    print 'Rooms'
    rooms['Entrance'].add_enemy(e)
    rooms['Entrance'].print_info()

    
    # Can create Enemies, Now create list of random enemies for each room
    populateRooms(rooms, fnames_male, lnames, enemy_types_dict)
    print 'Done populating'
    print len(rooms)
    enemy_names = []
    for r in rooms.values():
        for e in r.enemies:
            enemy_names.append(e.name)
    print 'Enemy Names:'
    print enemy_names

    i = random.randint(0,len(rooms))
    print 'i: %i' % i
    keys = rooms.keys()
    print keys[i]
    print rooms[keys[i]]


    # rooms is a dict with format {'key': Room}
    #rooms[keys[i]].potus = True
    rooms['Oval Office'].potus = True
    
    print '************ Reprinting Room info ************'
    for key,r in rooms.items():
        r.print_info()


    POTUSBattle_test(rooms.values(), enemy_names)

    #begin(char, rooms)


def POTUSBattle_test(rooms, enemy_names):
    # Create random game instance to test POTUSBattle
    print 'Creating random character'
    char_random = character.Character.randomChar(rooms, enemy_names)
    char_random.print_info()
    for e in char_random.allies:
        print e
    print 'Created random character'

    time_left = random.randint(0,25)
    print 'Random time_left: %i' % time_left

    os.system('reset')
    p_test = potus_battle.POTUSBattle(char_random, time_left)
    p_test.battle()



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

    str_loc = '''
    Your location is the entrance to the West Wing of the White House.
    This part of the White House is home to the Oval Office, the Cabinet Room, 
    and other offices of the Executive Branch.
    The President roams these halls throughout the day, discussing various 
    matters with his staff, and letting everybody know how cool he is.
    
    '''

    str_rules = '''
    Each room you enter may contain several employees. An employee may have 
    useful information for you, such as rumors or clues about the President's 
    location, or they could have no information. They could also want to talk to
    you and figure out what you're up to. Most employees will have certain 
    strengths and weaknesses to the various interactions you can make with them,
    such as small talk.

    Interacting with an employee takes time so make sure you don't get caught up
    talking to 1 employee for too long! Do your best to get information from the
    useful employees, and get past the useless ones as fast as possible!

    '''
    str_story = '''
    Today, a phone call from the China-Mexico-Muslim Alliance was received.  
    According to your sources, the Alliance wanted to ensure that the President 
    saw their latest Tweet that read "Murica don't do nuttin cept lose to us in
    errthang, fatties". The POTUS was heard furiously screaming throughout the 
    entire West Wing. The entire Twitter department has been fired, and now the 
    President feels that his only choice is to press the big red button. Nobody 
    knows what the big red button does, but we're pretty sure it nukes people. 
    
    '''

    str_task = '''
    Your task is to find the President and calm him down. Explore the West Wing,
    gather information from the people in the offices about the President's 
    location, and make sure to find him FAST before he does anything 
    irreversible! It is up to YOU to stop him from pushing the

    '''


    str_game_over = '''
    ******************************************************************
    ******************************************************************
    *****************************************************************
                                GAME OVER
    ******************************************************************
    ******************************************************************
    *****************************************************************
    '''

    # Print the opening message
    #print str_wel
    #print str_intro
    #printing.print_brb()
    #print 'Press Enter to begin'
    #time.sleep(1.0)

    # Print the game introduction
    #printing.delay_print(str_story)
    #printing.delay_print(str_task)
    #print str_loc
    #print str_story
    #print str_task
    
    #time.sleep(0.2)
    #printing.print_brb()

    #printing.delay_print(str_loc)
    #printing.delay_print(str_rules)


    str_prompt = "\nChoose an action"
    str_actions = ['Move','Interact','Look Around','Quit']
    
    #printing.print_actions(str_actions)



    # Build EncounterAction objects
    # char is a Character object passed in
    # Create an enemy
    #print 'Creating Enemy'
    #e = enemy.Enemy(0, 'James McCotter', 10, ['Small talk'], [])
    #enc = encounter.Encounter(char, e)
    #enc.print_intro_str()
    #enc.go()
    

    # Encounter with President
    p = potus_battle.POTUSBattle(char, 20)
    p.print_options()
    p.battle()
    

    done = False

    # Begin the main loop to play the game
    while not done:

        if char.room.potus:
            print str_game_over
            break


        # New iteration
        # Print the list of actions and get input
        printing.print_actions(str_actions)
        var = raw_input('\n')

        if var == 'm' or var == 'M':

            # List all rooms to move to
            printing.print_locs(char.room.connections)
            num = input("\n")
            
            # Get the room and call switch_room
            r = rooms[char.room.connections[num]]
            char.switch_room(rooms[ char.room.connections[num] ])

        elif var == 'l' or var == 'L':
            # **************************************************
            # Write a description of each room in its file
            # and always print the description first
            # **************************************************

            # Then, print the enemies seen in the room:
            print 'Enemies:'
            for e in char.room.enemies:
                e.print_info()

        elif var == 'i' or var == 'I':
            printing.print_enemies(char.room.enemies)
            #e = enemy.Enemy(0, 'James McCotter', 10, ['Small talk'], [])
            #enc = encounter.Encounter(char, e)
            #enc.print_intro_str()
            #enc.go()
            num = input('\n')

            e = char.room.enemies[num]
            print e
            print e.name

            enc = encounter.Encounter(char, e)
            enc.go()
            if enc.enemy.hp <= 0:
                char.room.enemies.remove(e)
            # Else, game over?
            else:
                print str_game_over
            
            
        elif var == 'q' or var == 'Q':
            break
        
        # Print character info
        print("\n***************Character Status**************")
        char.print_info()
        print("\n*********************************************")



        

    

if __name__ == '__main__':
    try:
        main()
    except:
        pass
