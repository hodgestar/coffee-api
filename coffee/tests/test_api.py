""" Tests for coffee.api.
"""

import unittest

from coffee.api import app, Kitchen, Brewable


class KitchenTestCase(unittest.TestCase):
    def setUp(self):
        self.kitchen = Kitchen()

    def test_beverages(self):
        self.assertEqual(self.kitchen.beverages, ['coffee', 'tea'])


class BrewableTestCase(unittest.TestCase):
    def test_from_dict(self):
        brew = Brewable.from_dict({
            "beverage": u"coffee",
            "person": u"Batistuta",
        })
        self.assertEqual(brew.beverage, u"coffee")
        self.assertEqual(brew.person, u"Batistuta")
        self.assertEqual(brew.brewing_at, None)
        self.assertEqual(brew.ready_at, None)


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/')
        assert "<title>Coffee API v1.0</title>" in rv.data
        assert "<h2>coffee queue:</h2>" in rv.data
        assert "<h2>tea queue:</h2>" in rv.data
        assert "Nothing brewing." in rv.data
