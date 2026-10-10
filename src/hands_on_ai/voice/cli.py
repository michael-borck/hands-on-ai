"""
CLI for the voice module.

Commands are declared with @app.command() (not nested sub-Typers) so that
arguments and options parse reliably:  voice speak "hi" --play
"""

from pathlib import Path
from typing import Optional

import typer
from rich import print

from .repl import play_audio, run_repl
from .speak import speak as speak_text
from .transcribe import transcribe as transcribe_audio

app = typer.Typer(help="Speech-to-text and text-to-speech")


@app.command()
def transcribe(
    audio: str = typer.Argument(..., help="Path to an audio file (wav, mp3, m4a, ...)."),
    language: Optional[str] = typer.Option(None, help="Language hint, e.g. 'en' (optional)."),
    model: Optional[str] = typer.Option(None, help="STT model (defaults to config)."),
):
    """Transcribe an audio file to text."""
    print(transcribe_audio(audio, language=language, model=model))


@app.command()
def speak(
    text: str = typer.Argument(..., help="Text to speak aloud."),
    voice: str = typer.Option("alloy", help="Voice name."),
    out: Optional[Path] = typer.Option(
        None, "--out", "-o", help="Output WAV file (default: speech.wav)."
    ),
    model: Optional[str] = typer.Option(None, help="TTS model (defaults to config)."),
    play: bool = typer.Option(False, "--play", help="Play the audio after generating it."),
):
    """Speak text aloud with a TTS model."""
    result = speak_text(text, voice=voice, out_path=str(out) if out else None, model=model)
    if isinstance(result, str):  # error message
        print(f"[red]{result}[/red]")
        raise typer.Exit(1)
    print(f"🔊 Audio written to [cyan]{result}[/cyan]")
    if play:
        play_audio(result)


@app.command()
def chat():
    """Start the type-to-voice loop (listen -> think -> speak)."""
    run_repl()


if __name__ == "__main__":
    app()
