"""
Interactive command for the rag CLI - provides a REPL interface.
"""

import typer
from rich import print
from pathlib import Path
from ...config import CONFIG_DIR
from .ask import ask

app = typer.Typer(help="Run interactive RAG chat")


@app.callback(invoke_without_command=True)
def interactive(
    index_path: str = typer.Option(None, help="Path to index file (default: ~/.hands-on-ai/index.npz)"),
    show_context: bool = typer.Option(False, "--context", "-c", help="Show retrieved context"),
    show_scores: bool = typer.Option(False, "--scores", "-s", help="Show similarity scores"),
    k: int = typer.Option(3, help="Number of chunks to retrieve"),
):
    """Run interactive RAG chat."""
    # Determine the index path
    if index_path is None:
        index_path = str(CONFIG_DIR / "index.npz")

    if not Path(index_path).exists():
        print(f"[red]❌ Index file not found: {index_path}[/red]")
        print("Run 'rag index <directory>' first to create an index.")
        raise typer.Exit(1)
    
    print("\n🔍 [bold]RAG Interactive Mode[/bold] - Ask questions about your documents")
    print(f"Using index: {index_path}")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("💬 Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting RAG Interactive Mode.")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        
        # Use the ask command to handle the query
        ask(user_input, str(index_path), show_context, show_scores, k)