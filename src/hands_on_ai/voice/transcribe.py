"""
Transcribe audio files to text with a speech-to-text (STT) model.

The request is a normal OpenAI-compatible API call: upload the audio, get the
words back. Small local models (Whisper and friends, served by tools such as
speaches or whisper.cpp) made this good enough to run on a laptop.
"""

import time
from pathlib import Path

from openai import OpenAI

from ..config import get_api_key, get_stt_model, get_stt_server_url, log


def _build_client(server_url: str, timeout: float) -> OpenAI:
    """Create an OpenAI-compatible client pointed at an audio-capable server."""
    if not server_url.endswith("/v1"):
        server_url = server_url.rstrip("/") + "/v1"
    log.debug(f"Using STT server URL: {server_url}")
    return OpenAI(base_url=server_url, api_key=get_api_key() or "hands-on-ai").with_options(
        timeout=timeout
    )


def transcribe(
    audio_path: str,
    model: str | None = None,
    language: str | None = None,
    retries: int = 2,
    timeout: float = 120,
) -> str:
    """
    Transcribe an audio file to text.

    Args:
        audio_path: Path to the audio file (wav, mp3, m4a, flac, ogg, ...).
        model: STT model to use (defaults to the ``stt_model`` config setting,
            which is ``whisper-1`` unless you override it).
        language: Optional language hint such as ``"en"`` (omit to auto-detect).
        retries: Number of attempts before giving up.
        timeout: Request timeout in seconds.

    Returns:
        str: The transcription, or an error message string in the same
        style as :func:`hands_on_ai.chat.get_response`.
    """
    if model is None:
        model = get_stt_model()

    path = Path(audio_path)
    if not path.is_file():
        return f"❌ Error: audio file not found: {audio_path}"

    last_error = "no attempts made"
    for attempt in range(1, retries + 1):
        try:
            client = _build_client(get_stt_server_url(), timeout)
            if language:
                result = client.audio.transcriptions.create(
                    model=model, file=path, language=language
                )
            else:
                result = client.audio.transcriptions.create(model=model, file=path)
            return (getattr(result, "text", "") or "").strip()
        except Exception as e:
            last_error = str(e)
            log.warning(f"Error during transcription (attempt {attempt}): {e}")
            if attempt < retries:
                time.sleep(1.0)

    return f"❌ Error: {last_error}"
