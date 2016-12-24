

class Room(object):

    def __init__(self, name):
        self.name = name
        self.connections = []


    # Connections are stored as strings of the room names
    def add_connector(self, room):
        self.connections.append(room)

    def add_connectors(self, rooms):
        for r in rooms:
            self.add_connector(r)

    def print_info(self):
        print("\nRoom:" + self.name)
        print("Connections:")
        for c in self.connections:
            print("\t%s" % c)
