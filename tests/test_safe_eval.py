"""
Tests for the safe arithmetic evaluator and the calculator tools.

These lock in the fix for the eval() sandbox-escape: emptying __builtins__ is
not a sandbox, so the calculator tools must reject attribute/dunder traversal
and any non-arithmetic construct.
"""

import math

import pytest

from hands_on_ai.utils.safe_eval import safe_eval, UnsafeExpressionError
from hands_on_ai.agent.tools.calculator import calculator
from hands_on_ai.agent.agents.calculator import calc, advanced_calc


def test_basic_arithmetic():
    assert safe_eval("2 + 2 * 10") == 22
    assert safe_eval("(1 + 2) ** 3") == 27
    assert safe_eval("7 // 2 + 7 % 2") == 4
    assert safe_eval("-5 + +3") == -2


def test_whitelisted_names_and_modules():
    assert safe_eval("sqrt(16)", {"sqrt": math.sqrt}) == 4.0
    assert safe_eval("math.sqrt(9)", {"math": math}) == 3.0
    assert safe_eval("pow(2, 8)", {"pow": pow}) == 256


@pytest.mark.parametrize("payload", [
    "().__class__.__bases__[0].__subclasses__()",
    "(1).__class__.__base__.__subclasses__()",
    '__import__("os").system("echo pwned")',
    "math.__loader__",
    "[x for x in range(3)]",
    "lambda: 1",
])
def test_escape_attempts_are_rejected(payload):
    with pytest.raises(UnsafeExpressionError):
        safe_eval(payload, {"math": math})


def test_calculator_tools_block_escapes():
    # The tool wrappers swallow the exception and return an error string;
    # the key invariant is that nothing executes.
    for tool in (calculator, calc, advanced_calc):
        result = tool("().__class__.__bases__[0].__subclasses__()")
        assert "Error" in result

    assert "22" in calculator("2 + 2 * 10")
    assert advanced_calc("sqrt(16)") == "4.0"
