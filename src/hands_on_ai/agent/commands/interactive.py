"""
Interactive command for the agent CLI - provides a REPL interface.
"""

import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from ..core import run_agent
from ...config import get_model


def interactive(
    model: str = typer.Option(None, help="LLM model to use (default: from config)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
):
    """Run interactive agent chat."""
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
    
    # Get model from config if not specified
    if model is None:
        model = get_model()
    
    print("\n🤖 [bold]Agent Interactive Mode[/bold] - Ask questions using AI tools")
    print("Type 'exit' to quit.\n")
    
    if verbose:
        from .tools import list_available_tools
        list_available_tools()
        console.print()
    
    while True:
        try:
            user_input = input("💬 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting Agent Interactive Mode.")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👋 Goodbye!")
            break
        
        # Run the agent
        try:
            response = run_agent(user_input, model=model)
            console.print(Panel(response, title="Agent", border_style="green"))
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")