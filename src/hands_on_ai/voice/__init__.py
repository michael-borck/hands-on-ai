"""
Voice helpers: speech-to-text and text-to-speech.

A voice agent is the chat loop wearing headphones: turn speech into text, think
with the same old `get_response`, turn the reply back into speech. This module
provides the two ears-and-mouth pieces -- `transcribe` (audio in, text out)
and `speak` (text in, audio out) -- so the whole loop fits in three lines.
"""

from .speak import speak
from .transcribe import transcribe

__all__ = ["transcribe", "speak"]
