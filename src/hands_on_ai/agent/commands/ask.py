"""
Ask command for the agent CLI - runs an agent with tools.
"""

import typer
from rich.panel import Panel
from rich.console import Console
from ..core import run_agent, list_tools
from ...config import get_model


def ask(
    prompt: str = typer.Argument(..., help="Question or instruction for the agent"),
    model: str = typer.Option(None, help="LLM model to use (default: from config)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Ask a question or give an instruction to the agent."""
    # Register tools from built-in agents
    from ..agents.calculator import register_calculator_agent
    from ..agents.dictionary import register_dictionary_agent
    from ..agents.converter import register_converter_agent
    from ..agents.text_tools import register_text_tools
    from ..agents.datetime_tools import register_datetime_tools
    from ..agents.education_tools import register_education_tools
    
    # Register all agent tools
    register_calculator_agent()
    register_dictionary_agent()
    register_converter_agent()
    register_text_tools()
    register_datetime_tools()
    register_education_tools()
    
    console = Console()
    
    # Show available tools
    if verbose:
        console.print("[bold]Available tools:[/bold]")
        for tool in list_tools():
            console.print(f"- [cyan]{tool['name']}[/cyan]: {tool['description']}")
        console.print()
    
    # Get model from config if not specified
    if model is None:
        model = get_model()
    
    # Run the agent
    console.print(f"🤖 [bold]Running agent with prompt:[/bold] {prompt}")
    
    try:
        response = run_agent(prompt, model=model)
        console.print(Panel(response, title="Agent Response", border_style="green"))
    except Exception as e:
        console.print(f"[red]❌ Error running agent: {e}[/red]")
        raise typer.Exit(1)