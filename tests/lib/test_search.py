"""Tests for the search module."""
from unittest import TestCase
from solver.lib import search
from solver.lib.collection import ContainerCollection
from solver.lib.move import Move


class TestSearch(TestCase):
    """Unit test cases for the search module."""

    def test_bfs_solved(self):
        """Ensure the same collection is returned when already solved."""
        puzzle = ContainerCollection([[]])
        result = search.bfs(puzzle)
        self.assertEqual(result.collection, puzzle)
        self.assertEqual(len(result.moves), 0)

    def test_dfs_solved(self):
        """Ensure the same collection is returned when already solved."""
        puzzle = ContainerCollection([[]])
        result = search.dfs(puzzle)
        self.assertEqual(result.collection, puzzle)
        self.assertEqual(len(result.moves), 0)

    def test_bfs_simple_puzzle(self):
        """Validate breadth-frist search on a simple puzzle."""
        puzzle = ContainerCollection(
            [
                ["BLUE", "ORANGE", "RED", "BLUE"],
                ["ORANGE", "ORANGE", "RED", "BLUE"],
                ["RED", "BLUE", "ORANGE", "RED"],
                [],
                [],
            ]
        )
        solution = (
            Move(0, 3),
            Move(0, 4),
            Move(1, 3),
            Move(1, 4),
            Move(0, 1),
            Move(0, 3),
            Move(2, 4),
            Move(2, 1),
            Move(2, 3),
            Move(2, 4),
        )
        result = search.bfs(puzzle)
        self.assertTrue(result.collection.is_solved, "Solved successfully")
        self.assertEqual(len(result.moves), 10, "Solved in 10 moves")
        self.assertEqual(result.moves, solution)

    def test_dfs_simple_puzzle(self):
        """Validate depth-frist search on a simple puzzle."""
        puzzle = ContainerCollection(
            [
                ["BLUE", "ORANGE", "RED", "BLUE"],
                ["ORANGE", "ORANGE", "RED", "BLUE"],
                ["RED", "BLUE", "ORANGE", "RED"],
                [],
                [],
            ]
        )
        solution = (
            Move(0, 3),
            Move(0, 4),
            Move(1, 3),
            Move(1, 4),
            Move(0, 1),
            Move(0, 3),
            Move(2, 0),
            Move(0, 4),
            Move(2, 0),
            Move(0, 1),
            Move(2, 0),
            Move(0, 3),
            Move(2, 4),
        )
        result = search.dfs(puzzle)
        self.assertTrue(result.collection.is_solved, "Solved successfully")
        self.assertEqual(len(result.moves), 13, "Solved in 13 moves")
        self.assertEqual(result.moves, solution)

    def test_dfs_complex(self):
        """Ensure the same collection is returned when already solved."""
        puzzle = ContainerCollection(
            [
                ["RED", "ORANGE", "LIGHT_GREEN", "LIGHT_BLUE"],
                ["GREY", "ORANGE", "BLUE", "GREY"],
                ["ORANGE", "RED", "LIGHT_BLUE", "ORANGE"],
                ["GREY", "PINK", "GREEN", "BLUE"],
                ["PINK", "RED", "LIGHT_GREEN", "PINK"],
                ["LIGHT_BLUE", "PURPLE", "GREEN", "LIGHT_BLUE"],
                ["LIGHT_GREEN", "GREY", "RED", "GREEN"],
                ["PURPLE", "PINK", "BLUE", "BLUE"],
                ["PURPLE", "LIGHT_GREEN", "PURPLE", "GREEN"],
                [],
                [],
            ]
        )
        expected = ContainerCollection(
            [
                ["RED", "RED", "RED", "RED"],
                ["GREEN", "GREEN", "GREEN", "GREEN"],
                ["BLUE", "BLUE", "BLUE", "BLUE"],
                ["GREY", "GREY", "GREY", "GREY"],
                ["PINK", "PINK", "PINK", "PINK"],
                [],
                ["LIGHT_GREEN", "LIGHT_GREEN", "LIGHT_GREEN", "LIGHT_GREEN"],
                ["PURPLE", "PURPLE", "PURPLE", "PURPLE"],
                [],
                ["LIGHT_BLUE", "LIGHT_BLUE", "LIGHT_BLUE", "LIGHT_BLUE"],
                ["ORANGE", "ORANGE", "ORANGE", "ORANGE"],
            ]
        )
        solution = (
            Move(0, 9),
            Move(0, 10),
            Move(2, 0),
            Move(2, 9),
            Move(5, 9),
            Move(6, 5),
            Move(2, 6),
            Move(2, 0),
            Move(3, 2),
            Move(7, 2),
            Move(4, 7),
            Move(8, 3),
            Move(10, 4),
            Move(0, 10),
            Move(6, 0),
            Move(1, 6),
            Move(1, 2),
            Move(1, 10),
            Move(1, 6),
            Move(3, 1),
            Move(3, 7),
            Move(5, 1),
            Move(5, 8),
            Move(5, 9),
            Move(4, 5),
            Move(4, 0),
            Move(6, 3),
            Move(5, 6),
            Move(7, 4),
            Move(8, 5),
            Move(5, 7),
            Move(8, 5),
            Move(5, 6),
            Move(8, 7),
        )
        result = search.dfs(puzzle)
        self.assertTrue(result.collection.is_solved)
        self.assertEqual(result.collection, expected)
        self.assertEqual(len(result.moves), 34, "Solved in 34 moves")
        self.assertEqual(result.moves, solution)
