"""Unit tests for the Move data type."""

from unittest import TestCase
from solver.lib.move import Move


class TestMove(TestCase):
    """Test cases for Move."""

    def test_move(self):
        """Ensure that move str() and reverse work."""
        move = Move(1, 2)
        self.assertEqual(move.src, 1, "Move source should be 1")
        self.assertEqual(move.dest, 2, "Move destination should be 2")
        self.assertEqual(
            move.__str__(),
            "(1, 2)",
            "Move string representation should be formatted as a tuple",
        )
        self.assertEqual(
            move.__repr__(),
            "Move(src=1, dest=2)",
            "Move debug represetation should be verbose",
        )

    def test_move_reverse(self):
        """Ensure that move reverse works."""
        move = Move(1, 2)
        reverse_move = Move(2, 1)
        self.assertEqual(
            move.reverse(), reverse_move, "Move reversed should be (2, 1)"
        )
