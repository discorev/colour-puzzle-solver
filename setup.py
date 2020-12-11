#!/usr/bin/env python

import re
from setuptools import setup, find_packages
import pathlib


def read_version():
    """Read the version number of the cli."""
    content = (
        pathlib.Path(__file__).parent / "solver/__init__.py"
    ).read_text()
    return re.search(r"__version__ = \"([^']+)\"", content).group(1)


def read_requirements(req):
    """Read requirements file into an array of requirements."""
    with (pathlib.Path(__file__).parent / req).open() as f:
        return [line.strip() for line in f if not line.strip().startswith("#")]


setup(
    name="colour-puzzle-solver",
    version=read_version(),
    description="Colour puzzle solver",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Ollie",
    url="https://github.com/discorev/colour-puzzle-solver",
    packages=find_packages(exclude=["tests.*", "tests"]),
    # Support Python 3.7 or greater
    python_requires=">=3.7, <=4.0, !=4.0",
    entry_points={"console_scripts": ["solver=solver.cli.main:cli"]},
    install_requires=read_requirements("requirements/base.txt"),
    extras_require={"dev": read_requirements("requirements/dev.txt")},
    include_package_data=True,
)
