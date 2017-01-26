import room
import random

class Character(object):

    def __init__(self, name, room):
        """ Creates a Character object.

        Args:
            name: string for a name
            room: Room object for the char's inital location
        """
        self.name = name
        self.room = room

        # List of actions available to the player
        self.actions = ['Move','Interact','Look Around','Quit Game']

        # The keys map to the base damage of the action
        self.combat_actions = {'Small talk': 3, 'Ask': 3}

        # List of allies the character has recruited
        self.allies = []

        #self.dmg_bonus = 2

        # True for small talk
        self.combat_move = False 

    @classmethod
    def randomChar(cls, room_list, enemies_list):
        ''' Creates a Character instance with random values.

            Args:
                room_list: List of Room objects to choose from
                enemies_list: List of strings corresponding to enemies in the 
                environment
            
            Return:
                Character instance
        '''
        #print 'In character.randomChar()'
        name = 'Random Character'
        r = random.choice(room_list)
        result = cls(name, r)
        
        # List of allies the character has recruited
        num = random.randint(0,10)
        used = []
        while len(result.allies) < num:
            rand_i = random.randint(0,len(enemies_list))
            if rand_i not in used:
                result.allies.append(enemies_list[rand_i])
                used.append(rand_i)
        return result

    def print_info(self):
        str_info = "\n\tName: %s\n\tRoom: %s" % (self.name, self.room.name)
        print str_info
        print 'List of allies:'
        print self.allies

    def switch_room(self, room):
        """ Sets the Character's room attribute

        Args:
            room: Room object
        """
        self.room = room

    
