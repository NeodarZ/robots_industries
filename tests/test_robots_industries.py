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

    def test_ItemInt_int(self):
        item = ItemInt(42)
        self.assertEqual(int(item), int(42))
        self.assertNotEqual(int(item), str(42))

    def test_ItemInt_convert_str(self):
        item = ItemInt(45)
        self.assertEqual(str(item), str(45))
        self.assertNotEqual(str(item), int(45))

    def test_ItemInt_convert_repr(self):
        item = ItemInt(47)
        self.assertEqual(repr(item), repr(47))
        self.assertNotEqual(repr(item), int(47))

    def test_ItemInt_eq(self):
        item = ItemInt(42)
        self.assertEqual(item, 42)

    def test_ItemInt_gt(self):
        item = ItemInt(42)
        self.assertGreater(item, 12)

    def test_ItemInt_ge(self):
        item = ItemInt(42)
        self.assertGreaterEqual(item, 42)
        self.assertGreaterEqual(item, 41)

    def test_ItemInt_lt(self):
        item = ItemInt(42)
        self.assertLess(item, 43)

    def test_ItemInt_le(self):
        item = ItemInt(42)
        self.assertLessEqual(item, 43)
        self.assertLessEqual(item, 44)

    def test_ItemInt_add(self):
        item = ItemInt(42)
        item += 1
        self.assertEqual(item, 43)

    def test_ItemInt_sub(self):
        item = ItemInt(42)
        item -= 1
        self.assertEqual(item, 41)

    def test_ItemInt_mod(self):
        item = ItemInt(42)
        new = item % 5
        self.assertEqual(new, 2)
        self.assertEqual(item, 42)

    def test_ItemInt_mul(self):
        item = ItemInt(42)
        new = item * 2
        self.assertEqual(new, 84)
        self.assertEqual(item, 42)

    def test_ItemInt_truediv(self):
        item = ItemInt(42)
        new = item / 2
        self.assertEqual(new, 21.0)
        self.assertEqual(item, 42)

    def test_ItemInt_rtruediv(self):
        item = ItemInt(42)
        new = 2 / item
        self.assertEqual(new, 0.047619047619047616)
        self.assertEqual(item, 42)

    def test_ItemInt_rtruediv(self):
        item = ItemInt(42)
        new = 2 / item
        self.assertEqual(new, 0.047619047619047616)
        self.assertEqual(item, 42)

    def test_ItemInt_get(self):
        item = ItemInt(42)
        self.assertEqual(item.__get__(item, item), 42)

    def test_ItemInt_set(self):
        item = ItemInt(42)
        item.__set__(item, 43)
        self.assertEqual(item, 43)

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


