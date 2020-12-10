"""Solve the water sort puzzel."""
from typing import Optional
import levels
from lib.collection import ContainerCollection
from lib.search import Option, bfs

start: ContainerCollection = ContainerCollection(levels.stats)
print(start)

result: Optional[Option] = bfs(start)

if result is None:
    print("Cannot be solved :(")
else:
    print("solved in", len(result.moves), "moves")
    print(result.collection)
    print(result.moves)
