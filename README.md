# Colour Sort Solver
[![Build Status](https://travis-ci.com/discorev/colour-puzzle-solver.svg?branch=master)](https://travis-ci.com/discorev/colour-puzzle-solver)
[![codecov](https://codecov.io/gh/discorev/colour-puzzle-solver/branch/master/graph/badge.svg?token=IK9OVXNNEC)](https://codecov.io/gh/discorev/colour-puzzle-solver)
[![CodeFactor](https://www.codefactor.io/repository/github/discorev/colour-puzzle-solver/badge)](https://www.codefactor.io/repository/github/discorev/colour-puzzle-solver)

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
Given a starting pattern the solver can perform either a [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search) or a [Depth-first search](https://en.wikipedia.org/wiki/Depth-first_search).

Once a valid solution is found, the search is completed and the final grid and all the moves taken to get there are output.

The starting pattern is provided as a JSON file. Some samples can be found in the levels folder.

### Breadth-First Search
The breadth first algorithm will always find the shortest path to a solution, sacraficing the time to find a solution in favour of ensuring the solution is optimal.

The starting pattern is evaluated to find all possible moves and this forms a queue of next patterns. Then each pattern in the queue is evaluted one-by-one, finding all possible moves that have not already been visited and placing them into the queue. This is repeated until the queue is empty or a solution is found.

### Depth-First Search
The depth first algorithm will find a solution as quickly as possible. The trade-off here is that the solution may not be an optional solution, but it is found far quicker.

All possible moves are evaluted recursively following down the tree as quickly as possible until a solution is found.


**NOTICE:** This project is for educational purposes only and bears no affiliation with the linked games above.
