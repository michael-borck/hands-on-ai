"""
Tests for the voice module (audio server calls mocked).
"""

import sys
from pathlib import Path

from hands_on_ai.config import (
    get_stt_model,
    get_stt_server_url,
    get_tts_model,
    get_tts_server_url,
)
from hands_on_ai.voice import speak, transcribe

# The function names shadow their submodules.
transcribe_mod = sys.modules["hands_on_ai.voice.transcribe"]
speak_mod = sys.modules["hands_on_ai.voice.speak"]


class FakeSTTClient:
    """Stands in for the OpenAI client's audio.transcriptions.create."""

    def __init__(self, text="Hello world", fail=False):
        self.calls = []
        self._text = text
        self._fail = fail
        outer = self

        class Transcriptions:
            def create(self, **kwargs):
                outer.calls.append(kwargs)
                if outer._fail:
                    raise ConnectionError("boom")
                return type("Result", (), {"text": outer._text})()

        class Audio:
            transcriptions = Transcriptions()

        self.audio = Audio()

    def with_options(self, timeout=None):
        self.timeout = timeout
        return self


class FakeTTSClient:
    """Stands in for the OpenAI client's audio.speech.create."""

    def __init__(self, audio=b"RIFF....WAVEfmt fake"):
        self.calls = []
        self._audio = audio
        outer = self

        class Speech:
            def create(self, **kwargs):
                outer.calls.append(kwargs)
                return type("Response", (), {"content": outer._audio})()

        class Audio:
            speech = Speech()

        self.audio = Audio()

    def with_options(self, timeout=None):
        self.timeout = timeout
        return self


def test_transcribe_happy_path(monkeypatch, tmp_path):
    fake = FakeSTTClient(text="G'day world")
    monkeypatch.setattr(transcribe_mod, "_build_client", lambda url, timeout: fake)
    monkeypatch.setattr(transcribe_mod, "get_stt_model", lambda: "whisper-1")
    audio = tmp_path / "speech.wav"
    audio.write_bytes(b"fake audio bytes")

    out = transcribe(str(audio))

    assert out == "G'day world"
    assert fake.calls[0]["model"] == "whisper-1"
    assert Path(fake.calls[0]["file"]).read_bytes() == b"fake audio bytes"
    assert "language" not in fake.calls[0]


def test_transcribe_language_hint(monkeypatch, tmp_path):
    fake = FakeSTTClient()
    monkeypatch.setattr(transcribe_mod, "_build_client", lambda url, timeout: fake)
    audio = tmp_path / "speech.wav"
    audio.write_bytes(b"fake")
    transcribe(str(audio), language="en")
    assert fake.calls[0]["language"] == "en"


def test_transcribe_missing_file(monkeypatch):
    fake = FakeSTTClient()
    monkeypatch.setattr(transcribe_mod, "_build_client", lambda url, timeout: fake)
    assert transcribe("no/such/audio.wav").startswith("❌ Error")


def test_transcribe_reports_failure_after_retries(monkeypatch, tmp_path):
    fake = FakeSTTClient(fail=True)
    monkeypatch.setattr(transcribe_mod, "_build_client", lambda url, timeout: fake)
    audio = tmp_path / "speech.wav"
    audio.write_bytes(b"fake")
    out = transcribe(str(audio), retries=1)
    assert out.startswith("❌ Error")
    assert len(fake.calls) == 1


def test_speak_writes_default_file(monkeypatch, tmp_path):
    fake = FakeTTSClient(audio=b"fake wav bytes")
    monkeypatch.setattr(speak_mod, "_build_client", lambda url, timeout: fake)
    monkeypatch.setattr(speak_mod, "get_tts_model", lambda: "kokoro")
    monkeypatch.chdir(tmp_path)

    result = speak("Hello class")

    assert result.name == "speech.wav"
    assert result.read_bytes() == b"fake wav bytes"
    assert fake.calls[0]["input"] == "Hello class"
    assert fake.calls[0]["voice"] == "alloy"
    assert fake.calls[0]["model"] == "kokoro"
    assert fake.calls[0]["response_format"] == "wav"


def test_speak_custom_out_path(monkeypatch, tmp_path):
    fake = FakeTTSClient()
    monkeypatch.setattr(speak_mod, "_build_client", lambda url, timeout: fake)
    out = tmp_path / "greeting.wav"
    result = speak("Hi", out_path=str(out))
    assert result == out
    assert out.exists()


def test_speak_empty_text(monkeypatch):
    fake = FakeTTSClient()
    monkeypatch.setattr(speak_mod, "_build_client", lambda url, timeout: fake)
    assert speak("   ").startswith("⚠️")


def test_speak_reports_failure(monkeypatch, tmp_path):
    class BrokenClient:
        def with_options(self, timeout=None):
            return self

        class Audio:
            class speech:
                @staticmethod
                def create(**kwargs):
                    raise ConnectionError("no tts server")

        audio = Audio()

    monkeypatch.setattr(speak_mod, "_build_client", lambda url, timeout: BrokenClient())
    out = speak("hello", out_path=str(tmp_path / "x.wav"), retries=1)
    assert out.startswith("❌ Error")


def test_stt_tts_config_env_overrides(monkeypatch):
    monkeypatch.setenv("HANDS_ON_AI_STT_SERVER", "http://stt.example")
    monkeypatch.setenv("HANDS_ON_AI_STT_MODEL", "faster-whisper-large")
    monkeypatch.setenv("HANDS_ON_AI_TTS_SERVER", "http://tts.example")
    monkeypatch.setenv("HANDS_ON_AI_TTS_MODEL", "kokoro")
    assert get_stt_server_url() == "http://stt.example"
    assert get_stt_model() == "faster-whisper-large"
    assert get_tts_server_url() == "http://tts.example"
    assert get_tts_model() == "kokoro"


def test_stt_tts_config_defaults_to_main_server(monkeypatch):
    for key in (
        "HANDS_ON_AI_STT_SERVER",
        "HANDS_ON_AI_STT_MODEL",
        "HANDS_ON_AI_TTS_SERVER",
        "HANDS_ON_AI_TTS_MODEL",
    ):
        monkeypatch.delenv(key, raising=False)
    assert get_stt_server_url() == get_stt_server_url()
    assert get_tts_server_url() == get_tts_server_url()
    assert isinstance(get_stt_model(), str) and get_stt_model()
    assert isinstance(get_tts_model(), str) and get_tts_model()
