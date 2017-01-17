import os
import random

class POTUSBattle(object):

    def __init__(self, char, time_left):
        self.char = char
        self.potus_HP = 30
        self.char_hp = 10
        self.mood = ['Aggressive', 'Calming']
        self.actions = ['Threaten', 'Reason', 'Bargain']
        self.time_left = time_left

        self.aggressive = self.load_text('aggressive')
        self.calming = self.load_text('calming')
        self.threaten = self.load_text('threaten')
        self.reason = self.load_text('reason')
        self.bargain = self.load_text('bargain')
    
        self.aggressive_count = 0
        self.calming_count = 0

        self.anger = random.randint(50,90)

        # potus_aggressive and potus_calm are dict object.
        # with format {'string': [int,int]} where the string object
        # is the phrase the potus says, and the list is the int to
        # modify self.anger by, the first element is if the player responds
        # aggressively and the 2nd element is if the player responds calmly
        self.potus_aggressive = {}
        self.potus_calm = {}

        self.init_potus_text()
        print 'Aggro:'
        print self.potus_aggressive
        print 'Calm'
        print self.potus_calm

        self.str_intro = '''
            You walk into the office and look around. The phone is off the hook.
            The blinds are shut. The President is pacing back and forth on the 
            other side of the room. He's yelling. "Those god damn losers. Think 
            they can beat ME huh?! Think they can grab MY pussy?! I'll go             
            high-energy all over their  .

            The secretary comes in. "Sir, uhh, Mr. President, these people-" 
            "Janice! Where's Ivanka? Make sure she's wearing that pussy-guard!" 
            "Y-yes sir. Sir, these people want to-" "Hang on, I've got something
            to do first!" The President walks over to his desk and picks up the 
            phone. "John! Ready the button."
            
            "Mr.  President! Stop! You can't press the big red button!"
        '''


    def load_text(self, category):
        ''' Return the list of strings for the category.

            Args:
                category: string with value 'aggressive', 'calming', or other 
                filname (no extension) from the 'text' directory
        '''
        #print 'In load_text'
        d = os.path.dirname(__file__)
        d_full_text = os.path.join(d, 'text')
        fname = os.path.join(d_full_text, category+'.txt')
        lines = open(fname).read().split('\n')
        return lines

    def init_potus_text(self):
        ''' Initializes the dict objects for potus_aggressive and potus_calm
        '''
        print 'In load_potus_text'
        d = os.path.dirname(__file__)
        d_full_path = os.path.join(d, 'text/potus')
        li = os.listdir(d_full_path)
        for filename in li:
            fname_full = os.path.join(d_full_path, filename)
            lines = open(fname_full).read().split('\n')
            for l in lines:
                if l:
                    strs = l.split('|')
                    mods = strs[1].split(',')
                    mods = map(int, mods)
                    if filename == 'potus_aggressive.txt':
                        self.potus_aggressive[strs[0]] = mods
                    else:
                        self.potus_calm[strs[0]] = mods

        



    def print_options(self):
        ''' Prints the list of options for the character to choose from.
        '''
        print 'Your options:'

        print '\tSay something:'
        for m in self.mood:
            print '\t%s/%s: %s' % (m[0].lower(), m[0].upper(), m)

        print '\n\tAttempt to:'
        for a in self.actions:
            print '\t%s/%s: %s' % (a[0].lower(), a[0].upper(), a)


    def process_aggressive(self):
        ''' Process an aggressive action against the POTUS. Decreases 
        self.potus_HP
        '''
        print 'In process_aggressive'
        str_line = random.choice(self.aggressive)
        print str_line
        dmg = 5 + len(self.char.allies)
        print 'dmg: %s' % dmg
        self.potus_HP -= dmg

    def process_calming(self):
        ''' Process a calming action against the POTUS. Decreases self.potus_HP
        '''
        print 'In process_calming'
        str_line = random.choice(self.aggressive)
        print str_line
        dmg = 5 + (time_left / 2)
        print 'dmg: %s' % dmg
        self.potus_HP -= dmg

    def process_threaten(self):
        ''' Process a threat action against the POTUS.
        '''
        print 'In process_threaten'

        str_line = random.choice(self.threaten)
        print str_line

        base_roll = randint(1,20)
        allies_mod = len(self.char.allies)
        anger_mod = self.anger / 10.0
        roll = base_roll + allies_mod - anger_mod
        print ('base: %i allies_mod: %i anger: %i anger_mod: %i roll: %i' % 
                (base_roll, allies_mod, self.anger, anger_mod, roll))

    def process_reason(self):
        ''' Process a reason action against the POTUS.
        '''
        print 'In process_reason'

    def process_bargain(self):
        ''' Process a bargain action against the POTUS.
        '''
        print 'In process_bargain'


    def battle(self):
        ''' Executes the main loop of the POTUS encounter.
        '''
        print 'In battle'
        print 'Character information:'
        self.char.print_info()
        print self.str_intro
         
        done = False
        while not done:
            self.print_options()
            
            var = raw_input('\n')
            print var

            if var == 'a' or var == 'A':
                self.process_aggressive()
                self.aggressive_count += 1

            elif var == 'c' or var == 'C':
                self.process_calming()
                self.calming_count += 1

            elif var == 't' or var == 'T':
                self.process_threaten()

            elif var == 'r' or var == 'R':
                self.process_reason()

            elif var == 'b' or var == 'B':
                self.process_bargain()

            print 'POTUS HP: %i' % self.potus_HP
            if self.potus_HP < 1:
                done = True











