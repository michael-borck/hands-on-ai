"""
Tools command for the agent CLI - lists available tools.
"""

from rich.table import Table
from rich.console import Console
from ..core import list_tools


def list_available_tools():
    """List all available agent tools."""
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
    
    # Create a table for tools
    table = Table(title="Available Agent Tools")
    table.add_column("Tool", style="cyan")
    table.add_column("Description")
    
    # Add tools to the table
    tools = list_tools()
    if not tools:
        console.print("[yellow]No tools are currently registered.[/yellow]")
        return
    
    for tool in tools:
        table.add_row(tool["name"], tool["description"])
    
    console.print(table)