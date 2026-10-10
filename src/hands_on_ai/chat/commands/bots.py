"""
Bots command for the chat CLI.
"""

from rich import print
from ..bots import list_available_bots, get_bot_description


def list_bots():
    """List available bots."""
    for name, func in list_available_bots().items():
        doc = get_bot_description(func)
        print(f"[bold cyan]{name}[/bold cyan]: {doc}")