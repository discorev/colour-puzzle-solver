"""Represent a single move between to containers."""
from __future__ import annotations
from collections import namedtuple


class Move(namedtuple("Move", ["src", "dest"])):
    """Tuple representing a single move in the game."""

    def reverse(self) -> Move:
        """Get the reverse of this move."""
        return Move(self.dest, self.src)

    def __str__(self) -> str:
        """Get a string representation of this move."""
        return f"({self.src}, {self.dest})"
