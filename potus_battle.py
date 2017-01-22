import os
import random
import printing
import time

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


        self.win_threshold = 18

        self.init_potus_text()

        self.last_response = ''

        self.won = False

        self.threaten_attempt_flag = 1
        self.reason_attempt_flag = 2
        self.bargain_attempt_flag = 3
        self.win_attempt = 0


        #print 'Aggro:'
        #print self.potus_aggressive
        #print 'Calm'
        #print self.potus_calm

        self.str_intro = '''
            You walk into the office and look around. The phone is off the hook.
            The blinds are shut. The President is pacing back and forth on the 
            other side of the room. He's yelling. "Those god damn losers. Think 
            they can beat ME huh?! Think they can grab MY pussy?! I'll go             
            high-energy all over their asses!" 

            The secretary comes in. "Sir, uhh, Mr. President, these people-" 
            "Janice! Where's Ivanka? Make sure she's wearing that pussy-guard!" 
            "Y-yes sir. Sir, these people want to-" "Hang on!" The President 
            walks over to his desk and picks up the phone. "John! How much 
            longer until its ready?"
            
            "Mr. President! Stop! You can't press the big red button!"

            The President turns and looks at you with pure disgust, waiting for 
            you to explain yourself.
        '''


        self.str_explain = '''
            You've found the President! 

            Your goal is to stop him from pressing the button. There are 3 ways 
            to stop him: 

            Threaten - You can attempt to threaten the President in response to 
            him pressing the button. The number of allies you have coming into 
            this will boost your chances of convincing him with a threat.

            Reason - You can plead with the President to find another option.  
            The time left until the button is ready will boost your chances with
            this approach.

            Before you attempt one of these, you may want to talk with the 
            President to calm him down. His anger level will be displayed, and 
            the angrier he is, the less of a chance he will listen to you.

            Be careful when choosing how to respond! The President is a complex
            person, and choosing to speak calmly will sometimes make him even 
            angrier!

        '''


        self.str_threaten = '''
            If you do this, it'll be your last day in office. We'll impeach you. 
            You'll be tried for war crimes, and we'll help them. Your Presidency 
            will be over and your legacy will be destroyed. You'll go down in 
            history as the worst person to ever set foot in this office. Now step 
            back from the button.
        '''

        self.str_reason = '''
            Mr. President, please, think. There MUST be another way. Pressing 
            the button would change the world forever. Millions of people will 
            die. The entire world will turn against us. Our nation will be hated
            forever. This is not how America acts. We have so many resources, so
            many options, we are smarter than this. Think Mr. President, think!
        '''


        self.str_won_threaten = '''
            The President stares you in the eye. He sniffs (it's deafening).  
            
            He turns towards his desk and he grabs the phone.

            "John, cancel it. We'll find something else."

            He turns back to you. "I'll remember this. Now get the fuck out of 
            my office.\n'''

        self.str_lost_threaten = '''
            The President stares you in the eye. He sniffs (it's deafening). 

            His nostrils flare, and he leans in so close you can feel his 
            breath.

            "Never...come into my office...and threaten me. I am the President 
            of the United States. You and your possee are a pack of gnats to 
            me."

            He walks past you through the door. He nods on his way out, and 
            three Secret Service men come in and grab you by the arm.\n'''

        self.str_won_reason = '''
            The President stares you in the eye. He sniffs (it's deafening).  

            He balks.

            "You're right...what was I thinking? I just...sometimes...something 
            just comes over me. I let my anger take control. Help me think of 
            another option, please."

            You sit down. You and the President sit thinking for some time. Then
            he snaps his fingers and a look of joy comes over his face. 

            "I've got it!"

            You sit up, eager to hear his complex plan that only the President 
            come concoct.

            "We'll put SANCTIONS on them!"\n'''

        self.str_lost_reason = '''
            The President stares you in the eye. He sniffs (it's deafening).  

            He smirks and grabs the phone.

            "Yeah, just 1"

            Three Secret Service come in and grab you by the arm.

            "Get the hell out. ha ha ha, AAA HA HA HA HA HA, AAAAAAAAAAA 
            HAHAHAHHAHAHAHAHAHAHAHA"\n'''

        self.str_lost_anger = '''
            The POTUS has become too angry with you.

            He screams, "Get OUT of my office! NOW! I'm the POTUS, I make this 
            decision, I'M PRESSING THE BUTTON!"

            Five Secret Service come in and grab you by the arm. You struggle, 
            but they grab both your ankles and carry you out while you flail and
            plead with anyone that will listen. But no one does.\n'''




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
        #print 'In init_potus_text'
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
        print '\n\tSay something:'
        for m in self.mood:
            print '\t\t%s/%s: %s' % (m[0].lower(), m[0].upper(), m)

        print '\n\tAttempt to:'
        for a in self.actions:
            print '\t\t%s/%s: %s' % (a[0].lower(), a[0].upper(), a)


    def process_aggressive(self):
        ''' Process an aggressive action against the POTUS. Decreases 
        self.potus_HP
        '''
        #print 'In process_aggressive'
        str_line = random.choice(self.aggressive)
        print '\n\nYou: %s' % str_line
        #print str_line

    def process_calming(self):
        ''' Process a calming action against the POTUS. Decreases self.potus_HP
        '''
        #print 'In process_calming'
        str_line = random.choice(self.calming)
        print str_line

    def process_threaten(self):
        ''' Process a threat action against the POTUS.
            
            Return:
                roll: int value for the final roll 
                
        '''
        #print 'In process_threaten'

        printing.delay_print(self.str_threaten)

        base_roll = random.randint(5,20)
        allies_mod = len(self.char.allies)
        anger_mod = self.anger / 10.0
        roll = base_roll + allies_mod - anger_mod
        print ('base: %i allies_mod: %i anger: %i anger_mod: %i roll: %i' % 
                (base_roll, allies_mod, self.anger, anger_mod, roll))
        return roll

    def process_reason(self):
        ''' Process a reason action against the POTUS.
        '''
        #print 'In process_reason'
        printing.delay_print(self.str_reason)
        
        base_roll = random.randint(5,20)
        time_mod = self.time_left / 2
        anger_mod = self.anger / 10.0
        roll = base_roll + time_mod - anger_mod
        print ('base: %i time_mod: %i anger: %i anger_mod: %i roll: %i' % 
                (base_roll, time_mod, self.anger, anger_mod, roll))
        return roll



    def process_bargain(self):
        ''' Process a bargain action against the POTUS.
        '''
        print 'In process_bargain'

    def respond(self):
        ''' Choose a random response from the POTUS and print it
        '''
        #print 'In respond'
        i = random.randint(0,1)
        if i == 0:
            response = random.choice(self.potus_calm.keys())
            self.last_response = self.potus_calm[response]
        else:
            response = random.choice(self.potus_aggressive.keys())
            self.last_response = self.potus_aggressive[response]

        # Print response string
        print 'President: %s' % response
        


    def battle(self):
        ''' Executes the main loop of the POTUS encounter.
        '''
        #print 'In battle'
        #print 'Character information:'
        #self.char.print_info()
        print self.str_explain
        print 'Press Enter to begin the encounter!'

        var = raw_input('\n')

        printing.delay_print(self.str_intro)

        roll = 0
         
        done = False
        while not done:
            self.print_options()
            print '\nPOTUS Anger Level: %i/100' % self.anger
            
            var = raw_input('\n')

            # Statements
            if var == 'a' or var == 'A':
                self.process_aggressive()
                
                # Modify anger
                if self.last_response:
                    self.anger += self.last_response[0]

            elif var == 'c' or var == 'C':
                self.process_calming()
               
                # Modify anger
                if self.last_response:
                    self.anger += self.last_response[1]


            # End moves
            elif var == 't' or var == 'T':
                roll = self.process_threaten()
                self.win_attempt = self.threaten_attempt_flag
                done = True
            elif var == 'r' or var == 'R':
                roll = self.process_reason()
                self.win_attempt = self.reason_attempt_flag
                done = True
            
            # Check if we won 
            self.won = roll > self.win_threshold
                

            if self.anger > 99:
                printing.delay_print(self.str_lost_anger)
                done = True
        
            if not done:
                self.respond()

        # Sleep for a few seconds for suspense
        #time.sleep(3)

        if self.won:
            if self.win_attempt == self.threaten_attempt_flag:
                printing.delay_print(self.str_won_threaten)
            elif self.win_attempt == self.reason_attempt_flag:
                printing.delay_print(self.str_won_reason)
        else:
            if self.win_attempt == self.threaten_attempt_flag:
                printing.delay_print(self.str_lost_threaten)
            elif self.win_attempt == self.reason_attempt_flag:
                printing.delay_print(self.str_lost_reason)




