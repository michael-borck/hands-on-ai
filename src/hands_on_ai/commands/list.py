"""
List command for the hands-on-ai CLI.
"""

from rich import print


def list_modules():
    """List available modules and their CLIs."""
    print("\n🧠 [bold]hands-on-ai[/bold]: AI Learning Lab Toolkit\n\n")
    print("[bold cyan]Available Modules:[/bold cyan]")
    print("  • [bold]chat[/bold] - Simple chatbot with system prompts")
    print("    Usage: [cyan]chat --help[/cyan]")
    print("  • [bold]rag[/bold] - Retrieval-Augmented Generation")
    print("    Usage: [cyan]rag --help[/cyan]")
    print("  • [bold]agent[/bold] - ReAct-style reasoning with tool use")
    print("    Usage: [cyan]agent --help[/cyan]")
    print("  • [bold]vision[/bold] - Describe images with a vision-language model")
    print("    Usage: [cyan]vision --help[/cyan]")
    print("  • [bold]voice[/bold] - Speech-to-text and text-to-speech")
    print("    Usage: [cyan]voice --help[/cyan]")