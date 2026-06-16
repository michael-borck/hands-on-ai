"""
Ask command for the chat CLI.
"""

import typer
from rich import print
from ..bots import get_bot

app = typer.Typer(help="Send a single prompt to a bot")


@app.callback(invoke_without_command=True)
def ask(
    prompt: str = typer.Argument(..., help="Prompt to send to the chatbot."),
    personality: str = typer.Option("friendly_bot", help="Bot personality to use"),
    usage: bool = typer.Option(False, "--usage", help="Show token usage after the response"),
):
    """Send a single prompt to a bot."""
    bot = get_bot(personality)
    if not bot:
        print(f"[red]❌ Bot '{personality}' not found. Try 'chat bots' for options.[/red]")
        raise typer.Exit(1)
    print(bot(prompt))
    if usage:
        from ..get_response import get_last_usage
        u = get_last_usage()
        if u:
            print(f"[dim]tokens: {u.get('total_tokens')} "
                  f"(prompt {u.get('prompt_tokens')}, completion {u.get('completion_tokens')})[/dim]")
        else:
            print("[dim]token usage not reported by the provider[/dim]")