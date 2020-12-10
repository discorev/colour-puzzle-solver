# Colour Sort Solver

This project is to develop a solver for popular colour sorting puzzle games such as Ball Sort Puzzle ([App Store](https://apps.apple.com/app/ball-sort-puzzle/id1494648714) | [Google Play](https://play.google.com/store/apps/details?id=com.GMA.Ball.Sort.Puzzle)) and Water Sort Puzzle ([App Store](https://apps.apple.com/app/water-sort-puzzle/id1514542157) | [Android](https://play.google.com/store/apps/details?id=com.gma.water.sort.puzzle))


## About the game
The game is based around a collection of containers that are filled with coloured items. Each container has a limited capacity (for the example games above, 4 items).

The goal is to sort the colours such that all items for each unique colour are moved into the same container following a simple set of rules.

There is no time limit.

### Rules
* You can only move the top most colour from one container to another
* You can only move a colour into a container if the top most colour is the same, unless the container is empty
* You can only move a colour into a container that is not already at it's maximum capaicty
* If there are multiple concurrent items of the same colour in the source contianer, all will be transfered to the destination container until it reaches it's maximum capacity.

## How does the solver work
Given a starting pattern the solver performs a [Breadth first search](https://en.wikipedia.org/wiki/Breadth-first_search) over the graph of potential next moves, until the shortest path to a winning move is found.

The starting pattern is evaluated to find all possible moves and this forms the start of the graph. Then recursively, each possible move is evaluated to get the next layer deep in the graph.

Once a valid solution is found, the search is completed.

Currently levels are hard coded into levels.py until a simple representation that allows for easily loading a puzzle configuration is added

**NOTICE:** This project is for educational purposes only and bears no affiliation with the linked games above.
