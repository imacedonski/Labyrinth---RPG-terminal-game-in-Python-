class Vertex:
    def __init__(self, key):
        self.id = key
        self.connected_to = []
        
    def get_id(self):
        return self.id

    def add_neighbor(self, nbr):
        self.connected_to.append(nbr)

    def get_connections(self):
        return self.connected_to

    def __str__(self):
        return f"{self.id} connected to: {[x.id for x in self.connected_to]}."
