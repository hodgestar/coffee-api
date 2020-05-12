""" Tests for coffee.api.
"""

import unittest
import json

from coffee.api import app, Kitchen, Brewable, kitchen


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
        kitchen.__init__()
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/')
        assert b"<title>Coffee API v1.0</title>" in rv.data
        assert b"<h2>coffee queue:</h2>" in rv.data
        assert b"<h2>tea queue:</h2>" in rv.data
        assert b"Nothing brewing." in rv.data

    def test_v1_brew(self):
        rv = self.app.post('/api/v1/person/me/brew/coffee')
        assert json.loads(rv.data) == {
            "brew": {
                "beverage": "coffee",
                "person": "me",
                "status": "brewing",
                "subtype": None,
            }
        }

    def test_v1_brew_subtype(self):
        rv = self.app.post(
            '/api/v1/person/me/brew/coffee',
            data=json.dumps({"subtype": "mocha"}),
            content_type="application/json")
        assert json.loads(rv.data) == {
            "brew": {
                "beverage": "coffee",
                "person": "me",
                "status": "brewing",
                "subtype": "mocha",
            }
        }
