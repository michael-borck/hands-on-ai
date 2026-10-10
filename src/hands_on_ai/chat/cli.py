"""
CLI for the chat module.

Commands are plain functions registered with @app.command() so that arguments
and options parse reliably:  chat ask "hi" --usage
"""

import typer
from .commands import ask, bots, doctor, interactive

app = typer.Typer(help="Simple chatbot with personality")

# Register commands (plain functions from the commands package)
app.command(name="ask", help="Send a single prompt to a bot")(ask.ask)
app.command(name="bots", help="List available bots")(bots.list_bots)
app.command(name="doctor", help="Run diagnostics")(doctor.doctor)
app.command(name="interactive", help="Start interactive REPL")(interactive.interactive)

# Default command - show help
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Chat module - Simple chatbot with personality.

    Use 'chat ask' to send a single prompt or 'chat interactive' for REPL.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Use 'chat --help' for available commands.")


if __name__ == "__main__":
    app()