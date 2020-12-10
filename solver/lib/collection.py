"""Collection module."""
from __future__ import annotations
from typing import Union, List, Optional

from lib.move import Move
from lib.container import Container


class ContainerCollection(object):
    """Collection of containers."""

    def __init__(self, data: Union[ContainerCollection, List[Container]]):
        """Construct a new collection from `data`."""
        self.__unique_set: Optional[set] = None
        if isinstance(data, list):
            self.data = tuple(Container(item) for item in data)
        elif isinstance(data, ContainerCollection):
            self.data = tuple(container.copy() for container in data.data)
        else:
            raise TypeError(
                f"Invalid type ({data.__class__.__name__}) "
                "used to construct ContainerCollection."
            )

    @property
    def is_solved(self) -> bool:
        """Check if all containers are solved."""
        return all([container.is_solved for container in self.data])

    # work out all possible next moves:
    def get_moves(self) -> List[Move]:
        """Get a list of possible moves.

        Each move is a possible way to move a colour between two indexes
        in the collection.
        """
        moves: List[Move] = []
        for x in range(len(self)):
            # Skip fully solved containers
            if self.data[x].is_solved or (
                self.data[x].is_unique and len(self.data[x]) > 2
            ):
                continue
            used_in_empty = False
            for y in range(len(self)):
                if x == y:
                    continue
                move = Move(x, y)
                # check if this is a possible move
                if not self.is_valid(move):
                    continue
                if used_in_empty and self.data[move.dest].is_empty:
                    continue
                moves.append(move)
                if self.data[move.dest].is_empty:
                    used_in_empty = True
        return moves

    def is_valid(self, move: Move) -> bool:
        """Check if a move is valid for this collection."""
        # Ensure it's a pratical move
        if (
            move.src == move.dest
            or self.data[move.dest].is_full
            or self.data[move.src].is_empty
        ):
            return False
        src = self.data[move.src]
        dest = self.data[move.dest]

        # Don't allow needless movement between containers
        if src.is_unique and dest.is_empty:
            return False

        # This tests the top most colour matches.
        # If it does, also check there's enough capacity for the pour.
        # Don't try to put more into a container than it could take
        src_count = sum(i == src.head for i in src.data)
        dest_space = dest.capacity - len(dest)
        return (
            self.data[move.dest].test(self.data[move.src].head)
            and src_count <= dest_space
        )

    def after(self, move: Move) -> ContainerCollection:
        """Get a new collection with `move` having been made."""
        if not self.is_valid(move):
            raise ValueError("Invalid move", move)
        _next = ContainerCollection(self)
        _next.data[move.src].pour(_next.data[move.dest])
        return _next

    def __getitem__(self, x):
        """Get item for this index."""
        return self.data[x]

    def __len__(self) -> int:
        """Get the number of containers in the collection."""
        return len(self.data)

    def _unique_set(self):
        if self.__unique_set is None:
            self.__unique_set = set(container.data for container in self.data)
        return self.__unique_set

    def __eq__(self, other: object) -> bool:
        """Check if this collection is the same as `other`.

        Compares the contents of each container but ignores the order.
        """
        if isinstance(other, ContainerCollection):
            return self._unique_set() == other._unique_set()
        if isinstance(other, list):
            return self._unique_set() == set(
                container.data for container in other
            )
        return False

    def __ne__(self, other: object) -> bool:
        """Check if this collection is different to `other`."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Printable representation of this collection."""
        return "\n".join(
            str(i).rjust(2, " ") + ": " + str(self.data[i])
            for i in range(len(self))
        )

    def __repr__(self) -> str:
        """Textual representation of the collection."""
        return f"[{','.join(item.__repr__() for item in self.data)}]"
