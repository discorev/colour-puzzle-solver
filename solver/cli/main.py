"""Entry point for the CLI."""
import click
import json
import logging
from typing import Optional
from solver.lib.collection import ContainerCollection
from solver.lib.search import Option, bfs, dfs

@click.command()
@click.option('-a', '--algorithm',
              type=click.Choice(['BFS', 'DFS'], case_sensitive=False),
              default='BFS', show_default=True)
@click.option("-v", "--verbose", is_flag=True)
@click.argument("puzzle", type=click.File())
def cli(puzzle=None, algorithm='BFS', verbose=False):
    """Solve PUZZLE.

    PUZZLE is the path to a json file describing the puzzle to solve.
    """
    if verbose:
        logging.basicConfig(
            format="%(levelname)s: %(message)s", level=logging.DEBUG
        )

    start: ContainerCollection = ContainerCollection(json.load(puzzle))
    print(start)

    result: Optional[Option] = None
    if algorithm == 'BFS':
        print('Searching using Breadth-First Search')
        result = bfs(start)
    elif algorithm == 'DFS':
        print('Searching using Depth-First Search')
        result = dfs(start)

    if result is None:
        print("Cannot be solved :(")
    else:
        print("solved in", len(result.moves), "moves")
        print(result.collection)
        print(result.moves)
