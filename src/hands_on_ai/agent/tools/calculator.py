"""
Calculator tool for mathematical operations.
"""

import math
from ..core import register_tool
from ...utils.safe_eval import safe_eval


def calculator(expression: str):
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        str: Result of evaluation
    """
    # Create a safe evaluation environment
    safe_globals = {
        "abs": abs,
        "round": round,
        "max": max,
        "min": min,
        "sum": sum,
        "len": len,
        "math": math
    }
    
    try:
        result = safe_eval(expression, safe_globals)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: Could not evaluate expression. {str(e)}"


def register_calculator_tool():
    """Register the calculator tool with the agent."""
    register_tool(
        name="calculator",
        description="Evaluate a mathematical expression. Example input: {'expression': '2 + 2 * 10'}",
        function=calculator
    )