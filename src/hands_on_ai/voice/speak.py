"""
Speak text aloud with a text-to-speech (TTS) model.

One call: text in, audio file out. Small local models (Kokoro, Piper) made
this cheap enough to run anywhere; cloud voices are the same API with a
different server and model name.
"""

import time
from pathlib import Path

from openai import OpenAI

from ..config import get_api_key, get_tts_model, get_tts_server_url, log

DEFAULT_VOICE = "alloy"
DEFAULT_OUT_PATH = "speech.wav"


def _build_client(server_url: str, timeout: float) -> OpenAI:
    """Create an OpenAI-compatible client pointed at an audio-capable server."""
    if not server_url.endswith("/v1"):
        server_url = server_url.rstrip("/") + "/v1"
    log.debug(f"Using TTS server URL: {server_url}")
    return OpenAI(base_url=server_url, api_key=get_api_key() or "hands-on-ai").with_options(
        timeout=timeout
    )


def speak(
    text: str,
    voice: str = DEFAULT_VOICE,
    out_path: str | None = None,
    model: str | None = None,
    retries: int = 2,
    timeout: float = 120,
) -> Path | str:
    """
    Turn text into a spoken audio file.

    Args:
        text: What to say.
        voice: Voice name (providers map common names such as ``"alloy"`` to
            their own voices).
        out_path: Where to write the WAV file (defaults to ``speech.wav`` in
            the current directory).
        model: TTS model to use (defaults to the ``tts_model`` config setting,
            which is ``kokoro`` unless you override it).
        retries: Number of attempts before giving up.
        timeout: Request timeout in seconds.

    Returns:
        Path: The written audio file on success, or an error message string
        (starting with ``"❌"``) in the same style as
        :func:`hands_on_ai.chat.get_response`.
    """
    if model is None:
        model = get_tts_model()
    if not text.strip():
        return "⚠️ Empty text."

    path = Path(out_path) if out_path else Path(DEFAULT_OUT_PATH)

    last_error = "no attempts made"
    for attempt in range(1, retries + 1):
        try:
            client = _build_client(get_tts_server_url(), timeout)
            response = client.audio.speech.create(
                model=model, voice=voice, input=text, response_format="wav"
            )
            path.write_bytes(response.content)
            return path
        except Exception as e:
            last_error = str(e)
            log.warning(f"Error during speech (attempt {attempt}): {e}")
            if attempt < retries:
                time.sleep(1.0)

    return f"❌ Error: {last_error}"
