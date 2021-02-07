import os
import numpy as np
from cv2 import cv2


from solver.lib.colour import Colour
from solver.lib.item import Item
from solver.lib.collection import ContainerCollection

color_map = {
    (181, 57, 45): Colour.RED,
    (216, 103, 123): Colour.PINK,
    (119, 75, 26): Colour.BROWN,
    (127, 149, 48): Colour.GREEN,
    (129, 212, 134): Colour.LIGHT_GREEN,
    (46, 99, 55): Colour.DARK_GREEN,
    (236, 218, 108): Colour.YELLOW,
    (57, 46, 187): Colour.BLUE,
    (103, 161, 224): Colour.LIGHT_BLUE,
    (99, 100, 102): Colour.GREY,
    (104, 47, 142): Colour.PURPLE,
    (219, 143, 81): Colour.ORANGE,
}


def _sort_contours(contours, reverse=False):
    def map_contour(cnt):
        x, y, _, _ = cv2.boundingRect(cnt)
        return x + (100 * y)

    return sorted(contours, key=map_contour, reverse=reverse)


def _rects_overlap(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0] + a[2], b[0] + b[2]) - x
    h = min(a[1] + a[3], b[1] + b[3]) - y
    if w < 0 or h < 0:
        return False
    return True


def load(path):
    img = cv2.imread(path)
    tubes = _find_tubes_in_img(img)
    containers = []
    for tube in tubes:
        container = _process_tube_from_img(img, tube)
        containers.append(container)

    cv2.destroyAllWindows()
    return ContainerCollection(containers)


def _find_tubes_in_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    tubes = _sort_contours(
        [cnt for cnt in contours if cv2.contourArea(cnt) > 60000]
    )
    return tubes


def _process_tube_from_img(img, tube):
    # Extract the tube into an image
    x, y, w, h = cv2.boundingRect(tube)
    tube_img = img[y : y + h, x : x + w]
    # Use the Canny edge detector to find the items in the tube
    canny = cv2.Canny(tube_img, 100, 200)
    # Threshold the canny result to make the items stand out
    tube_thresh = cv2.adaptiveThreshold(
        canny, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    # Find the contours within the single tube
    contours, _ = cv2.findContours(
        tube_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )
    # Filter items by area
    items = [
        cnt
        for cnt in contours
        if cv2.contourArea(cnt) > 8500 and cv2.contourArea(cnt) < 10100
    ]

    # if there are not four items, then look for double sized
    if len(items) < 4:
        large_items = [
            cnt
            for cnt in contours
            if cv2.contourArea(cnt) > 17000 and cv2.contourArea(cnt) < 21000
        ]
        for item in large_items:
            item_rect = cv2.boundingRect(item)
            # Ensure it dosen't overlap any other items
            overlaps = False
            for c in items:
                c_rect = cv2.boundingRect(c)
                if _rects_overlap(item_rect, c_rect):
                    overlaps = True
                    break
            if not overlaps:
                items.append(item)

    # Draw the final contours onto the tube
    if "DEBUG" in os.environ:
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
        c = np.array(cv2.mean(sample)).astype(np.uint8)
        item = Item(color_map.get((c[2], c[1], c[0])))
        container.append(item)
        if h > 100:
            container.append(item)
    return container
