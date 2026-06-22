"""
Loop module: repeat a step until a goal is met.

The simplest agentic pattern, made legible: do something, check whether you are
done, repeat. ``run_loop`` stops when a goal is satisfied; ``run_ratchet`` (the
"Ralph Wiggum" technique) only keeps changes that improve a score. ``judged``
turns the ``eval`` LLM judge into a stopping condition.
"""

from .runner import run_loop, run_ratchet, judged

__all__ = ["run_loop", "run_ratchet", "judged"]
