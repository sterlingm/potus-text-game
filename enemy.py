
class Enemy(object):

    def __init__(self, t, name, hp, weak, strong):
        print 'In Enemy.init'
        self.enemy_type = t
        self.name = name
        self.hp = hp
        self.weakness = weak
        self.strength = strong
        print 'Leaving Enemy.init'


    def take_action(self, action, base_damage):
        """ Executes an action on the enemy.

        Args:
            action: string key for the action
            base_damage: int for the base damage to take
        """
        print 'In Enemy.take_action'
        print action
        print base_damage

        total_dmg = base_damage 

        if action in self.weakness:
            total_dmg = total_dmg + 3
        elif action in self.strength:
            total_dmg = total_dmg - 3

        if total_dmg < 0:
            total_dmg = 0
        
        self.hp = self.hp - total_dmg


    def print_info(self):
        print 'Enemy Name: %s' % self.name
        print 'Enemy HP: %i' % self.hp





