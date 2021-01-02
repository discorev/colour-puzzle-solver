"""Tests for the item module."""
import pathlib
from unittest import TestCase
from solver.lib import json2collection
from solver.lib.collection import ContainerCollection


class TestItem(TestCase):
    """Test cases for the Item class."""

    def test_load_valid(self):
        """Test loading from a valid json file."""
        expected = ContainerCollection(
            [
                ["RED", "RED", "GREEN", "GREEN"],
                ["RED", "RED", "GREEN", "GREEN"],
                [],
            ]
        )
        with pathlib.Path("./levels/debug.json").open() as reader:
            collection = json2collection.load(reader)
        self.assertEqual(collection, expected)

    def test_load_invalid_ignore(self):
        """Test loading from a invalid json file and not rejecting it."""
        expected = ContainerCollection(
            [
                ["RED", "RED", "GREEN", "GREEN"],
                ["RED", "RED", "RED", "GREEN"],
                [],
            ]
        )
        with pathlib.Path("./levels/bad.json").open() as reader:
            collection = json2collection.load(reader, reject_invalid=False)
        self.assertEqual(collection, expected)

    def test_load_invalid_(self):
        """Test loading from a invalid json file and rejecting it."""
        with self.assertRaises(ValueError):
            with pathlib.Path("./levels/bad.json").open() as reader:
                _ = json2collection.load(reader, reject_invalid=True)
