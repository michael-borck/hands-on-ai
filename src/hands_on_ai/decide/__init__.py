"""
Decide module: typed, fast judgments (System-1 style).

Small decisions your code can use directly: pick one option, answer
yes/no with a probability, score against criteria, or extract a typed
record. Local schema-constrained models by default; TypeSafe's Jev
(calibrated System One) as an optional backend.
"""

from .core import classify, decide, extract, score_output

__all__ = ["classify", "decide", "score_output", "extract"]
