"""
Evaluation helpers.

The hard question after "how do I build it?" is "how do I know if the output is
good?". This module uses an LLM to judge the quality of an output against
criteria you define (the "LLM-as-judge" pattern).
"""

from .judge import judge

__all__ = ["judge"]
