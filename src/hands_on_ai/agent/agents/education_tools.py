"""
Educational tools for various subjects.

This agent provides tools for educational purposes, including periodic table
lookups, multiplication tables, and prime number checking.
"""

import math
from ..core import register_tool


# Dictionary of basic element information for the periodic table
ELEMENTS = {
    "hydrogen": {"symbol": "H", "atomic_number": 1, "atomic_weight": 1.008, "category": "Nonmetal", "group": 1, "period": 1},
    "helium": {"symbol": "He", "atomic_number": 2, "atomic_weight": 4.0026, "category": "Noble Gas", "group": 18, "period": 1},
    "lithium": {"symbol": "Li", "atomic_number": 3, "atomic_weight": 6.94, "category": "Alkali Metal", "group": 1, "period": 2},
    "beryllium": {"symbol": "Be", "atomic_number": 4, "atomic_weight": 9.0122, "category": "Alkaline Earth Metal", "group": 2, "period": 2},
    "boron": {"symbol": "B", "atomic_number": 5, "atomic_weight": 10.81, "category": "Metalloid", "group": 13, "period": 2},
    "carbon": {"symbol": "C", "atomic_number": 6, "atomic_weight": 12.011, "category": "Nonmetal", "group": 14, "period": 2},
    "nitrogen": {"symbol": "N", "atomic_number": 7, "atomic_weight": 14.007, "category": "Nonmetal", "group": 15, "period": 2},
    "oxygen": {"symbol": "O", "atomic_number": 8, "atomic_weight": 15.999, "category": "Nonmetal", "group": 16, "period": 2},
    "fluorine": {"symbol": "F", "atomic_number": 9, "atomic_weight": 18.998, "category": "Halogen", "group": 17, "period": 2},
    "neon": {"symbol": "Ne", "atomic_number": 10, "atomic_weight": 20.180, "category": "Noble Gas", "group": 18, "period": 2},
    "sodium": {"symbol": "Na", "atomic_number": 11, "atomic_weight": 22.990, "category": "Alkali Metal", "group": 1, "period": 3},
    "magnesium": {"symbol": "Mg", "atomic_number": 12, "atomic_weight": 24.305, "category": "Alkaline Earth Metal", "group": 2, "period": 3},
    "aluminum": {"symbol": "Al", "atomic_number": 13, "atomic_weight": 26.982, "category": "Post-Transition Metal", "group": 13, "period": 3},
    "silicon": {"symbol": "Si", "atomic_number": 14, "atomic_weight": 28.085, "category": "Metalloid", "group": 14, "period": 3},
    "phosphorus": {"symbol": "P", "atomic_number": 15, "atomic_weight": 30.974, "category": "Nonmetal", "group": 15, "period": 3},
    "sulfur": {"symbol": "S", "atomic_number": 16, "atomic_weight": 32.06, "category": "Nonmetal", "group": 16, "period": 3},
    "chlorine": {"symbol": "Cl", "atomic_number": 17, "atomic_weight": 35.45, "category": "Halogen", "group": 17, "period": 3},
    "argon": {"symbol": "Ar", "atomic_number": 18, "atomic_weight": 39.948, "category": "Noble Gas", "group": 18, "period": 3},
    "potassium": {"symbol": "K", "atomic_number": 19, "atomic_weight": 39.098, "category": "Alkali Metal", "group": 1, "period": 4},
    "calcium": {"symbol": "Ca", "atomic_number": 20, "atomic_weight": 40.078, "category": "Alkaline Earth Metal", "group": 2, "period": 4},
    "iron": {"symbol": "Fe", "atomic_number": 26, "atomic_weight": 55.845, "category": "Transition Metal", "group": 8, "period": 4},
    "copper": {"symbol": "Cu", "atomic_number": 29, "atomic_weight": 63.546, "category": "Transition Metal", "group": 11, "period": 4},
    "zinc": {"symbol": "Zn", "atomic_number": 30, "atomic_weight": 65.38, "category": "Transition Metal", "group": 12, "period": 4},
    "silver": {"symbol": "Ag", "atomic_number": 47, "atomic_weight": 107.87, "category": "Transition Metal", "group": 11, "period": 5},
    "gold": {"symbol": "Au", "atomic_number": 79, "atomic_weight": 196.97, "category": "Transition Metal", "group": 11, "period": 6},
    "mercury": {"symbol": "Hg", "atomic_number": 80, "atomic_weight": 200.59, "category": "Transition Metal", "group": 12, "period": 6},
    "lead": {"symbol": "Pb", "atomic_number": 82, "atomic_weight": 207.2, "category": "Post-Transition Metal", "group": 14, "period": 6},
    "uranium": {"symbol": "U", "atomic_number": 92, "atomic_weight": 238.03, "category": "Actinide", "group": 3, "period": 7},
}


def periodic_table(element: str) -> str:
    """
    Look up information about an element in the periodic table.
    
    Args:
        element: Element name or symbol
        
    Returns:
        str: Information about the element
    """
    # Normalize the input to lowercase
    element = element.lower().strip()
    
    # Check if it's a valid element name
    if element in ELEMENTS:
        info = ELEMENTS[element]
        
        # Format the result
        result = f"Element: {element.capitalize()}\n"
        result += f"Symbol: {info['symbol']}\n"
        result += f"Atomic Number: {info['atomic_number']}\n"
        result += f"Atomic Weight: {info['atomic_weight']}\n"
        result += f"Category: {info['category']}\n"
        result += f"Group: {info['group']}\n"
        result += f"Period: {info['period']}"
        
        return result
    
    # Check if it's a valid element symbol
    for name, info in ELEMENTS.items():
        if str(info["symbol"]).lower() == element:
            
            # Format the result
            result = f"Element: {name.capitalize()}\n"
            result += f"Symbol: {info['symbol']}\n"
            result += f"Atomic Number: {info['atomic_number']}\n"
            result += f"Atomic Weight: {info['atomic_weight']}\n"
            result += f"Category: {info['category']}\n"
            result += f"Group: {info['group']}\n"
            result += f"Period: {info['period']}"
            
            return result
    
    # If no match is found
    return f"Error: Element '{element}' not found in the periodic table. Note: This is a simplified periodic table with only common elements."


def multiplication_table(number: str, size: str = "10") -> str:
    """
    Generate a multiplication table for a given number.
    
    Args:
        number: The base number for the multiplication table
        size: The size of the multiplication table (default: 10)
        
    Returns:
        str: A formatted multiplication table
    """
    try:
        # Parse the inputs
        num = int(number)
        table_size = int(size)
        
        # Validate the size
        if table_size <= 0:
            return "Error: Table size must be a positive integer."
        
        if table_size > 20:
            return "Error: Maximum table size is 20 to keep output readable."
        
        # Generate the table
        table = []
        for i in range(1, table_size + 1):
            result = num * i
            table.append(f"{num} × {i} = {result}")
        
        # Format the output
        header = f"Multiplication Table for {num} (up to {table_size})"
        separator = "=" * len(header)
        
        return f"{header}\n{separator}\n" + "\n".join(table)
        
    except ValueError:
        return "Error: Please provide valid integers for number and size."


def prime_check(number: str) -> str:
    """
    Check if a number is prime and find its factors if it's not.
    
    Args:
        number: The number to check
        
    Returns:
        str: Information about whether the number is prime and its factors
    """
    try:
        # Parse the input
        num = int(number)
        
        # Handle special cases
        if num <= 1:
            return f"{num} is not a prime number. Prime numbers start at 2."
        
        if num == 2:
            return f"{num} is a prime number."
        
        # Check if the number is prime
        is_prime = True
        factors = []
        
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                factors.append(i)
                # Add the corresponding factor
                if i != num // i:  # Avoid duplicates for perfect squares
                    factors.append(num // i)
        
        # Prepare the result
        if is_prime:
            return f"{num} is a prime number."
        else:
            # Sort the factors
            factors.sort()
            
            # Format the factors
            factors_str = ", ".join(map(str, factors))
            
            result = f"{num} is not a prime number.\n"
            result += f"Factors of {num}: 1, {factors_str}, {num}"
            
            # Check if it's a perfect square
            sqrt_num = math.sqrt(num)
            if sqrt_num.is_integer():
                result += f"\n{num} is a perfect square: {int(sqrt_num)}²"
            
            return result
            
    except ValueError:
        return "Error: Please provide a valid integer."


def register_education_tools():
    """Register all educational tools with the agent."""
    register_tool(
        "periodic_table",
        "Look up information about an element in the periodic table",
        periodic_table
    )
    
    register_tool(
        "multiplication_table",
        "Generate a multiplication table for a number (with optional size parameter)",
        multiplication_table
    )
    
    register_tool(
        "prime_check",
        "Check if a number is prime and find its factors if it's not",
        prime_check
    )