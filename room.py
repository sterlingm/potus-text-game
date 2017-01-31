

class Room(object):

    def __init__(self, name, time):
        self.name = name
        self.connections = []
        self.enemies = []
        self.potus = False
        self.time_dec = time


    # Connections are stored as strings of the room names
    def add_connector(self, room):
        self.connections.append(room)

    def add_connectors(self, rooms):
        for r in rooms:
            self.add_connector(r)

    def add_enemy(self, e):
        """ Adds an enemy to the room

        Args:
            e: Enemy instance
        """
        print 'In room.add_enemy'
        self.enemies.append(e)

    def print_info(self):
        print 'In print_info, name: %s' % self.name
        print '\nRoom:' + self.name
        print 'Connections:'
        for c in self.connections:
            print("\t%s" % c)
        print 'Enemies:'
        for e in self.enemies:
            e.print_info()
        print 'Time decrement: %i' % self.time_dec
