"""
The interactive type-to-voice loop, plus best-effort audio playback.

This is the voice-agent loop from the concepts page in three steps --
listen (you, typing for now), think (the chat model), speak (TTS) -- with no
framework in between. Capturing real microphone audio is the extension
exercise; see the "Build the world's smallest Pipecat" project.
"""

import subprocess
import sys

from rich import print

from ..chat import Conversation
from .speak import speak

_SYSTEM = (
    "You are a helpful assistant. Keep your answers short and conversational, "
    "one or two sentences, because they will be read aloud."
)


def play_audio(path) -> None:
    """Play a WAV file with whatever the OS offers (best effort)."""
    players = {"darwin": "afplay", "linux": "aplay", "win32": None}
    player = players.get(sys.platform)
    if not player:
        print(f"[dim]Open {path} in an audio player to hear it.[/dim]")
        return
    try:
        subprocess.run([player, str(path)], check=False)
    except FileNotFoundError:
        print(f"[dim]No '{player}' player found — open {path} manually.[/dim]")


def run_repl() -> None:
    """Type a question, hear the spoken answer. Quit with q, Ctrl-C or Ctrl-D."""
    conversation = Conversation(system=_SYSTEM)
    print("\n🎙️  [bold]voice chat[/bold] — the smallest voice agent\n")
    print("Type what you would say; the reply is spoken via the TTS model.")
    print("Quit with 'q', Ctrl-C, or Ctrl-D.\n")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in {"q", "quit", "exit"}:
            break
        if not text:
            continue

        reply = conversation.ask(text)
        print(f"[bold]Bot:[/bold] {reply}")
        result = speak(reply)
        if isinstance(result, str):  # error message
            print(f"[red]{result}[/red]")
        else:
            print(f"[dim](spoken via {result})[/dim]")
            play_audio(result)
