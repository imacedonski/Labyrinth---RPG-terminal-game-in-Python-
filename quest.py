from item import Item


class Quest:
    def __init__(self, name, item):
        if isinstance(item, Item):
            self.name = name
            self.reward = item
            self.monsters = 3
            self.find_item = False
        else:
            raise ValueError('Object item should be an element of Item class')

    def was_killed(self):
        return self.monsters <= 0

    def was_found(self):
        return self.find_item

    def is_done(self):
        return self.was_found() or self.was_killed()

