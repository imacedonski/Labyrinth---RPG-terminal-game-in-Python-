import random
from item import Item
from enemy import Enemy
from quest import Quest


class Hero(Enemy):
    def __init__(self, name, level=1, const=4.5):
        super().__init__(name, level, const)
        self.equipment = {"armor": None, "weapon": None}
        # inventory: key = item.name, value = object of type Item
        self.inventory = {}
        self.backpack = {"small potion": 0, "medium potion": 0, "big potion": 0}
        self.experience = 0
        self.max_health = level * const * 6
        # active_quests: key = Quest.name, value = object of type Quest
        self.active_quests = {}

    def increase_health(self, value):
        if self.max_health >= self.health + value:
            self.health += value
        else:
            self.health = self.max_health

    def use_potion(self, name):
        if self.backpack[name] > 0 and name == 'small potion':
            self.increase_health(80)
            self.backpack[name] -= 1
        elif self.backpack[name] > 0 and name == 'medium potion':
            self.increase_health(200)
            self.backpack[name] -= 1
        elif self.backpack[name] > 0 and name == 'big potion':
            self.increase_health(400)
            self.backpack[name] -= 1
        else:
            raise ValueError('U dont have this type of potion!')

    def put_off_armor(self):
        if self.equipment["armor"] is not None:
            self.inventory[self.equipment["armor"].name] = self.equipment["armor"]
            self.defence -= self.equipment["armor"].value
            self.equipment["armor"] = None
        else:
            raise ValueError('U dont have any armor on!')

    def put_off_weapon(self):
        if self.equipment["weapon"] is not None:
            self.inventory[self.equipment["weapon"].name] = self.equipment["weapon"]
            self.attack -= self.equipment["weapon"].value
            self.equipment["weapon"] = None
        else:
            raise ValueError('U dont have any weapon on!')

    def put_on(self, name):
        if name in self.inventory and self.inventory[name].type != 'quest':
            # if we already have item of this type on - first we put this current item off and then we put new item on
            if self.equipment[self.inventory[name].type] is not None and self.inventory[name].type == "armor":
                self.put_off_armor()
                self.equipment["armor"] = self.inventory[name]
                self.defence += self.inventory[name].value
                del self.inventory[name]
            elif self.equipment[self.inventory[name].type] is not None and self.inventory[name].type == "weapon":
                self.put_off_weapon()
                self.equipment["weapon"] = self.inventory[name]
                self.attack += self.inventory[name].value
                del self.inventory[name]
            elif self.equipment[self.inventory[name].type] is not None:
                raise ValueError('U can put on only weapon/armor!')
            elif self.equipment[self.inventory[name].type] is None and self.inventory[name].type == "armor":
                self.equipment["armor"] = self.inventory[name]
                self.defence += self.inventory[name].value
                del self.inventory[name]
            elif self.equipment[self.inventory[name].type] is None and self.inventory[name].type == "weapon":
                self.equipment["weapon"] = self.inventory[name]
                self.attack += self.inventory[name].value
                del self.inventory[name]
        elif name in self.inventory and self.inventory[name].type == 'quest':
            raise TypeError('You cant wear items of type quest!')
        else:
            raise ValueError('You dont have this item in inventory!')

    def add_quest(self, quest):
        if isinstance(quest, Quest):
            self.active_quests[quest.name] = quest
        else:
            raise ValueError('U can only add to quests object of type Quest!')

    def get_item(self, item):
        if isinstance(item, Item) and item.type != 'potion':
            self.inventory[item.name] = item
        elif isinstance(item, Item) and item.type == 'potion':
            self.backpack[item.name] += 1
        else:
            raise ValueError('U can add to inventory only objects of type Item')

    def get_reward(self):
        to_del = None
        for quest in self.active_quests.values():
            if quest.is_done():
                self.get_item(quest.reward)
                to_del = quest.name
        if to_del is not None:
            del self.active_quests[to_del]
            print('You have done the quest! The reward is now in your inventory.')

    def light_strike(self):
        return random.randint(1, 10) in range(1, 9)

    def strong_strike(self):
        return random.randint(1, 10) in range(1, 5)

    def do_attack(self, strong=False):
        if strong:
            if self.strong_strike():
                return 5 * self.apply_damage()
            return 0
        if self.light_strike():
            return 2 * self.apply_damage()
        return 0

    def get_experience(self):
        self.experience += 1

    def lvl_up(self, const=4):
        if self.experience == 3:
            self.level += 1
            self.attack += const*6
            self.max_health += const * 10
            self.defence += const*5
            self.experience = 0
        # this constance = 4 is connected with difficulties of game, it can be changed if it's necessary

    def quest_item(self):
        for item_name in self.inventory:
            if item_name in self.active_quests:
                self.active_quests[item_name].find_item = True

    def check_item(self, name):
        if name in self.inventory:
            print(f'Type of item {name} is {self.inventory[name].type}. Value = {self.inventory[name].value}')
        else:
            raise ValueError('You dont have this item in your inventory!')

    def show_equipment(self):
        weapon = self.equipment['weapon']
        armor = self.equipment['armor']
        if weapon is None and armor is None:
            print('Weapon: -, Armor: -.')
        elif weapon is None and armor is not None:
            print(f'Weapon: -, Armor: {armor.name}.')
        elif weapon is not None and armor is None:
            print(f'Weapon: {weapon.name}, Armor: -.')
        else:
            print(f'Weapon: {weapon.name}, Armor: {armor.name}.')

    def drop_item(self, name):
        if name in self.inventory:
            del self.inventory[name]
        else:
            raise ValueError('You dont have this item!')

'''
if __name__ == "__main__":
    test = Hero('Waldemar', 1)
    sword = Item('sword', 'weapon', 10)
    test.get_item(sword)
    test.put_on('sword')
    test.get_experience()
    test.get_experience()
    test.get_experience()
    print(test.experience)
    print(test.attack)
    test.lvl_up()
    print(test.equipment['weapon'])
    print(test.attack)
'''

