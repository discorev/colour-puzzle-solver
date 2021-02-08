"""Module for handling the conversion of images to collections."""
import os
import numpy as np
from cv2 import cv2
from typing import List

from solver.lib.colour import Colour
from solver.lib.item import Item
from solver.lib.collection import ContainerCollection


def load(path: str) -> ContainerCollection:
    """Recognise an image file and create a `ContainerCollection`."""
    img = cv2.imread(path)
    if img is None:
        raise ValueError("Invalid file")
    tubes = _find_tubes_in_img(img)
    containers = []
    for tube in tubes:
        container = _process_tube_from_img(img, tube)
        containers.append(container)

    cv2.destroyAllWindows()
    return ContainerCollection(containers)


def _find_tubes_in_img(img: np.array):
    """Find tubes in a loaded image.

    This uses a nieve algorithm based on finding contours that cover a
    large area of the image.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    tubes = _sort_contours(
        [cnt for cnt in contours if cv2.contourArea(cnt) > 60000]
    )
    return tubes


def _sort_contours(contours: List[np.array], reverse=False):
    """Sort a list of contours by the origin of their bounding rects."""

    def map_contour(cnt: np.array) -> int:
        x, y, _, _ = cv2.boundingRect(cnt)
        return x + (100 * y)

    return sorted(contours, key=map_contour, reverse=reverse)


def _process_tube_from_img(img, tube):
    """Convert a tube image into a list of `Item` objects."""
    x, y, w, h = cv2.boundingRect(tube)
    tube_img = img[y : y + h, x : x + w]
    threshold = 50
    # Use the Canny edge detector to find the items in the tube
    canny = cv2.Canny(tube_img, threshold, threshold * 3)
    # Threshold the canny result to make the items stand out
    tube_thresh = cv2.adaptiveThreshold(
        canny, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    # Find the contours within the single tube
    contours, _ = cv2.findContours(
        tube_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    # Filter for items within the right sort of area range and then let
    # the filter below sort out which we really want
    items = [
        cnt
        for cnt in contours
        if cv2.contourArea(cnt) > 8500 and cv2.contourArea(cnt) < 30000
    ]
    # Remove overlapping elements that are larger in area to find the innermost
    # contours within the tube as these are the insides of the coloured blocks
    items = list(
        filter(
            lambda x: all(
                [
                    not (
                        _rects_overlap(
                            cv2.boundingRect(x), cv2.boundingRect(item)
                        )
                        and cv2.contourArea(x) > cv2.contourArea(item)
                    )
                    for item in items
                    if not np.array_equal(x, item)
                ]
            ),
            items,
        )
    )

    # When debugging draw the contours onto the tube
    if "DEBUG" in os.environ:  # pragma: no cover
        tube_contours = tube_img.copy()
        tube_contours = cv2.drawContours(
            tube_contours, items, -1, (0, 255, 0), 3
        )
        cv2.imshow("Tube Contours", tube_contours)
        cv2.waitKey(0)

    container = []
    for item in _sort_contours(items, reverse=True):
        x, y, w, h = cv2.boundingRect(item)
        sample = tube_img[y : y + 5, x : x + 5]
        item = _item_for_sample(sample)
        container.append(item)
        if h > 100:
            container.append(item)
    return container


def _rects_overlap(a: np.array, b: np.array):
    """Check if two rects overlap by finding the intersection."""
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0] + a[2], b[0] + b[2]) - x
    h = min(a[1] + a[3], b[1] + b[3]) - y
    if w < 0 or h < 0:
        return False
    return True


def _item_for_sample(sample: np.array) -> Item:
    """Convert the mean colour of a sample to an `Item`."""
    color_map = [
        (np.array([45, 57, 181, 0], dtype=np.uint8), Colour.RED),
        (np.array([123, 103, 216, 0], dtype=np.uint8), Colour.PINK),
        (np.array([26, 75, 119, 0], dtype=np.uint8), Colour.BROWN),
        (np.array([48, 149, 127, 0], dtype=np.uint8), Colour.GREEN),
        (np.array([134, 212, 129, 0], dtype=np.uint8), Colour.LIGHT_GREEN),
        (np.array([55, 99, 46, 0], dtype=np.uint8), Colour.DARK_GREEN),
        (np.array([108, 218, 236, 0], dtype=np.uint8), Colour.YELLOW),
        (np.array([187, 46, 57, 0], dtype=np.uint8), Colour.BLUE),
        (np.array([224, 161, 103, 0], dtype=np.uint8), Colour.LIGHT_BLUE),
        (np.array([102, 100, 99, 0], dtype=np.uint8), Colour.GREY),
        (np.array([142, 47, 104, 0], dtype=np.uint8), Colour.PURPLE),
        (np.array([81, 143, 219, 0], dtype=np.uint8), Colour.ORANGE),
    ]
    c = np.array(cv2.mean(sample)).astype(np.uint8)
    colour = None
    for key, value in color_map:
        if np.linalg.norm(key - c) < 2:
            colour = value
            break
    if colour is None:
        raise ValueError(f"Unknown Colour (R: {c[2]}, G: {c[1]}, B: {c[0]})")
    return Item(colour)
