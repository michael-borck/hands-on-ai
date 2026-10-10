"""
Vision helpers.

A vision-language model (VLM) turns an image into tokens -- the same kind of
input the chat module already sends -- so "seeing" is really just another way
of writing a prompt. This module adds one small function to Hands-On AI:
hand it an image and a question, get a description back. It describes images;
it does not create them.
"""

from .describe import describe

__all__ = ["describe"]
