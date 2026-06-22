"""
Converter agent for unit conversions.

This agent provides tools for converting between different units of measurement.
"""

from typing import Any, Optional
from ..core import register_tool


# Conversion factors for various units
LENGTH_CONVERSIONS = {
    # Base unit: meters
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.34
}

WEIGHT_CONVERSIONS = {
    # Base unit: grams
    "g": 1.0,
    "kg": 1000.0,
    "mg": 0.001,
    "lb": 453.592,
    "oz": 28.3495,
    "st": 6350.29,  # stone
    "ton": 907185.0,  # US ton
    "tonne": 1000000.0  # Metric ton
}

VOLUME_CONVERSIONS = {
    # Base unit: liters
    "l": 1.0,
    "ml": 0.001,
    "gal": 3.78541,  # US gallon
    "qt": 0.946353,  # US quart
    "pt": 0.473176,  # US pint
    "cup": 0.24,
    "tbsp": 0.0147868,
    "tsp": 0.00492892,
    "fl_oz": 0.0295735  # fluid ounce
}

TEMPERATURE_CONVERSIONS = {
    # Special case, requires formulas
    "c": "celsius",
    "f": "fahrenheit",
    "k": "kelvin"
}

TIME_CONVERSIONS = {
    # Base unit: seconds
    "s": 1.0,
    "min": 60.0,
    "hr": 3600.0,
    "day": 86400.0,
    "week": 604800.0,
    "month": 2592000.0,  # 30-day month
    "year": 31536000.0  # 365-day year
}

# Combined dictionary for easier lookup. Values are heterogeneous: the numeric
# tables map unit -> factor (float), while temperature maps unit -> name (str).
ALL_CONVERSIONS: dict[str, dict[str, Any]] = {
    "length": LENGTH_CONVERSIONS,
    "weight": WEIGHT_CONVERSIONS,
    "volume": VOLUME_CONVERSIONS,
    "temperature": TEMPERATURE_CONVERSIONS,
    "time": TIME_CONVERSIONS
}


def detect_unit_type(unit: str) -> Optional[str]:
    """
    Detect the type of unit (length, weight, etc.).
    
    Args:
        unit: The unit abbreviation
        
    Returns:
        str: The type of unit, or None if not found
    """
    unit = unit.lower()
    
    for unit_type, conversions in ALL_CONVERSIONS.items():
        if unit in conversions:
            return unit_type
            
    return None


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert between temperature units (Celsius, Fahrenheit, Kelvin).
    
    Args:
        value: The temperature value to convert
        from_unit: The source unit (c, f, k)
        to_unit: The target unit (c, f, k)
        
    Returns:
        float: The converted temperature
    """
    # First convert to Celsius as the intermediate unit
    if from_unit == "f":
        celsius = (value - 32) * 5/9
    elif from_unit == "k":
        celsius = value - 273.15
    else:  # already Celsius
        celsius = value
    
    # Then convert from Celsius to the target unit
    if to_unit == "f":
        return (celsius * 9/5) + 32
    elif to_unit == "k":
        return celsius + 273.15
    else:  # to Celsius
        return celsius


def convert_unit(value_str: str, from_unit: str, to_unit: str) -> str:
    """
    Convert a value from one unit to another.
    
    Args:
        value_str: The value to convert as a string
        from_unit: The source unit
        to_unit: The target unit
        
    Returns:
        str: The conversion result or an error message
    """
    try:
        value = float(value_str)
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        # Detect unit types
        from_type = detect_unit_type(from_unit)
        to_type = detect_unit_type(to_unit)
        
        if not from_type:
            return f"Error: Unknown unit '{from_unit}'"
        
        if not to_type:
            return f"Error: Unknown unit '{to_unit}'"
        
        if from_type != to_type:
            return f"Error: Cannot convert between {from_type} and {to_type}"
        
        # Handle temperature conversions specially
        if from_type == "temperature":
            result = convert_temperature(value, from_unit, to_unit)
            return f"{value} {from_unit} = {result:.4g} {to_unit}"
        
        # For other unit types, use the conversion factors
        conversions = ALL_CONVERSIONS[from_type]
        base_value = value * conversions[from_unit]  # Convert to base unit
        result = base_value / conversions[to_unit]  # Convert from base unit to target
        
        return f"{value} {from_unit} = {result:.4g} {to_unit}"
    
    except ValueError:
        return f"Error: Invalid value '{value_str}'. Please provide a numeric value."
    except Exception as e:
        return f"Error: {str(e)}"


def convert_length(value_str: str, from_unit: str, to_unit: str) -> str:
    """
    Convert a length from one unit to another.
    
    Args:
        value_str: The length value to convert as a string
        from_unit: The source unit (m, km, cm, mm, in, ft, yd, mi)
        to_unit: The target unit (m, km, cm, mm, in, ft, yd, mi)
        
    Returns:
        str: The conversion result or an error message
    """
    try:
        value = float(value_str)
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in LENGTH_CONVERSIONS:
            return f"Error: Unknown length unit '{from_unit}'. Available units: m, km, cm, mm, in, ft, yd, mi"
        
        if to_unit not in LENGTH_CONVERSIONS:
            return f"Error: Unknown length unit '{to_unit}'. Available units: m, km, cm, mm, in, ft, yd, mi"
        
        # Convert to meters, then to target unit
        meters = value * LENGTH_CONVERSIONS[from_unit]
        result = meters / LENGTH_CONVERSIONS[to_unit]
        
        return f"{value} {from_unit} = {result:.4g} {to_unit}"
    
    except ValueError:
        return f"Error: Invalid value '{value_str}'. Please provide a numeric value."
    except Exception as e:
        return f"Error: {str(e)}"


def convert_weight(value_str: str, from_unit: str, to_unit: str) -> str:
    """
    Convert a weight from one unit to another.
    
    Args:
        value_str: The weight value to convert as a string
        from_unit: The source unit (g, kg, mg, lb, oz, st, ton, tonne)
        to_unit: The target unit (g, kg, mg, lb, oz, st, ton, tonne)
        
    Returns:
        str: The conversion result or an error message
    """
    try:
        value = float(value_str)
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit not in WEIGHT_CONVERSIONS:
            return f"Error: Unknown weight unit '{from_unit}'. Available units: g, kg, mg, lb, oz, st, ton, tonne"
        
        if to_unit not in WEIGHT_CONVERSIONS:
            return f"Error: Unknown weight unit '{to_unit}'. Available units: g, kg, mg, lb, oz, st, ton, tonne"
        
        # Convert to grams, then to target unit
        grams = value * WEIGHT_CONVERSIONS[from_unit]
        result = grams / WEIGHT_CONVERSIONS[to_unit]
        
        return f"{value} {from_unit} = {result:.4g} {to_unit}"
    
    except ValueError:
        return f"Error: Invalid value '{value_str}'. Please provide a numeric value."
    except Exception as e:
        return f"Error: {str(e)}"


def convert_temperature_tool(value_str: str, from_unit: str, to_unit: str) -> str:
    """
    Convert a temperature from one unit to another.
    
    Args:
        value_str: The temperature value to convert as a string
        from_unit: The source unit (c, f, k - for Celsius, Fahrenheit, Kelvin)
        to_unit: The target unit (c, f, k - for Celsius, Fahrenheit, Kelvin)
        
    Returns:
        str: The conversion result or an error message
    """
    try:
        value = float(value_str)
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        valid_units = ["c", "f", "k"]
        
        if from_unit not in valid_units:
            return f"Error: Unknown temperature unit '{from_unit}'. Available units: c (Celsius), f (Fahrenheit), k (Kelvin)"
        
        if to_unit not in valid_units:
            return f"Error: Unknown temperature unit '{to_unit}'. Available units: c (Celsius), f (Fahrenheit), k (Kelvin)"
        
        result = convert_temperature(value, from_unit, to_unit)
        
        # Format unit names for display
        from_unit_name = {"c": "°C", "f": "°F", "k": "K"}[from_unit]
        to_unit_name = {"c": "°C", "f": "°F", "k": "K"}[to_unit]
        
        return f"{value} {from_unit_name} = {result:.4g} {to_unit_name}"
    
    except ValueError:
        return f"Error: Invalid value '{value_str}'. Please provide a numeric value."
    except Exception as e:
        return f"Error: {str(e)}"


def register_converter_agent():
    """Register all converter tools with the agent."""
    register_tool(
        "convert",
        "Convert a value from one unit to another (e.g., length, weight, volume, temperature, time)",
        convert_unit
    )
    
    register_tool(
        "convert_length",
        "Convert between length units (m, km, cm, mm, in, ft, yd, mi)",
        convert_length
    )
    
    register_tool(
        "convert_weight",
        "Convert between weight units (g, kg, mg, lb, oz, st, ton, tonne)",
        convert_weight
    )
    
    register_tool(
        "convert_temperature",
        "Convert between temperature units (c/Celsius, f/Fahrenheit, k/Kelvin)",
        convert_temperature_tool
    )