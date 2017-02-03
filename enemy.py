import printing

class Enemy(object):

    def __init__(self, t, name, state, fact, hp, weak, strong):
        print 'In Enemy.init'
        self.enemy_type = t
        self.name = name
        self.hp = hp
        self.weakness = weak
        self.strength = strong

        self.state = state
        self.fact = fact
        print 'Leaving Enemy.init'

    def print_fact(self):
        print self.fact % self.name


    def take_action(self, action, base_damage):
        """ Executes an action on the enemy.

        Args:
            action: string key for the action
            base_damage: int for the base damage to take
        """
        #print 'In Enemy.take_action'
        #print action
        #print base_damage

        total_dmg = base_damage 

        if action in self.weakness:
            total_dmg = total_dmg + 2
        elif action in self.strength:
            total_dmg = total_dmg - 2

        if total_dmg < 0:
            total_dmg = 0
        
        s = 'Damage: %i' % total_dmg
        printing.print_blue(s)
        self.hp = self.hp - total_dmg


    def print_info(self):
        print '\nEnemy Name: %s' % self.name
        print 'Enemy Type: %s' % self.enemy_type
        print 'Enemy HP: %i' % self.hp






