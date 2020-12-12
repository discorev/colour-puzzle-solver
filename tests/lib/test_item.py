"""Tests for the item module."""
from unittest import TestCase
from solver.lib.item import Item
from solver.lib.colour import Colour


class TestItem(TestCase):
    """Test cases for the Item class."""

    def test_item_Colour(self):
        """Test Item initalised from the Colour enum."""
        item = Item(Colour.RED)
        self.assertEqual(item.colour, Colour.RED, "Colour should be RED")
        self.assertTrue(
            item.__eq__(Colour.RED), "Colour should equal Colour.RED"
        )
        self.assertTrue(
            item.__eq__("RED"), "Colour should equal the string RED"
        )
        self.assertTrue(
            item.__eq__(Colour.RED.value),
            "Colour should equal Colour.RED.value",
        )
        self.assertTrue(
            item.__ne__(Colour.BLUE), "Colour should not equal Colour.BLUE"
        )
        self.assertTrue(
            item.__ne__("BLUE"), "Colour should not equal the string BLUE"
        )
        self.assertTrue(
            item.__ne__(Colour.BLUE.value),
            "Colour should not equal Colour.BLUE.value",
        )
        self.assertEqual(
            item.__str__(),
            "\x1b[31m\u25A0\x1b[39m",
            "Item string representation should be a coloured square",
        )
        self.assertEqual(
            item.__repr__(),
            "'RED'",
            "Item debug representation should be the name of the colour",
        )
        self.assertEqual(
            item.__hash__(),
            Colour.RED.__hash__(),
            "Item hash should match Colour hash",
        )

    def test_item_string(self):
        """Item initalised with a string."""
        item = Item("RED")
        self.assertEqual(item, Colour.RED, "Colour should be RED")
        self.assertEqual(item.colour, Colour.RED, "Colour should be RED")
        self.assertEqual(item, Colour.RED.value, "Colour should be RED")
        self.assertEqual(
            Item("\x1b[31m"), Colour.RED, "Colour should match value"
        )

    def test_item_equality(self):
        """Items initalised from a string and enum should compare equal."""
        self.assertTrue(
            Item(Colour.RED).__eq__(Item(Colour.RED)),
            "Items of the same colour should match",
        )
        self.assertTrue(
            Item("RED").__eq__(Item(Colour.RED)),
            "Items of the same colour should match",
        )
        self.assertTrue(
            Item(Colour.RED).__eq__(Item("RED")),
            "Items of the same colour should match",
        )
        self.assertTrue(
            Item(Colour.RED).__eq__("\x1b[31m"),
            "Items of the same colour should match",
        )
        self.assertTrue(
            Item(Colour.RED).__ne__(Item(Colour.BLUE)),
            "Items of different colours should not match",
        )
        self.assertTrue(
            Item("RED").__ne__(Colour.BLUE),
            "Items of different colours should not match",
        )
        self.assertTrue(
            Item(Colour.RED).__ne__(Item("BLUE")),
            "Items of different colours should not match",
        )
        self.assertTrue(
            Item(Colour.BLUE).__ne__("\x1b[31m"),
            "Items of the same colour should match",
        )
        self.assertFalse(
            Item(Colour.RED).__eq__(object), "Item does not equal a non-item"
        )
