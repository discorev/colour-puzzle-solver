"""Entry point for the CLI."""
import logging
from typing import Optional

import click

from solver.lib import json2collection
from solver.lib.collection import ContainerCollection
from solver.lib.search import Option, bfs, dfs


@click.command()
@click.option(
    "-a",
    "--algorithm",
    type=click.Choice(["BFS", "DFS"], case_sensitive=False),
    default="BFS",
    show_default=True,
)
@click.option("-v", "--verbose", is_flag=True)
@click.option("--validate", is_flag=True)
@click.argument("puzzle", type=click.File())
def cli(
    puzzle=None,
    algorithm="BFS",
    verbose=False,
    validate=False,
    prog_name="solver",  # pylint: disable=W0613
):
    """Solve PUZZLE.

    PUZZLE is the path to a json file describing the puzzle to solve.
    """
    if verbose:
        logging.basicConfig(
            format="%(levelname)s: %(message)s", level=logging.DEBUG
        )

    try:
        start: ContainerCollection = json2collection.load(
            puzzle, reject_invalid=validate
        )
    except ValueError as err:
        raise click.BadArgumentUsage("Invalid PUZZLE: " + str(err))

    print(start, "\n")

    result: Optional[Option] = None
    if algorithm == "BFS":
        print("Searching using Breadth-First Search\n")
        result = bfs(start)
    elif algorithm == "DFS":
        print("Searching using Depth-First Search\n")
        result = dfs(start)

    if result is None:
        print("Cannot be solved :(")
    else:
        print("solved in", len(result.moves), "moves")
        print(result.collection, "\n\n", result.moves, sep="")
