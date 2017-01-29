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
import copy

    
time_left = 30

def populateRooms(rooms, fnames, lnames, states, facts, enemy_types_dicts):
    """ Goes through the list of rooms and puts random enemies in each one

    Args:
        rooms: List of Room objects
    """
    print 'In populateRooms'
    
    for key, r in rooms.items():
        print 'Room %s' % r.name
        num_enemies = random.randint(0,2)
        print 'Number of enemies: %i' % num_enemies
        for i in range(num_enemies):
            # Randomly select type
            # TODO: Find better way to get list of types
            t = random.choice(enemy_types_dicts)
            print 'Type: %s' % t
            e = createEnemy(fnames, lnames, t, states, facts)
            e.print_info()
            r.enemies.append(e)

def process_encounter(char, enemy, small_talk_lines, ask_lines):
    ''' Does an encounter with an enemy

    Args:
        char: Character instance
        enemy: Enemy instance
    '''
    #print 'In process_encounter'

    enc = encounter.Encounter(char, enemy, small_talk_lines, ask_lines)
    enc.go()

    # Check if enemy is dead
    if enc.enemy.hp <=0:
        char.room.enemies.remove(enemy)



def process_move(char, rooms_dict, small_talk_lines, ask_lines):
    ''' Moves the character to room r, and checks if any enemies will interact 
    with character on the way.

    Args:
        char: Character instance
        rooms_dict: dict with format ['room name': Room instance]
    Return:
        char: Updated Character instance
    '''

    char_def = 12

    
    # List all rooms to move to and get an index
    printing.print_locs(char.room.connections)
    num = input("\n")

    #all_enemies = copy.deepcopy(char.room.enemies)

    i = 0
    while i < len(char.room.enemies):
        # do stuff
        e = char.room.enemies[i]

        # Roll 1d20
        roll = random.randint(0,20)
        
        # If enemy loves small talk, they get a huge bonus
        if e.strength == 'Small talk':
            roll += 10

        # Check if the roll was high enough
        if roll > char_def:
            # Start encounter
            print '\nUh-oh, %s wants to talk to you!' % e.name
            process_encounter(char, e, small_talk_lines, ask_lines)
            i-=1

        i+=1

    # Check if any enemies will interact with the character

    # Switch the Character's room
    char.switch_room(rooms_dict[ char.room.connections[num] ])

    return char




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

def createEnemy(fnames, lnames, t, states, facts):
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

    state = random.choice(states)
    fact = random.choice(facts)

    e = enemy.Enemy(t['Type'], fname + " " + lname, state, fact, t['HP'], 
            t['Weakness'], t['Strength'])
    return e

    
def get_text_encounters():
    d = os.path.dirname(__file__)
    print 'd: %s' % d
    d_full_text = os.path.join(d, 'text')
    print 'd_full_text: %s' % d_full_path
    fname_small = d_full_text.path.join(d_full_text, 'small_talk.txt')
    print fname_small
    fname_ask = d_full_text.path.join(d_full_text, 'ask.txt')
    print fname_ask

    small_talk_lines = open(fname_small).read().split('\n')
    ask_lines = open(fname_ask).read().split('\n')

    if '' in small_talk_lines:
        small_talk_lines.remove('')
    if '' in ask_lines:
        ask_lines.remove('')

    print small_talk_lines
    print ask_lines


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


    print 'd: %s' % d
    d_text = os.path.join(d, 'text')
    print 'd_text: %s' % d_text
    fname_small = os.path.join(d_text, 'small_talk.txt')
    print fname_small
    fname_ask = os.path.join(d_text, 'ask.txt')
    print fname_ask

    small_talk_lines = open(fname_small).read().split('\n')
    ask_lines = open(fname_ask).read().split('\n')

    if '' in small_talk_lines:
        small_talk_lines.remove('')
    if '' in ask_lines:
        ask_lines.remove('')

    print small_talk_lines
    print ask_lines


    states_filename = os.path.join(d, 'states.txt')
    print states_filename
    states = open(states_filename).read().split('\n')
    print 'After getting states'
    facts = open('./facts.txt').read().split('\n')
    print 'After getting facts'
    states.remove('')
    facts.remove('')
    print states
    print facts


    print '******Enemy Types*******'
    print enemy_types_dict
    e = createEnemy(fnames_male, lnames, enemy_types_dict[0], states, facts)
    print e
    e.print_info()
    print 'Rooms'
    rooms['Entrance'].add_enemy(e)
    rooms['Entrance'].print_info()

    # Can create Enemies, Now create list of random enemies for each room
    populateRooms(rooms, fnames_male, lnames, states, facts, enemy_types_dict)
    print 'Done populating'
    print len(rooms)
    enemy_names = []
    for r in rooms.values():
        for e in r.enemies:
            enemy_names.append(e.name)
    print 'Enemy Names:'
    print enemy_names

    i = random.randint(0,len(rooms)-1)
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


    #POTUSBattle_test(rooms.values(), enemy_names)

    # **********************************************************
    # **********************************************************
    # **********************************************************
    # BEGIN THE MAIN GAME LOOP
    begin(char, rooms, small_talk_lines, ask_lines)
    # **********************************************************
    # **********************************************************
    # **********************************************************
    # **********************************************************



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


def print_game_state(char):
    print("\n*********************************************")
    char.print_info()
    print '\tTime left: %d' % time_left
    print("\n*********************************************")


def begin(char, rooms, small_talk_lines, ask_lines):
    ''' Runs the main game loop

    Args:
        char: Character instance
        rooms: dict of rooms in form ['name of room': Room instance]
    '''

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
    Each room you enter may contain several employees. You may choose to 
    interact with these people, or they may interact with you. The point of 
    interacting with people is to make them your ally. If you want to really 
    hardball the President, it helps to have people in your corner. However, the
    clock is ticking so you don't want to interact with everyone.
    
    When you interact with these people, you will have two options: "Small talk" 
    or "Ask". Small talk will ask the person about the weather or about some 
    other thing nobody cares about. "Ask" will prompt you to ask the person 
    about what's going on with the current China-Muslim-Mexican conflict, or 
    something else that might press people to talk about policy.
    
    The goal is to end the interaction (you've got something to do, remember?).  
    Most types of employees will be strong or weak against a type of action. For 
    example, members of Congress like to seem friendly, but they hate being 
    asked hard questions. If you encounter one, don't even think about trying to
    "Small talk" them, that's their livelihood. "Ask" them something about 
    policy though? They'll be flying away.

    After an encounter, you can try to make the employee one of your allies.

    Interacting with an employee takes time so make sure you don't get caught up
    talking to 1 employee for too long! Do your best to end the encounter, make 
    an ally, and keep moving towards the President! The clock is ticking!
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
    

    reached_potus = False
    done = False

    # Begin the main loop to play the game
    while not done:

        if char.room.name == 'Oval Office':
            reached_potus = True
            break

        # Print "You are now in ..."
        printing.print_room_status(char.room)

        # New iteration
        # Print the list of actions and get input
        printing.print_actions(str_actions)
        var = raw_input('\n')

        if var == 'm' or var == 'M':

            char = process_move(char, rooms, small_talk_lines, ask_lines)

            # List all rooms to move to
            #printing.print_locs(char.room.connections)
            #num = input("\n")
            
            # Get the room and call switch_room
            #r = rooms[char.room.connections[num]]
            #char.switch_room(rooms[ char.room.connections[num] ])

        elif var == 'l' or var == 'L':
            # **************************************************
            # Write a description of each room in its file
            # and always print the description first
            # **************************************************

            # Print Room info
            print_game_state(char)


        elif var == 'i' or var == 'I':
            printing.print_enemies(char.room.enemies)
            num = input('\n')

            e = char.room.enemies[num]

            process_encounter(char, e, small_talk_lines, ask_lines)
            
        elif var == 'q' or var == 'Q':
            break
        
        print_game_state(char)


    # Encounter with President
    if reached_potus:
        p = potus_battle.POTUSBattle(char, 20)
        p.battle()
    
    print 'Game over'


        

    

if __name__ == '__main__':
    try:
        main()
    except:
        pass
