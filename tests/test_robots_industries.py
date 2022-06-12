import io
import contextlib
import unittest

from multiprocessing import Event
from robots_industries.factory import (
    ItemInt,
    Inventory,
    Robot
)

from unittest.mock import patch, MagicMock

class ItemIntTest(unittest.TestCase):

    def test_ItemInt(self):
        item = ItemInt(42)
        assert int(item) == int(42)
        assert str(item) == str(42)
        assert repr(item) == repr(42)
        assert item == 42
        assert item > 12
        assert item >= 42
        assert item < 43
        assert item <= 42
        item += 1
        assert item == 43
        item -= 1
        assert item == 42
        new = item % 5
        assert new == 2
        new = item * 2
        assert new == 84
        new = item / 2
        assert new == 21.0
        new = 2 / item
        assert new ==  0.047619047619047616
        assert item.__get__(item, item) == 42
        item.__set__(item, 43)
        assert item == 43

class InventoryTests(unittest.TestCase):

    def test_empty(self):
        inventory = Inventory()
        inv = "{'foo': 0, 'bar': 0, 'foobar': 0, 'pending_robot': 0, 'robots': 0, 'coins': 0}"
        self.assertEqual(str(inventory), inv)

    def test_full(self):
        inventory = Inventory()
        inventory.foo = 1
        inventory.bar = 6
        inventory.foobar = 45
        inventory.pending_robot = 200
        inventory.robots = 42
        inventory.coins = 86
        inv = "{'foo': 1, 'bar': 6, 'foobar': 45, 'pending_robot': 200, 'robots': 42, 'coins': 86}"
        self.assertEqual(str(inventory), inv)

class RobotTests(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        self.inventory.foo = 0
        self.inventory.bar = 0
        self.inventory.foobar = 0
        self.inventory.pending_robot = 0
        self.inventory.robots = 0
        self.inventory.coins = 0
        Robot.start = MagicMock()
        self.robot = Robot(self.inventory, Event(), 0.1)

    def test_mining_foo(self):
        self.inventory.foo = 0

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.robot.worker()
        self.assertIn('mining some foo', f.getvalue())

    def test_mining_bar(self):
        self.inventory.foo = 10

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.robot.worker()
        self.assertIn('mining some bar', f.getvalue())

    @patch('random.randrange')
    def test_assembling_foobar_success(self, mockRandrange):
        mockRandrange.return_value = 99
        self.inventory.foo = 10
        self.inventory.bar = 10

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.robot.worker()
        self.assertIn('successfully assembled a foobar after', f.getvalue())

    @patch('random.randrange')
    def test_assembling_foobar_failed(self, mockRandrange):
        mockRandrange.return_value = 1
        self.inventory.foo = 10
        self.inventory.bar = 10

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.robot.worker()
        self.assertIn('failed assembled a foobar after', f.getvalue())

    def test_selling_foobar(self):
        self.inventory.foobar = 5

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.robot.worker()
        self.assertIn('Successfully sell a foobar for 1 euros', f.getvalue())


    def test_buy_robot(self):
        self.inventory.coins = 4
        self.inventory.foo = 7

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.robot.worker()
        self.assertIn('Successfully buy a new robot for 6 euros', f.getvalue())


