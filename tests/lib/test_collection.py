"""Test the collection module."""
import random
from unittest import TestCase
from solver.lib.collection import ContainerCollection
from solver.lib.container import Container
from solver.lib.colour import Colour
from solver.lib.move import Move

colours = list(Colour)


class TestContainerCollection(TestCase):
    """Test cases for the container collection class."""

    def test_construct_with_invalid(self):
        """Constructing with an invalid type should cause a TypeError."""
        with self.assertRaises(TypeError):
            ContainerCollection(None)

        with self.assertRaises(TypeError):
            ContainerCollection(object)

    def test_construct_with_list(self):
        """Construct with a list of collections."""
        coll = ContainerCollection([["RED"], []])
        self.assertEqual(len(coll), 2, "Created with two containers")
        self.assertEqual(
            coll[0], Container(["RED"]), "First container has one red item"
        )
        self.assertEqual(coll[1], Container([]), "Second container is empty")

    def test_is_solved_single_empty(self):
        """An empty collection is always solved."""
        coll = ContainerCollection([[]])
        self.assertTrue(
            coll.is_solved,
            "A single empty container results in a solved collection",
        )

    def test_is_solved_single_full(self):
        """A full collection of the same colour is always solved."""
        colour = random.choice(colours)
        coll = ContainerCollection([[colour.name] * 4])
        self.assertTrue(
            coll.is_solved,
            f"A container full of {colour.name} items always"
            "results in a solved collection",
        )

    def test_is_solved_full_and_empty(self):
        """A full (unique) container and empty container are solved."""
        colour = random.choice(colours)
        coll = ContainerCollection([[colour.name] * 4, []])
        self.assertTrue(
            coll.is_solved,
            f"A solved {colour.name} container and empty container always "
            "result in a solved collection",
        )

    def test_is_solved_multiple_full(self):
        """Multiple solved contianers should cause a solved collection."""
        colour = random.choice(colours)
        coll = ContainerCollection([[colour.name] * 4] * 3)
        self.assertTrue(
            coll.is_solved,
            f"Multiple solved {colour.name} containers always results "
            "in a solved collection",
        )

    def test_is_solved_non_full(self):
        """A collection with a non-full container is not solved."""
        colour = random.choice(colours)
        coll = ContainerCollection([[colour.name] * 3])
        self.assertFalse(
            coll.is_solved,
            f"A single non-full {colour.name} container always results "
            " in a non-solved collection",
        )

    def test_is_solved_full_mixed(self):
        """A single mixed container results in a non-solved collection."""
        coll = ContainerCollection([["RED", "RED", "GREEN", "RED"]])
        self.assertFalse(
            coll.is_solved,
            "A single mixed container results in a non-solved collection",
        )

    def test_is_solved_multiple_non_full(self):
        """A single mixed container results in a non-solved collection."""
        coll = ContainerCollection([["RED", "RED"], ["RED", "RED"]])
        self.assertFalse(
            coll.is_solved,
            "Multiple non-full containers result in a non-solved collection",
        )

    def test_get_moves(self):
        """Test for getting moves from the debug puzzle."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "GREEN", "GREEN"],
                ["RED", "RED", "GREEN", "GREEN"],
                [],
            ]
        )
        moves = coll.get_moves()
        expected = [Move(0, 2), Move(1, 2)]
        self.assertEqual(len(moves), 2, "There are two possible moves")
        self.assertSequenceEqual(moves, expected)

    def test_get_moves_non_possible(self):
        """Tests for getting moves when none are possible."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "GREEN", "GREEN"],
                ["RED", "RED", "GREEN", "GREEN"],
            ]
        )
        moves = coll.get_moves()
        self.assertEqual(len(moves), 0, "No moves should be possible")
        self.assertSequenceEqual(moves, [], "Empty set of moves expected")

    def test_get_moves_only_allow_one_empty(self):
        """Test getting moves with multiple empty containers."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "RED", "GREEN"],
                [],
                [],
            ]
        )
        moves = coll.get_moves()
        self.assertEqual(len(moves), 1, "Only one move should be available")
        self.assertSequenceEqual(
            moves, [Move(0, 1)], "Empty set of moves expected"
        )

    def test_is_valid_from_unique_to_empty(self):
        """Test it's invalid to move from a unique to empty container."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "RED", "RED"],
                [],
            ]
        )
        self.assertFalse(
            coll.is_valid(Move(0, 1)),
            "Moving from a full container to an empty container is not valid",
        )

    def test_after_invalid_move(self):
        """Test that an expcetion is raised trying to use an invalid move."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "RED", "RED"],
                [],
            ]
        )
        with self.assertRaises(ValueError):
            _ = coll.after(Move(0, 1))

    def test_after(self):
        """Ensures the expected collection is returned after a move."""
        expected = ContainerCollection(
            [
                ["RED", "RED", "RED"],
                ["GREEN"],
                [],
            ]
        )
        coll = ContainerCollection(
            [
                ["RED", "RED", "RED", "GREEN"],
                [],
                [],
            ]
        )
        self.assertEqual(coll.after(Move(0, 1)), expected)

    def test_collection_equals_list(self):
        """Test collection equal to a list of containers."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "RED", "GREEN"],
            ]
        )
        self.assertEqual(coll, [Container(["RED", "RED", "RED", "GREEN"])])

    def test_collection_equals_other(self):
        """Test collection equality against other class types."""
        coll = ContainerCollection(
            [
                ["RED", "RED", "RED", "GREEN"],
            ]
        )
        self.assertNotEqual(coll, object())
