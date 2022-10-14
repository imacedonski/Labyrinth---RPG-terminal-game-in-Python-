from graph import Graph
from hero import Hero
from item import Item
from npc import NPC
from quest import Quest
from enemy import Enemy
import networkx as nx
import matplotlib.pyplot as plt
import pickle


class Game:
    def __init__(self, world=None, hero=None, id=None):
        self.view = None
        self.pos = None
        self.world = world
        self.hero = hero
        # id of place in Graph
        self.current_place = id
        self.list_of_commands = ['go to', 'fight', 'take items', 'show ways', 'show npc', 'show enemies',
                                 'check inventory', 'check statistics', 'talk to npc', 'help', 'exit', 'put on',
                                 'use potion', 'check item', 'delete item', 'check backpack', 'show map',
                                 'show equipment', 'save game', 'load game', 'delete saved game']

    @staticmethod
    def clear_pickles():
        empty = []
        with open('hero.dat', 'wb') as a:
            pickle.dump(empty, a)
        with open('view.dat', 'wb') as b:
            pickle.dump(empty, b)
        with open('pos.dat', 'wb') as c:
            pickle.dump(empty, c)
        with open('world.dat', 'wb') as d:
            pickle.dump(empty, d)
        with open('position.dat', 'wb') as e:
            pickle.dump(empty, e)

    def check_statistics(self):
        print(f'Statistics of Hero {self.hero.name}:\nLevel = {self.hero.level}, attack = {self.hero.attack}, defence '
              f'{self.hero.defence}, health = {self.hero.health}, maximum health = {self.hero.max_health}, '
              f'experience = {self.hero.experience}')

    def check_inventory(self):
        output = []
        for item in self.hero.inventory:
            output.append(item)
        output = ", ".join(output)
        if len(output) == 0:
            output = '-'
        else:
            output += '.'
        print(f'In your inventory you have:\n{output}')

    def show_ways(self):
        current = self.world.place_list[self.current_place]
        print(f'You are currently at place number {self.current_place}.\n You can go to places of numbers '
              f'{[x.id for x in current.connected_to]}')

    def show_enemies(self):
        print(
            f'Enemies in this place are: {[enemy.name for enemy in self.world.place_list[self.current_place].get_enemies()]}')

    def go_to(self, destination):
        current = self.world.place_list[self.current_place]
        if destination in [x.id for x in current.connected_to]:
            if len(current.get_enemies()) > 0 and destination > current.id:
                print('Hola! You need to kill enemy first!')
            else:
                self.current_place = destination
                print(f'You are now in place number {self.current_place}')
                self.world.visited_places.add(destination)
        else:
            print('You can not go directly to this place!')

    def show_npc(self):
        if self.world.place_list[self.current_place].npc is None:
            print('There is no NPC in this place.')
        else:
            print(f'In this place there is an available NPC, his name is:'
                  f' {self.world.place_list[self.current_place].npc.name}')

    def talk_to_npc(self):
        if self.world.place_list[self.current_place].npc is None:
            print('There is no NPC in this place.')
        else:
            self.world.place_list[self.current_place].npc.text()
            if self.world.place_list[self.current_place].npc.quest is not None:
                self.hero.add_quest(self.world.place_list[self.current_place].npc.quest)
                self.world.place_list[self.current_place].npc.set_none()

    def fight(self, enemy):
        if enemy.name != 'gothmog':
            while self.hero.health > 0:
                x = input(
                    'Type 1 for strong strike or type 0 for light strike or anything else to run from battlefield: ')
                if x == "1":
                    val = self.hero.do_attack(True)
                elif x == '0':
                    val = self.hero.do_attack(False)
                else:
                    raise AttributeError
                if val > 0:
                    y = enemy.get_damage(val)
                    print(f'You hit the enemy! His health is decreasing by: {y}.\nCurrent health of your '
                          f'opponent is'
                          f': {enemy.health}')
                else:
                    print('The enemy is dodging your strike! His health is not decreasing.')
                val2 = enemy.do_attack()
                if enemy.health > 0:
                    if val2 > 0:
                        z = self.hero.get_damage(val2)
                        print(
                            f'The enemy strikes! Your health is decreasing by: {z}.\nCurrent health: '
                            f'{self.hero.health}')
                    else:
                        print('You have managed to dodge the enemy strike! Your health is not decreasing')
                else:
                    break
            if self.hero.health > 0:
                print(f'You won! Your health after fight is {self.hero.health}')
                self.world.place_list[self.current_place].kill_enemy(enemy.name)
                self.hero.get_experience()
                self.hero.lvl_up()
                if enemy.name in self.hero.active_quests:
                    self.hero.active_quests[enemy.name].monsters -= 1
                    self.hero.get_reward()

            else:
                print('Unfortunately, u have lost.. Game is over!')
                exit()
        else:
            print("My name is Gothmog, I'm the Lord of Balrogs. This is where your journey ends. I'm going to take you"
                  " straight to hell!")
            while self.hero.health > 0:
                x = input(
                    'Type 1 for strong strike or type 0 for light strike or anything else to run from battlefield: ')
                if x == "1":
                    val = self.hero.do_attack(True)
                elif x == '0':
                    val = self.hero.do_attack(False)
                else:
                    raise AttributeError
                if val > 0:
                    y = enemy.get_damage(val)
                    print(f'You hit the enemy! His health is decreasing by: {y}.\nCurrent health of your '
                          f'opponent is'
                          f': {enemy.health}')
                else:
                    print('The enemy is dodging your strike! His health is not decreasing.')
                val2 = enemy.do_attack()
                if enemy.health > 0:
                    if val > 0:
                        z = self.hero.get_damage(val2)
                        print(
                            f'The enemy strikes! Your health is decreasing by: {z}.\nCurrent health: '
                            f'{self.hero.health}')
                    else:
                        print('You have managed to dodge the enemy strike! Your health is not decreasing')
                else:
                    break
            if self.hero.health > 0:
                print(f'Congratulations! You have killed the Gothmog and finished the game!')
                exit()

            else:
                print('Unfortunately, u have lost.. Game is over!')
                exit()

    def take_items(self):
        if len(self.world.place_list[self.current_place].get_enemies()) == 0:
            if len(self.world.place_list[self.current_place].chest) > 0:
                for item in self.world.place_list[self.current_place].chest:
                    self.hero.get_item(item)
                self.world.place_list[self.current_place].chest = []
                self.hero.quest_item()
                self.hero.get_reward()
                print('Every item from this room is now in your inventory!')
            else:
                print('There are no items in this place')
        else:
            print('U have to kill enemies first!')

    def help(self):
        string = ""
        for command in self.list_of_commands:
            string += str(command) + ", "
        string = string[:-2]
        print("Commands that you can use:\n" + str(string))

    def action(self, command):
        if command == 'check statistics':
            self.check_statistics()
        if command == 'check inventory':
            self.check_inventory()
        if command == 'talk to npc':
            try:
                self.talk_to_npc()
            except AttributeError:
                print('You have already taken this quest.')
        if command == 'show npc':
            self.show_npc()
        if command == 'show ways':
            self.show_ways()
        if command == 'go to':
            x = input('Type a number of place u want to go: ')
            try:
                self.go_to(int(x))
            except ValueError:
                print('This place does not exist!')
        if command == 'take items':
            self.take_items()
        if command == 'show enemies':
            if len(self.world.place_list[self.current_place].get_enemies()) > 0:
                self.show_enemies()
            else:
                print('There are no enemies in this room.')
        if command == 'fight':
            if len(self.world.place_list[self.current_place].get_enemies()) > 0:
                self.show_enemies()
                x = input(
                    'With who you want to fight? Choose number: (for instance: 1 for the first enemy in list, 2 for the'
                    'second ect.) ')
                try:
                    self.fight(self.world.place_list[self.current_place].enemies[abs(int(x) - 1)])
                except ValueError:
                    print('U have to type a number!')
                except IndexError:
                    print('Number is not correct!')
                except AttributeError:
                    print('U have run from battlefield!')
            else:
                print('There are no enemies in this room.')
        if command == 'help':
            self.help()
        if command == 'exit':
            exit()
        if command == 'put on':
            x = input('Type the name of item you want to wear: ')
            try:
                self.hero.put_on(x)
                print('This item is now active and its value has been added to your statistics')
            except ValueError:
                print('You dont have this item in your inventory!')
            except TypeError:
                print('U can not wear quest items!')
        if command == 'use potion':
            x = input('Type the size of potion you want to use (small potion, medium potion, big potion): ')
            try:
                self.hero.use_potion(x)
                print(f'You used the potion! Your current health is: {self.hero.health}')
            except ValueError:
                print('You dont have this type of potion in your backpack!')
            except KeyError:
                print('You need to type small potion, medium potion or big potion!')
        if command == 'check item':
            x = input('Type the name of item you want to check: ')
            try:
                self.hero.check_item(x)
            except ValueError:
                print('You dont have this item in your inventory!')
        if command == 'check backpack':
            print(f'In your backpack you have:\n{self.hero.backpack["small potion"]} small potions,'
                  f' {self.hero.backpack["medium potion"]} medium potions and {self.hero.backpack["big potion"]}'
                  f' big potions.')
        if command == 'show map':
            self.show_map()
        if command == 'show equipment':
            self.hero.show_equipment()
        if command == 'save game':
            self.clear_pickles()
            self.save_game()
            print('Save is now available in game files!')
        if command == 'load game':
            with open('hero.dat', 'rb') as a:
                check = pickle.load(a)
            if check:
                self.load_game()
                print('Game was successfully loaded!')
            else:
                print('You dont have any saves!')
        if command == 'delete saved game':
            with open('hero.dat', 'rb') as a:
                check = pickle.load(a)
            if check:
                self.clear_pickles()
                print('Your last save was successfully deleted!')
            else:
                print('You dont have any game saved')
        if command == 'delete item':
            name = input('Type the name of item you want to delete: ')
            try:
                self.hero.drop_item(name)
                print('Item was successfully deleted!')
            except ValueError:
                print('You dont have this item in your inventory!')

    def play(self):
        question = input("Type 'load' if you want to load game, type anything else if you want to start new game: ")
        if question == 'load':
            with open('hero.dat', 'rb') as a:
                check = pickle.load(a)
            if check:
                self.load_game()
                print('Game was successfully loaded!')
            else:
                print('There is no available save!')
                question = 'none'
        if question != 'load':
            name = input('Type your nickname: ')
            self.generate_new_game(name)
            print("Your character: " + str(name) + " (level 1)\n Let's play!\n (You can type 'help' for instructions)")
        while True:
            command = str(input())
            if command in self.list_of_commands:
                self.action(command)
            else:
                print("Wrong command!\n"
                      "(You can type 'help' for instructions)")

    def show_map(self):
        val_map = {}
        for i in self.world.visited_places:
            val_map[i] = 0
        values = [val_map.get(nodes, 0.5) for nodes in self.view]
        nx.draw_networkx_nodes(self.view, self.pos, cmap=plt.get_cmap('Dark2'), node_size=500, node_color=values)
        nx.draw_networkx_edges(self.view, self.pos, edgelist=self.view.edges(), edge_color='black')
        nx.draw_networkx_labels(self.view, self.pos)
        plt.show()

    def save_game(self):
        with open('hero.dat', 'wb') as a:
            pickle.dump(self.hero, a)
        with open('view.dat', 'wb') as b:
            pickle.dump(self.view, b)
        with open('pos.dat', 'wb') as c:
            pickle.dump(self.pos, c)
        with open('world.dat', 'wb') as d:
            pickle.dump(self.world, d)
        with open('position.dat', 'wb') as e:
            pickle.dump(self.current_place, e)

    def load_game(self):
        with open('hero.dat', 'rb') as a:
            self.hero = pickle.load(a)
        with open('view.dat', 'rb') as b:
            self.view = pickle.load(b)
        with open('pos.dat', 'rb') as c:
            self.pos = pickle.load(c)
        with open('world.dat', 'rb') as d:
            self.world = pickle.load(d)
        with open('position.dat', 'rb') as e:
            self.current_place = pickle.load(e)

    def generate_new_game(self, name):
        world = Graph()
        for i in range(1, 14):
            world.add_place(i)
        world.add_edge(1, 3)
        world.add_edge(1, 2)
        world.add_edge(3, 4)
        world.add_edge(3, 5)
        world.add_edge(2, 7)
        world.add_edge(2, 8)
        world.add_edge(7, 9)
        world.add_edge(5, 6)
        world.add_edge(9, 10)
        world.add_edge(9, 11)
        world.add_edge(8, 12)
        world.add_edge(8, 13)
        big_potion = Item('big potion', 'potion', 400)
        small_potion = Item('small potion', 'potion', 80)
        medium_potion = Item('medium potion', 'potion', 200)
        sword = Item('sword', 'weapon', 10)
        long_sword = Item('long sword', 'weapon', 30)
        beliar_sword = Item('The Claw of Beliar', 'weapon', 150)
        golden_axe = Item('golden axe', 'weapon', 80)
        light_armor = Item('light armor', 'armor', 50)
        farmer = Item('farmers clothing', 'armor', 10)
        dragon = Item('dragons hunter armor', 'armor', 65)
        paladin = Item('Paladins Armor', 'armor', 140)
        quest_it = Item('xardas ring', 'quest', None)
        quest_x = Quest('xardas ring', light_armor)
        quest_d = Quest('wolf', long_sword)
        quest_l = Quest('goblin', golden_axe)
        xardas = NPC('Xardas', quest_x)
        diego = NPC('Diego', quest_d)
        lester = NPC('Lester', quest_l)
        thief = Enemy('thief', 2)
        wolf1 = Enemy('wolf', 5)
        wolf2 = Enemy('wolf', 5)
        wolf3 = Enemy('wolf', 5)
        goblin1 = Enemy('goblin', 8)
        goblin2 = Enemy('goblin', 8)
        goblin3 = Enemy('goblin', 8)
        goblin4 = Enemy('goblin', 8)
        hydra = Enemy('hydra', 20)
        demon = Enemy('demon', 26)
        demon2 = Enemy('demon', 26)
        basilisk = Enemy('basilisk', 29)
        dragon1 = Enemy('dragon', 27)
        cyklop = Enemy('cyklop', 32)
        orc = Enemy('orc', 10)
        bandit = Enemy('bandit', 9)
        gothmog = Enemy('gothmog', 63)
        world.place_list[2].add_npc(diego)
        world.place_list[2].add_enemy(thief)
        world.place_list[2].add_item(sword)
        world.place_list[2].add_item(farmer)
        world.place_list[2].add_item(small_potion)
        world.place_list[3].add_npc(xardas)
        world.place_list[3].add_enemy(wolf1)
        world.place_list[3].add_item(small_potion)
        world.place_list[4].add_npc(lester)
        world.place_list[4].add_enemy(wolf2)
        world.place_list[4].add_item(small_potion)
        world.place_list[5].add_enemy(goblin1)
        world.place_list[5].add_enemy(wolf3)
        world.place_list[5].add_item(medium_potion)
        world.place_list[6].add_enemy(bandit)
        world.place_list[6].add_enemy(orc)
        world.place_list[5].add_item(quest_it)
        world.place_list[6].add_item(small_potion)
        world.place_list[6].add_item(medium_potion)
        world.place_list[7].add_enemy(goblin2)
        world.place_list[7].add_enemy(hydra)
        world.place_list[7].add_item(dragon)
        world.place_list[8].add_enemy(goblin3)
        world.place_list[8].add_enemy(demon)
        world.place_list[9].add_enemy(goblin4)
        world.place_list[9].add_enemy(demon2)
        world.place_list[10].add_enemy(dragon1)
        world.place_list[11].add_enemy(basilisk)
        world.place_list[12].add_enemy(cyklop)
        world.place_list[7].add_item(medium_potion)
        world.place_list[7].add_item(big_potion)
        world.place_list[10].add_item(small_potion)
        world.place_list[10].add_item(medium_potion)
        world.place_list[11].add_item(big_potion)
        world.place_list[11].add_item(beliar_sword)
        world.place_list[12].add_item(paladin)
        world.place_list[13].add_enemy(gothmog)
        self.world = world
        self.current_place = 1
        self.hero = Hero(name, 1)
        self.view = nx.Graph()
        self.view.add_nodes_from(range(1, 13))
        self.view.add_edges_from([(1, 2), (1, 3), (3, 4), (3, 5), (5, 6), (2, 7), (2, 8), (7, 9), (9, 10), (9, 11),
                                  (8, 12), (8, 13)])
        self.pos = nx.spring_layout(self.view)


if __name__ == '__main__':
    new_game = Game()
    new_game.play()
