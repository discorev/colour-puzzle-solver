"""Tests for the json2collection module."""
from unittest import TestCase
from solver.lib import img2collection
from solver.lib.collection import ContainerCollection


class TestImg2Collection(TestCase):
    """Test cases for the json2collection class."""

    def test_load_valid(self):
        """Test loading from a valid image file."""
        expected = ContainerCollection(
            [
                ["PINK", "DARK_GREEN", "RED", "LIGHT_BLUE"],
                ["PURPLE", "LIGHT_GREEN", "BROWN", "GREEN"],
                ["RED", "PINK", "BROWN", "GREEN"],
                ["GREY", "GREY", "ORANGE", "RED"],
                ["GREY", "RED", "ORANGE", "DARK_GREEN"],
                ["LIGHT_GREEN", "BLUE", "BLUE", "GREY"],
                ["PURPLE", "ORANGE", "PURPLE", "PINK"],
                ["LIGHT_GREEN", "YELLOW", "DARK_GREEN", "LIGHT_BLUE"],
                ["LIGHT_BLUE", "GREEN", "LIGHT_GREEN", "BROWN"],
                ["LIGHT_BLUE", "YELLOW", "DARK_GREEN", "PURPLE"],
                ["PINK", "BLUE", "GREEN", "ORANGE"],
                ["YELLOW", "BROWN", "YELLOW", "BLUE"],
                [],
                [],
            ]
        )
        collection = img2collection.load("./levels/369.jpeg")
        self.assertEqual(collection, expected)

    def test_load_invalid_(self):
        """Test loading from a invalid file and rejecting it."""
        with self.assertRaises(ValueError):
            _ = img2collection.load("./levels/debug.json")
