"""
Calculator agent for solving mathematical problems.

This agent provides tools for performing basic and advanced calculations.
"""

import math
from typing import Dict, Any
from ..core import register_tool
from ...utils.safe_eval import safe_eval


def calc(expression: str) -> str:
    """
    Evaluate a mathematical expression with basic operations.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        str: Result of the calculation
    """
    # Create a safe evaluation environment
    safe_globals: Dict[str, Any] = {
        "abs": abs,
        "round": round,
        "max": max,
        "min": min,
        "sum": sum,
        "pow": pow,
        "int": int,
        "float": float,
    }
    
    try:
        result = safe_eval(expression, safe_globals)
        return str(result)
    except Exception as e:
        return f"Error: Could not evaluate expression. {str(e)}"


def advanced_calc(expression: str) -> str:
    """
    Evaluate a mathematical expression with advanced operations.
    
    Args:
        expression: Mathematical expression to evaluate (can include math functions)
        
    Returns:
        str: Result of the calculation
    """
    # Create a safe evaluation environment with advanced math functions
    safe_globals: Dict[str, Any] = {
        "abs": abs,
        "round": round,
        "max": max,
        "min": min,
        "sum": sum,
        "pow": pow,
        "int": int,
        "float": float,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "factorial": math.factorial,
        "degrees": math.degrees,
        "radians": math.radians,
    }
    
    try:
        result = safe_eval(expression, safe_globals)
        return str(result)
    except Exception as e:
        return f"Error: Could not evaluate expression. {str(e)}"


def quadratic_solver(a: str, b: str, c: str) -> str:
    """
    Solve a quadratic equation of form ax² + bx + c = 0.
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
        
    Returns:
        str: Solutions to the quadratic equation
    """
    try:
        a_float = float(a)
        b_float = float(b)
        c_float = float(c)
        
        # Calculate the discriminant
        discriminant = b_float**2 - 4*a_float*c_float
        
        # Check discriminant to determine number and type of solutions
        if discriminant > 0:
            # Two real solutions
            x1 = (-b_float + math.sqrt(discriminant)) / (2*a_float)
            x2 = (-b_float - math.sqrt(discriminant)) / (2*a_float)
            return f"Two real solutions: x = {x1} or x = {x2}"
        elif discriminant == 0:
            # One real solution (repeated)
            x = -b_float / (2*a_float)
            return f"One real solution (repeated): x = {x}"
        else:
            # Complex solutions
            real_part = -b_float / (2*a_float)
            imag_part = math.sqrt(abs(discriminant)) / (2*a_float)
            return f"Two complex solutions: x = {real_part} + {imag_part}i or x = {real_part} - {imag_part}i"
    except Exception as e:
        return f"Error: Could not solve the quadratic equation. {str(e)}"


def register_calculator_agent():
    """Register all calculator tools with the agent."""
    register_tool(
        "calc",
        "Evaluate a basic mathematical expression (e.g., '2 + 2 * 3')",
        calc
    )
    
    register_tool(
        "advanced_calc",
        "Evaluate an advanced mathematical expression with functions like sqrt, sin, cos (e.g., 'sqrt(16) + sin(pi/2)')",
        advanced_calc
    )
    
    register_tool(
        "solve_quadratic",
        "Solve a quadratic equation ax² + bx + c = 0. Provide the coefficients a, b, and c.",
        quadratic_solver
    )