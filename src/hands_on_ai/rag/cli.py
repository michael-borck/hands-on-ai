"""
CLI for the rag module.
"""

import typer
from .commands import index, ask, interactive

app = typer.Typer(help="RAG - Retrieval-Augmented Generation")

# Add command modules
app.add_typer(index.app, name="index", help="Build a RAG index from files")
app.add_typer(ask.app, name="ask", help="Ask questions using indexed documents")
app.add_typer(interactive.app, name="interactive", help="Run interactive RAG chat")

# Default command - show help
@app.callback(invoke_without_command=True)
def main():
    """
    RAG module - Retrieval-Augmented Generation.
    
    Use 'rag index' to index documents and 'rag ask' to query them.
    """
    import typer
    typer.echo("Use 'rag --help' for available commands.")


if __name__ == "__main__":
    app()