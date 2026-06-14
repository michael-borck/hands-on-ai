"""
Simple tools for the agent module.
"""

import datetime
from typing import Dict, Callable
from .core import register_tool
from ..utils.safe_eval import safe_eval

# Simple built-in tools
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression.
    Uses an AST-based evaluator (not ``eval``) for safe evaluation.
    """
    try:
        result = safe_eval(expression, {
            "abs": abs, "min": min, "max": max, "round": round,
            "sum": sum, "len": len, "int": int, "float": float,
            "str": str, "pow": pow
        })
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def echo(text: str) -> str:
    """Simply returns the input text."""
    return text

def today(_=None) -> str:
    """Returns the current date."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Dictionary of tools for easy access and extension
SIMPLE_TOOLS: Dict[str, Callable] = {
    "calc": calculator,
    "echo": echo,
    "today": today,
}

def register_simple_tools():
    """Register all simple tools with the agent."""
    register_tool("calc", "Evaluate a mathematical expression (e.g., '2 * 3 + 4')", calculator)
    register_tool("echo", "Repeat back the text given to it", echo)
    register_tool("today", "Get today's date in YYYY-MM-DD format", today)

# Ensure the tools are available when this module is imported
register_simple_tools()