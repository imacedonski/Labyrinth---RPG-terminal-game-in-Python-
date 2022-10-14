import random


class Enemy:
    def __init__(self, name, level, const=2):
        self.name = name
        self.level = level
        self.attack = level * const*3
        self.defence = level * const
        self.health = level * const * 6

    def get_damage(self, value):
        if value - self.defence > 1:
            self.health -= value - self.defence
            return value - self.defence
        else:
            self.health -= 1
            return 1

    def apply_damage(self):
        return self.attack

    def do_attack(self):
        if random.randint(1, 10) in range(1, 8):
            return self.apply_damage()
        else:
            return 0


