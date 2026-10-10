"""
CLI for the rag module.

Commands are plain functions registered with @app.command() so that arguments
and options parse reliably:  rag ask "question" --scores
"""

import typer
from .commands import index, ask, interactive

app = typer.Typer(help="RAG - Retrieval-Augmented Generation")

# Register commands (plain functions from the commands package)
app.command(name="index", help="Build a RAG index from files")(index.index)
app.command(name="ask", help="Ask questions using indexed documents")(ask.ask)
app.command(name="interactive", help="Run interactive RAG chat")(interactive.interactive)

# Default command - show help
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    RAG module - Retrieval-Augmented Generation.

    Use 'rag index' to index documents and 'rag ask' to query them.
    """
    if ctx.invoked_subcommand is None:
        typer.echo("Use 'rag --help' for available commands.")


if __name__ == "__main__":
    app()