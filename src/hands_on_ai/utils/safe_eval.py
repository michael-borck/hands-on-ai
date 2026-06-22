"""
Safe arithmetic expression evaluation for the calculator tools.

Emptying ``__builtins__`` is *not* a sandbox: an expression like
``().__class__.__bases__[0].__subclasses__()`` still reaches ``os`` and can run
arbitrary code, so ``eval`` must never touch attacker- or LLM-controlled input.
This evaluator instead parses the expression to an AST and walks it, permitting
only a fixed whitelist of node types, names, and calls.
"""

import ast
import operator
import types

# Binary and unary operators we allow.
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class UnsafeExpressionError(ValueError):
    """Raised when an expression contains a disallowed construct."""


def safe_eval(expression: str, names: dict | None = None):
    """
    Evaluate a mathematical expression without using ``eval``.

    Only numeric literals, the arithmetic operators above, names provided in
    ``names``, attribute access on whitelisted modules (e.g. ``math.sqrt``), and
    calls to whitelisted callables are permitted. Anything else raises
    :class:`UnsafeExpressionError`.

    Args:
        expression: The expression to evaluate.
        names: Mapping of allowed names (functions, constants, modules).

    Returns:
        The numeric result of the expression.
    """
    names = names or {}

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as e:
        raise UnsafeExpressionError(f"invalid syntax: {e}") from e

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float, complex)):
                return node.value
            raise UnsafeExpressionError(f"constant {node.value!r} is not allowed")

        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
            return _BIN_OPS[type(node.op)](_eval(node.left), _eval(node.right))

        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
            return _UNARY_OPS[type(node.op)](_eval(node.operand))

        if isinstance(node, ast.Name):
            if node.id in names:
                return names[node.id]
            raise UnsafeExpressionError(f"name '{node.id}' is not defined")

        if isinstance(node, ast.Attribute):
            # Block dunder/private traversal (the sandbox-escape vector) and
            # only allow attributes on whitelisted module objects.
            if node.attr.startswith("_"):
                raise UnsafeExpressionError("access to private attributes is not allowed")
            value = _eval(node.value)
            if not isinstance(value, types.ModuleType):
                raise UnsafeExpressionError("attribute access is only allowed on modules")
            return getattr(value, node.attr)

        if isinstance(node, ast.Call):
            if node.keywords:
                raise UnsafeExpressionError("keyword arguments are not allowed")
            func = _eval(node.func)
            args = [_eval(arg) for arg in node.args]
            return func(*args)

        raise UnsafeExpressionError(f"{type(node).__name__} is not allowed")

    return _eval(tree)
