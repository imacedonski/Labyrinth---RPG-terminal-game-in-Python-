import unittest

from hero import Hero
from graph import Graph
from game import Game
from item import Item
from place import Place
from enemy import Enemy
from npc import NPC
from quest import Quest
import pickle


class Test(unittest.TestCase):
    def setUp(self):
        self.hero = Hero('test', 1)
        self.world = Graph()
        self.game = Game()
        self.item = Item('sss', 'weapon', 100)
        self.enemy = Enemy('wolf', 20)
        self.place = Place(33)
        self.quest = Quest('test', self.item)
        self.npc = NPC('test', self.quest)

    def test_init(self):
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.item.value, 100)
        self.assertEqual(self.item.name, 'sss')
        self.assertIn('fight', self.game.list_of_commands)
        self.assertNotIn(None, self.game.list_of_commands)

    def test_generate_new_game(self):
        self.game.generate_new_game('aaa')
        self.assertIsInstance(self.game.hero, Hero)
        self.assertIsInstance(self.game.current_place, int)
        self.assertIsInstance(self.game.world, Graph)

    def test_talk_to_npc(self):
        self.game.generate_new_game('aaa')
        self.game.world.place_list[self.game.current_place].add_npc(self.npc)
        self.game.talk_to_npc()
        self.assertIn(self.quest, self.game.hero.active_quests.values())

    def test_take_items(self):
        self.game.generate_new_game('aaa')
        self.game.world.place_list[self.game.current_place].add_item(self.item)
        self.game.take_items()
        self.assertIn(self.item, self.game.hero.inventory.values())

    def test_go_to(self):
        self.game.generate_new_game('aaa')
        self.game.go_to(2)
        self.assertEqual(self.game.current_place, 2)

    def test_save_game(self):
        self.game.generate_new_game('aaa')
        self.game.save_game()
        with open('hero.dat', 'rb') as x:
            check = pickle.load(x)
        self.assertNotEqual(check, [])

    def test_clear_pickles(self):
        self.game.generate_new_game('aaa')
        self.game.save_game()
        self.game.clear_pickles()
        with open('hero.dat', 'rb') as x:
            check = pickle.load(x)
        self.assertEqual(check, [])

    def test_load_game(self):
        self.game.generate_new_game('aaa')
        self.game.go_to(2)
        self.game.save_game()
        self.game.generate_new_game('bbb')
        self.game.load_game()
        self.assertEqual(self.game.hero.name, 'aaa')
        self.assertEqual(self.game.current_place, 2)

    def test_get_damage(self):
        self.hero.get_damage(10)
        self.assertEqual(self.hero.health, self.hero.max_health - (10 - self.hero.defence))

    def test_increase_health(self):
        self.hero.get_damage(10)
        self.hero.increase_health(1)
        self.assertEqual(self.hero.health, self.hero.max_health - (10 - self.hero.defence) + 1)
        self.hero.get_damage(5)
        self.hero.increase_health(9999)
        self.assertEqual(self.hero.health, self.hero.max_health)

    def test_put_on(self):
        self.hero.get_item(self.item)
        self.hero.put_on(self.item.name)
        self.assertEqual(self.hero.equipment['weapon'], self.item)

    def test_put_off_weapon(self):
        self.hero.get_item(self.item)
        self.hero.put_on(self.item.name)
        self.hero.put_off_weapon()
        self.assertEqual(self.hero.equipment['weapon'], None)

    def test_drop_item(self):
        self.hero.get_item(self.item)
        self.assertIn(self.item.name, self.hero.inventory)
        self.hero.drop_item(self.item.name)
        self.assertNotIn(self.item.name, self.hero.inventory)
        with self.assertRaises(ValueError):
            self.hero.drop_item(self.item.name)

    def test_check_item(self):
        self.hero.get_item(self.item)
        self.assertEqual(self.hero.check_item(self.item.name), None)
        with self.assertRaises(ValueError):
            self.hero.check_item('dddd')




