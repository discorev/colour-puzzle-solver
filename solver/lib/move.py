"""Represent a single move between to containers."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Move:
    """Represents a move between two containers in the game."""

    src: int
    dest: int

    def reverse(self) -> Move:
        """Get the reverse of this move."""
        return Move(self.dest, self.src)

    def __str__(self) -> str:
        """Get a string representation of this move."""
        return f"({self.src}, {self.dest})"
