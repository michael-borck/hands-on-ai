"""
CLI for the chat module.
"""

import typer
from .commands import ask, bots, doctor, interactive

app = typer.Typer(help="Simple chatbot with personality")

# Add command modules
app.add_typer(ask.app, name="ask", help="Send a single prompt to a bot")
app.add_typer(bots.app, name="bots", help="List available bots")
app.add_typer(doctor.app, name="doctor", help="Run diagnostics")
app.add_typer(interactive.app, name="interactive", help="Start interactive REPL")

# Default command - show help
@app.callback(invoke_without_command=True)
def main():
    """
    Chat module - Simple chatbot with personality.
    
    Use 'chat ask' to send a single prompt or 'chat interactive' for REPL.
    """
    import typer
    typer.echo("Use 'chat --help' for available commands.")


if __name__ == "__main__":
    app()