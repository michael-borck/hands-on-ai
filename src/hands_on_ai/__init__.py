"""
hands_on_ai: Your Hands-on AI Toolkit

A modular toolkit for learning AI concepts through hands-on experimentation.
"""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

try:
    __version__ = _pkg_version("hands-on-ai")
except PackageNotFoundError:  # package not installed (e.g. running from source)
    __version__ = "0.4.0"

# Import core modules
from . import chat
from . import rag
from . import agent

# Make modules available at top level
__all__ = [
    "chat",
    "rag", 
    "agent"
]