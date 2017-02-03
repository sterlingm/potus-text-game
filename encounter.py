import character
import printing
import enemy
import random
import copy

class Encounter(object):

    def __init__(self, char, enemy, small_talk, ask):
        """ Creates an Encounter object.

        Args:
            char: Character object
            enemy: Enemy object
        """

        #print 'in Encounter.__init__'

        self.char = char
        self.enemy = enemy
        self.time = 0
        self.base_def = 5
        self.done = False
        self.small_talk_full = copy.deepcopy(small_talk)
        self.ask_full = copy.deepcopy(ask)

        self.strong_against_counter = 0
        self.time_dec = 0

        self.small_talk = copy.deepcopy(self.small_talk_full)
        self.ask = copy.deepcopy(self.ask_full)

        # Strings to describe the enemy responses
        self.enemy_resp_st_weak = ['%s rolls their eyes. "Uhh yeah, great"', 
                
'''%s gives the smallest of smiles and says whatever he thinks you want to 
hear''']

        self.enemy_resp_st_strong = [
'''%s smiles, they start talking about how great everything is! They are doing 
well, the weather is great, what a day!''', '''%s answers with a surprisingly 
positive response! They go on to ask you questions in rapid fire about your day, 
your family, and if you are LOVING this weather.''']
        
        self.enemy_resp_a_weak = [
        
'''%s inches back...they look around to see who is within earshot...they stutter 
out a simple, neutral response, clearly uncomfortable.''', '''%s takes a moment 
to think, and then they say they're really not too sure about it yet. They say 
that they need to do more research on it. Then they look around and focus on the 
closest door.''']

        self.enemy_resp_a_strong = [
        
'''%s inches close, and takes a deep breath.
They go on about what the Framers would have thought, a brief history of the 
issue, and what the current picture of the issue looks like. Then, they go on to 
tell you their opinion on the matter.''', 
        
'''%s looks surprised, and then leans in. They talk your ear off about why it's 
the correct decision, and why the other side is dead wrong.''']



    def print_intro_str(self):
        str_name = '''
        You have encountered %s!
        '''
        print str_name % self.enemy.name

        str_intro = '''%s is a %s from %s. '''
        print str_intro % (self.enemy.name, self.enemy.enemy_type, 
                self.enemy.state)

        self.enemy.print_fact()

    def print_combat_actions(self):
        printing.print_actions(self.char.combat_actions.keys())
        

    def print_action(self, action):
        line = random.sample(self.small_talk, 1)[0] if action == 'Small talk' \
                else random.sample(self.ask,1)[0]

        s = '\nYou: %s' % line
        printing.print_bold_red(s)

        if len(self.small_talk) == 0:
            self.small_talk = copy.deepcopy(self.small_talk_full)
        if len(self.ask) == 0:
            self.ask = copy.deepcopy(self.ask_full)

    def print_enemy_response(self, str_chosen_action):
        s = '---Enemy Response---'
        printing.print_bold_red(s)

        response_list = self.enemy_resp_st_weak

        # Set the correct response list to choose from
        if (str_chosen_action == 'Small talk' and str_chosen_action in 
                self.enemy.strength):
            response_list = self.enemy_resp_st_strong

        elif (str_chosen_action == 'Ask' and str_chosen_action in 
                self.enemy.weakness):
            response_list = self.enemy_resp_a_weak

        elif (str_chosen_action == 'Ask' and str_chosen_action in 
                self.enemy.strength):
            response_list = self.enemy_resp_a_strong

        # Choose from the response list and print the response 
        l = random.choice(response_list)
        s = l % self.enemy.name
        printing.print_bold_red(s)


    def go(self):
        """ This will start the encounter.

        This method will print the introduction and run the main loop.
        """
        self.print_intro_str()

        # Enter loop of turns        
        while not self.done:
            self.print_combat_actions()
            var = raw_input('\n')

            # Get the EncounterAction object from character list with var hotkey
            str_chosen_action = var
            if str_chosen_action == 's' or str_chosen_action == 'S':
                str_chosen_action = 'Small talk'
            elif str_chosen_action == 'a' or str_chosen_action == 'A':
                str_chosen_action = 'Ask'
            else:
                s = '******* Incorrect Input ********'
                print s
                continue



            #print 'Chosen action: %s' % str_chosen_action

            # Execute action
            self.print_action(str_chosen_action)
            self.enemy.take_action(str_chosen_action,
                    self.char.combat_actions[str_chosen_action])

            # If the enemy is strong against the chosen action, decrement the 
            # time
            if str_chosen_action in self.enemy.strength:
                self.strong_against_counter += 1

            # An enemy action is a response to the player action
            self.print_enemy_response(str_chosen_action)
                       
            # Print the enemy info after the action (mostly just for hp)
            self.enemy.print_info()

            # Check if the encounter is over
            if self.enemy.hp <= 0:
                self.done = True
                s = '\n***** Encounter Over *****'
                printing.print_blue(s)
        
        # After encounter, do a roll for making allies
        if self.enemy.enemy_type != 'Secret Service':
            print 'Enter \'y\' to persuade this person to become your ally'
            var = raw_input('\n')
            if var == 'y' or var == 'Y':
                r = random.randint(0, 15)
                if r > (self.base_def + min(0,self.enemy.hp)):
                    print 'Enemy %s added as ally!' % self.enemy.name
                    self.char.allies.append(self.enemy.name)

        # Set how much decrement the time
        self.time_dec = self.strong_against_counter / 2
              


