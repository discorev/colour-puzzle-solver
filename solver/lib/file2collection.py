"""Route files to the correct loader for convert to a collection."""
import pathlib

from solver.lib import json2collection, img2collection
from solver.lib.collection import ContainerCollection


def load(path: str, reject_invalid: bool) -> ContainerCollection:
    """Load a file based on it's extension."""
    file = pathlib.Path(path)
    if file.suffix == ".json":
        with file.open() as fh:
            return json2collection.load(fh, reject_invalid=reject_invalid)
    else:
        return img2collection.load(path)
