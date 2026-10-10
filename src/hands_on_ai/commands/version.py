"""
Version command for the hands-on-ai CLI.
"""

from rich import print
from .. import __version__


def version():
    """Display version information."""
    print(f"hands-on-ai v{__version__}")
    print("AI Learning Lab Toolkit")
