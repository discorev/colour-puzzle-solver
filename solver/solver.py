"""Solve the water sort puzzel."""
import levels
from lib.collection import ContainerCollection
from lib.search import Option, bfs

start = ContainerCollection(levels.stats["start"])
print(start)

result: Option = bfs(start)

print("solved in", len(result.moves), "moves")
print(result.collection)
print(result.moves)
