from item import Item
from enemy import Enemy
from npc import NPC
from vertex import Vertex


class Place(Vertex):
    def __init__(self, key):
        super().__init__(key)
        self.chest = []
        self.enemies = []
        self.npc = None

    def add_npc(self, npc):
        if isinstance(npc, NPC):
            self.npc = npc
        else:
            raise ValueError('Wrong type')

    def add_item(self, item):
        if isinstance(item, Item):
            self.chest.append(item)
        else:
            raise ValueError('Wrong type')

    def add_enemy(self, enemy):
        if isinstance(enemy, Enemy):
            self.enemies.append(enemy)
        else:
            raise ValueError('Wrong type')

    def get_enemies(self):
        return self.enemies

    def kill_enemy(self, name):
        val = False
        for enemy in self.enemies:
            if enemy.name == name:
                self.enemies.remove(enemy)
                val = True
                break
        if not val:
            raise ValueError('This enemy is not in this place, so u can not kill it ')


