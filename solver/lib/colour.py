"""Colours for use in the game."""
from enum import Enum
from sty import fg, Style, RgbFg

fg.li_green = Style(RgbFg(153, 255, 153))
fg.li_blue = Style(RgbFg(102, 255, 255))
fg.green = Style(RgbFg(102, 153, 0))
fg.brown = Style(RgbFg(110, 79, 43))
fg.orange = Style(RgbFg(255, 150, 50))
fg.pink = Style(RgbFg(255, 153, 204))


class Colour(Enum):
    """Colours that can be used."""

    RED = fg.red
    PINK = fg.pink
    BROWN = fg.brown
    GREEN = fg.green
    LIGHT_GREEN = fg.li_green
    DARK_GREEN = fg.da_green
    YELLOW = fg.yellow
    BLUE = fg.blue
    LIGHT_BLUE = fg.li_blue
    DARK_BLUE = fg.da_blue
    GREY = fg(245)
    PURPLE = fg(93)
    ORANGE = fg.orange
