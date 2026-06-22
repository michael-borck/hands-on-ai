"""
Ask command for the rag CLI - queries indexed documents.
"""

import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from pathlib import Path
from ...config import CONFIG_DIR, get_model
from ...chat import get_response
from ..utils import get_top_k

app = typer.Typer(help="Ask questions using indexed documents")


@app.callback(invoke_without_command=True)
def ask(
    query: str = typer.Argument(..., help="Question to ask"),
    index_path: str = typer.Option(None, help="Path to index file (default: ~/.hands-on-ai/index.npz)"),
    show_context: bool = typer.Option(False, "--context", "-c", help="Show retrieved context"),
    show_scores: bool = typer.Option(False, "--scores", "-s", help="Show similarity scores"),
    k: int = typer.Option(3, help="Number of chunks to retrieve"),
):
    """Ask a question using indexed documents."""
    # Determine the index path
    if index_path is None:
        index_path = str(CONFIG_DIR / "index.npz")

    if not Path(index_path).exists():
        print(f"[red]❌ Index file not found: {index_path}[/red]")
        print("Run 'rag index <directory>' first to create an index.")
        raise typer.Exit(1)
    
    # Get matching chunks
    console = Console()
    console.print(f"🔍 Searching for: [bold cyan]{query}[/bold cyan]")
    
    try:
        if show_scores:
            context, scores = get_top_k(query, index_path, k=k, return_scores=True)
        else:
            context = get_top_k(query, index_path, k=k)
            scores = None
    except Exception as e:
        print(f"[red]❌ Error retrieving context: {e}[/red]")
        raise typer.Exit(1)
    
    # Show retrieved context if requested
    if show_context:
        console.print("\n[bold]Retrieved context:[/bold]")
        for i, (chunk, source) in enumerate(context):
            score_text = f" (Score: {scores[i]:.4f})" if scores else ""
            console.print(f"\n[bold cyan]Source {i+1}: {source}{score_text}[/bold cyan]")
            console.print(Panel(chunk[:500] + "..." if len(chunk) > 500 else chunk))
    
    # Build prompt with context
    prompt = f"Question: {query}\n\nContext:\n"
    for chunk, source in context:
        prompt += f"- {chunk}\n"
    prompt += "\nAnswer the question based on the provided context. If the context doesn't contain the answer, say so."
    
    # Get response
    try:
        model = get_model()
        console.print("\n🤖 [bold]Generating answer...[/bold]")
        response = get_response(
            prompt,
            system="You are a helpful assistant that answers questions based only on the provided context.",
            model=model
        )
        console.print(Panel(response, title="Answer", border_style="green"))
    except Exception as e:
        print(f"[red]❌ Error generating response: {e}[/red]")
        raise typer.Exit(1)