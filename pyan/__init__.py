#!/usr/bin/env python3

from importlib.metadata import version, PackageNotFoundError
import sys
import warnings

from .api import create_callgraph

try:
    __version__ = version("pyan3")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

if sys.version_info[:2] == (3, 9):
    # Emit a red warning if running in a terminal that supports ANSI colors.
    RED = "\033[91m"
    RESET = "\033[0m"
    message = (
        "pyan3 support for Python 3.9 is deprecated and will be removed in a future release."
    )
    # Use warnings.warn with highlighted color in terminal, otherwise fallback to normal message
    if sys.stderr.isatty():
        # Print colored warning to stderr, then also raise a FutureWarning for programmatic users.
        print(f"{RED}Warning: {message}{RESET}", file=sys.stderr)
    warnings.warn(message, FutureWarning, stacklevel=2)

from glob import glob
import io
from typing import List, Union

from .analyzer import CallGraphVisitor
from .main import main  # noqa: F401, for export only.
from .visgraph import VisualGraph
from .writers import DotWriter, HTMLWriter, SVGWriter




