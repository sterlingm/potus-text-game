
class POTUSBattle:

    def __init__(self, char):
        self.char = char
        self.potus_HP = 30
        self.char_hp = 10
        self.mood = ['Aggressive', 'Calming']
        self.actions = ['Threaten', 'Reason', 'Bargain']
    

        str_intro = '''
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
        ''' Process an aggressive action against the POTUS.
        '''
        print 'In process_aggressive'

    def process_calming(self):
        ''' Process a calming action against the POTUS.
        '''
        print 'In process_calming'

    def process_threaten(self):
        ''' Process a threat action against the POTUS.
        '''
        print 'In process_threaten'

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

        print self.str_intro
         
        while self.potus_HP > 0:
            print_options()
            
            var = raw_input('\n')

            if v == 'a' or v == 'A':
                self.process_aggressive()
            elif v == 'c' or v == 'C':
                self.process_calming()


            self.potus_HP -= 1












