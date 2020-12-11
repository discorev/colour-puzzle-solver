"""Entry point for the CLI."""
import click
import json
import logging
from typing import Optional
from solver.lib.collection import ContainerCollection
from solver.lib.search import Option, bfs


@click.command()
@click.option("-v", "--verbose", is_flag=True)
@click.argument("puzzle", type=click.File())
def cli(puzzle=None, verbose=False):
    """Solve PUZZLE.

    PUZZLE is the path to a json file describing the puzzle to solve.
    """
    if verbose:
        logging.basicConfig(
            format="%(levelname)s: %(message)s", level=logging.DEBUG
        )

    start: ContainerCollection = ContainerCollection(json.load(puzzle))
    print(start)

    result: Optional[Option] = bfs(start)

    if result is None:
        print("Cannot be solved :(")
    else:
        print("solved in", len(result.moves), "moves")
        print(result.collection)
        print(result.moves)
