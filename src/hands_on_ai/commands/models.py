"""
Commands for working with LLM models in hands-on-ai.
"""

import typer
from rich import print
from rich.table import Table
from ..models import list_models, check_model_exists, get_model_info, get_model_capabilities

app = typer.Typer(help="Manage and inspect LLM models")


@app.callback(invoke_without_command=True)
def models_callback(ctx: typer.Context):
    """Manage and inspect LLM models."""
    # Only run list_models if no subcommand was invoked
    if ctx.invoked_subcommand is None:
        list_available_models()

@app.command()
def list():
    """List all available models."""
    list_available_models()

def list_available_models():
    """List all available models."""
    models = list_models()
    
    if not models:
        print("[yellow]No models found.[/yellow] Make sure Ollama is running.")
        print("Try 'ollama list' to see your available models.")
        return
    
    # Create a table to display model information
    table = Table(title="Available Models")
    table.add_column("Name", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Modified", style="blue")
    
    for model in models:
        # Extract and format information
        name = model.get("name", "Unknown")
        size = _format_size(model.get("size", 0))
        modified = model.get("modified", "Unknown")
        
        table.add_row(name, size, modified)
    
    print(table)
    print("\nUse [bold]hands-on-ai models info <model_name>[/bold] to see detailed information about a specific model.")


@app.command()
def info(model_name: str):
    """Show detailed information about a specific model."""
    if not check_model_exists(model_name):
        print(f"[red]Model '{model_name}' not found.[/red]")
        return
    
    model_info = get_model_info(model_name) or {}
    capabilities = get_model_capabilities(model_name)
    
    print(f"\n[bold cyan]Model:[/bold cyan] {model_name}")
    
    # Extract and format basic information
    if "parameters" in model_info:
        params = model_info["parameters"]
        
        if "num_params" in params:
            print(f"[bold]Parameters:[/bold] {_format_params(params['num_params'])}")
        elif "parameter_count" in params:
            print(f"[bold]Parameters:[/bold] {_format_params(params['parameter_count'])}")
    
    # Display model size if available
    if "size" in model_info:
        print(f"[bold]Size on disk:[/bold] {_format_size(model_info['size'])}")
    
    # Display model family/architecture if available
    if "modelfile" in model_info:
        model_file = model_info["modelfile"]
        from_line = next((line for line in model_file.split("\n") if line.startswith("FROM ")), None)
        if from_line:
            base_model = from_line.replace("FROM ", "").strip()
            print(f"[bold]Base model:[/bold] {base_model}")
    
    # Display capabilities
    print("\n[bold green]Capabilities:[/bold green]")
    for capability, supported in capabilities.items():
        icon = "✓" if supported else "✗"
        color = "green" if supported else "red"
        print(f"[{color}]{icon}[/{color}] {capability.replace('_', ' ').title()}")
    
    # Display best format
    best_format = "react" if capabilities["react_format"] else "json"
    print(f"\n[bold]Recommended format:[/bold] {best_format}")


@app.command()
def check(model_name: str):
    """Check if a model exists."""
    if check_model_exists(model_name):
        print(f"[green]Model '{model_name}' is available.[/green]")
    else:
        print(f"[red]Model '{model_name}' not found.[/red]")
        print("Run 'hands-on-ai models' to see available models.")


def _format_size(size_bytes: int) -> str:
    """Format size in bytes to a human-readable format."""
    size = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0 or unit == "TB":
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def _format_params(params: int) -> str:
    """Format parameter count to a human-readable format."""
    if params >= 1_000_000_000:
        return f"{params / 1_000_000_000:.1f}B"
    elif params >= 1_000_000:
        return f"{params / 1_000_000:.1f}M"
    elif params >= 1_000:
        return f"{params / 1_000:.1f}K"
    return str(params)