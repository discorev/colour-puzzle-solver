"""Solve the water sort puzzel."""
from collections import namedtuple
import levels
from lib.collection import ContainerCollection

Option = namedtuple("Option", ["collection", "moves"])

start = ContainerCollection(levels.level_160["start"])
print(start)

options = [Option(start.after(move), (move,)) for move in start.get_moves()]

solved = False
while not solved:
    print("loop", len(options[0].moves), "Options", len(options))
    next_options = []
    next_collections = []
    for option in options:
        if solved:
            break

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
            if _next in next_collections:
                continue
            moves = list(option.moves)
            moves.append(move)
            # Check if a solution was found
            if is_solved:
                next_options = [Option(_next, tuple(moves))]
                solved = True
                break
            next_collections.append(_next)
            next_options.append(Option(_next, tuple(moves)))
    options = next_options

print("solved in", len(options[0][1]), "moves")
print(options[0][0])
print(options[0][1])
