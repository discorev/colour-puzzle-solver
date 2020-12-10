"""Implementation of search algorithms."""
import logging
from typing import List, Optional
from collections import namedtuple
from lib.collection import ContainerCollection

Option = namedtuple("Option", ["collection", "moves"])


def bfs(root: ContainerCollection) -> Optional[Option]:
    """Perform a Breadth-first search to find an optimal solution."""
    # Ensure the search is required
    if root.is_solved:
        return Option(root, tuple())
    queue: List[Option] = [
        Option(root.after(move), (move,)) for move in root.get_moves()
    ]
    while len(queue) > 0:
        logging.debug(f"loop {len(queue[0].moves)} Options {len(queue)}")
        next_queue: List[Option] = []
        discovered: List[ContainerCollection] = []
        for option in queue:
            for move in option.collection.get_moves():
                # If this move is the reverse of the previous move and the move
                # before that was this move, a loop has been found and needs to
                # be broken by simply ignoring this move.
                if (
                    len(option.moves) > 1
                    and option.moves[-1] == move.reverse()
                    and option.moves[-2] == move
                ):
                    continue
                _next: ContainerCollection = option.collection.after(move)
                is_solved = _next.is_solved
                # If this is a leaf node, we cannot continue our search
                if not is_solved and len(_next.get_moves()) == 0:
                    continue
                # Check if this option has been marked as visited
                if _next in discovered:
                    continue
                moves = list(option.moves)
                moves.append(move)
                # Check if a solution was found
                if is_solved:
                    return Option(_next, tuple(moves))
                discovered.append(_next)
                next_queue.append(Option(_next, tuple(moves)))
        queue = next_queue

    # No valid options
    return None
