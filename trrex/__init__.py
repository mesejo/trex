# flake8: noqa

import importlib.metadata

from .trrex import make

__all__ = [
    "make"
]

__version__ = importlib.metadata.version(__package__)