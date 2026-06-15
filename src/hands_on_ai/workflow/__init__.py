"""
Workflow module — orchestrate multi-step tasks as folders of stages (ICM).

A lightweight, human-in-the-loop alternative to heavy agent frameworks: a
workflow is a folder of numbered stages, each a plain-text contract that one
orchestrating model reads in order, writing a reviewable file at every step.
"""

from .runner import Pipeline, init_workspace

__all__ = ["Pipeline", "init_workspace"]
