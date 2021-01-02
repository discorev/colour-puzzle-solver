"""Module for handling the conversion of json input files to collections."""
import json
from typing import Dict, TextIO, List

# from solver.lib.container import Container
from solver.lib.collection import ContainerCollection


def load(file: TextIO, *, reject_invalid: bool = False) -> ContainerCollection:
    """Load a json file into a `ContainerCollection`."""
    content: List[List[str]] = json.load(file)

    if reject_invalid:
        colours: Dict[str, int] = dict()
        for container_list in content:
            for item in container_list:
                if item in colours:
                    colours[item] = colours[item] + 1
                else:
                    colours[item] = 1
        # Check each colour has a count of four
        if not all(count == 4 for count in colours.values()):
            raise ValueError("Invalid colour count")

    return ContainerCollection(content)
