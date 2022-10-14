from place import Place


class Graph:
    def __init__(self):
        # keys - keys (ids) of places
        # values - objects of class Places
        self.place_list = {}
        self.visited_places = {1}

    def add_place(self, key):
        new_place = Place(key)
        self.place_list[key] = new_place

    def get_place(self, key):
        if key in self.place_list:
            return self.place_list[key]
        else:
            return None

    def add_edge(self, f, t):
        if f not in self.place_list:
            self.add_place(f)
        if t not in self.place_list:
            self.add_place(t)
        self.place_list[f].add_neighbor(self.place_list[t])
        self.place_list[t].add_neighbor(self.place_list[f])

    def get_places(self):
        return self.place_list.keys()

    def __contains__(self, key):
        return key in self.place_list

    def __iter__(self):
        return iter(self.place_list.values())


