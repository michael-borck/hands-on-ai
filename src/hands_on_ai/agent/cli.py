"""
CLI for the agent module.

Commands are plain functions registered with @app.command() so that arguments
and options parse reliably:  agent ask "calculate 2+2" --verbose
"""

import typer
from .commands import ask, tools, interactive

app = typer.Typer(help="Agent - ReAct-style reasoning with tool use")

# Register commands (plain functions from the commands package)
app.command(name="ask", help="Ask a question using agent tools")(ask.ask)
app.command(name="tools", help="List available agent tools")(tools.list_available_tools)
app.command(name="interactive", help="Run interactive agent chat")(interactive.interactive)

# Default command - show help
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Agent module - ReAct-style reasoning with tool use.

    Use 'agent ask' to run a single prompt or 'agent interactive' for a REPL.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Use 'agent --help' for available commands.")


if __name__ == "__main__":
    app()