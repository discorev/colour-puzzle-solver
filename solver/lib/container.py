"""A container is a vessle with a limited capacity that holds items."""
from __future__ import annotations
from typing import Optional, Sequence, Tuple, Union, cast

from solver.lib.item import Item


class Container(object):
    """Represents a capacity limited container in the game."""

    def __init__(
        self,
        initial_content: Union[Sequence[Item], Container, Sequence[str]],
        capacity: int = 4,
    ):
        """Create a container with `intial_content` and `capacity`."""
        self._capacity = capacity
        # Ensure this is only ever set to the maximum size
        self.data: Tuple[Item, ...]
        if isinstance(initial_content, Container):
            if initial_content.capacity == capacity:
                self.data = initial_content.data
            else:
                self.data = initial_content.data[:capacity]
        else:
            type_map = set(map(type, iter(initial_content)))
            if type_map == {Item}:
                initial_content = cast(
                    Sequence[Item], initial_content[:capacity]
                )
                self.data = tuple(initial_content)
            elif type_map == {str}:
                initial_content = cast(
                    Sequence[str], initial_content[:capacity]
                )
                self.data = tuple(
                    Item(value) for value in initial_content[:capacity]
                )
            elif type_map == set():
                self.data = tuple()
            else:
                raise TypeError(
                    f"Unknown initaliser: {initial_content.__class__.__name__}"
                    f": {type_map.__repr__()}"
                )

    @property
    def capacity(self) -> int:
        """Get the capacity of this container."""
        return self._capacity

    @property
    def is_empty(self) -> bool:
        """Check if there are any items in the container.

        Returns true if the container is empty.
        """
        return len(self.data) == 0

    @property
    def is_full(self) -> bool:
        """Check if the container is full.

        Returns true if the container contains it's maximum number of items.
        """
        return len(self.data) >= self.capacity

    @property
    def is_unique(self) -> bool:
        """Check if the container has a unique collection of items.

        Returns true if empty or all contents are the same colour.
        """
        if len(self.data) == 0:
            return True
        return len(set(self.data)) == 1

    @property
    def is_solved(self) -> bool:
        """Check if the container is solved.

        Returns true if empty or full and all contents are the same colour.
        """
        return self.is_empty or (self.is_unique and self.is_full)

    @property
    def head(self) -> Optional[Item]:
        """Get the top most item in the container or None if empty."""
        if self.is_empty:
            return None
        return self.data[-1]

    def test(self, item: Item) -> bool:
        """Check if `item` can be put in this container."""
        if self.is_full or (not self.is_empty and self.data[-1] != item):
            return False
        return True

    def pour(self, target: Container) -> bool:
        """Move the head item from this container to target container.

        If there are multiple concurrent items that are equal, move as many as
        fit within `target` over to it.

        Returns a bool indicating if any items were successfully moved.
        """
        head = self.head
        if head is None:
            return False
        if not target.test(head):
            return False
        # Remove the last item from data and add it to target
        self.data = self.data[:-1]
        target.add(head)
        # Check for matching colours left at head and keep repeating
        # until all have been moved or target is full
        while self.head is not None and self.head == head:
            if target.is_full:
                break
            self.data = self.data[:-1]
            target.add(head)
        return True

    def add(self, next: Item) -> bool:
        """Add `item` to this collection.

        Returns a boolean indiciating success.
        """
        if not self.test(next):
            return False
        # Convert data to a list and then back to a tuple to change it
        data = list(self.data)
        data.append(next)
        self.data = tuple(data)
        return True

    def __str__(self) -> str:
        """Get the string representation of this container."""
        content = [str(content) for content in self.data]
        padding = ""
        if len(content) < self.capacity:
            padding = " " * (self.capacity - len(self))
        return f"[{''.join(content)}{padding}]"

    def __repr__(self) -> str:
        """Get a representation of the container."""
        return f"[{','.join(item.__repr__() for item in self.data)}]"

    def __len__(self) -> int:
        """Return the number of items contained."""
        return len(self.data)

    def copy(self) -> Container:
        """Create a new container with the same data.

        The new container can be mutated using the `add` function
        without affecting the original container.
        """
        return Container(self)

    def __getitem__(self, idx):
        """Get the `item` at `index`."""
        return self.data.__getitem__(idx)

    def __iter__(self):
        """Iterate over this container's items."""
        return self.data.__iter__()

    def __next__(self):
        """Get the next item from this container."""
        return self.data.__next__()
