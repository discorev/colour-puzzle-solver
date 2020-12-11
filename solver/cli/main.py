"""Entry point for the CLI."""
import click
import json
from typing import Optional
from solver.lib.collection import ContainerCollection
from solver.lib.search import Option, bfs


@click.command()
@click.argument("puzzle", type=click.File())
def cli(puzzle=None):
    """Solve PUZZLE.

    PUZZLE is the path to a json file describing the puzzle to solve.
    """
    start: ContainerCollection = ContainerCollection(json.load(puzzle))
    print(start)

    result: Optional[Option] = bfs(start)

    if result is None:
        print("Cannot be solved :(")
    else:
        print("solved in", len(result.moves), "moves")
        print(result.collection)
        print(result.moves)
