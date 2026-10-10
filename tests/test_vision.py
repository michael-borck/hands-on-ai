"""
Tests for the vision module (model call mocked).
"""

import base64
import sys

from hands_on_ai.vision import describe

# The `describe` submodule is shadowed by the function of the same name.
describe_mod = sys.modules["hands_on_ai.vision.describe"]


def make_recorder(reply="A cat sits on a mat."):
    """Return (fake_chat_completion, calls) that records each call's args."""
    calls = []

    def fake(messages, **kwargs):
        calls.append({"messages": messages, **kwargs})
        return (reply, None)

    return fake, calls


def test_describe_passes_url_through(monkeypatch):
    fake, calls = make_recorder()
    monkeypatch.setattr(describe_mod, "chat_completion", fake)
    out = describe("https://example.com/cat.png", "What animal is this?")
    assert out == "A cat sits on a mat."
    content = calls[0]["messages"][1]["content"]
    assert content[0] == {"type": "text", "text": "What animal is this?"}
    assert content[1]["image_url"]["url"] == "https://example.com/cat.png"


def test_describe_inlines_local_file_as_data_url(monkeypatch, tmp_path):
    fake, calls = make_recorder()
    monkeypatch.setattr(describe_mod, "chat_completion", fake)
    image = tmp_path / "cat.png"
    image.write_bytes(b"\x89PNG fake bytes")
    describe(str(image))
    url = calls[0]["messages"][1]["content"][1]["image_url"]["url"]
    assert url.startswith("data:image/png;base64,")
    decoded = base64.b64decode(url.split(",", 1)[1])
    assert decoded == b"\x89PNG fake bytes"


def test_describe_uses_default_prompt_and_model(monkeypatch):
    fake, calls = make_recorder()
    monkeypatch.setattr(describe_mod, "chat_completion", fake)
    monkeypatch.setattr(describe_mod, "get_vision_model", lambda: "moondream")
    describe("https://example.com/x.jpg")
    assert calls[0]["model"] == "moondream"
    assert calls[0]["messages"][1]["content"][0]["text"] == "Describe this image."


def test_describe_honours_model_argument(monkeypatch):
    fake, calls = make_recorder()
    monkeypatch.setattr(describe_mod, "chat_completion", fake)
    describe("https://example.com/x.jpg", model="llava")
    assert calls[0]["model"] == "llava"


def test_describe_uses_generous_timeout(monkeypatch):
    fake, calls = make_recorder()
    monkeypatch.setattr(describe_mod, "chat_completion", fake)
    describe("https://example.com/x.jpg")
    assert calls[0]["timeout"] == 120
    describe("https://example.com/x.jpg", timeout=30)
    assert calls[1]["timeout"] == 30


def test_describe_reports_missing_file(monkeypatch):
    fake, calls = make_recorder()
    monkeypatch.setattr(describe_mod, "chat_completion", fake)
    out = describe("no/such/image.png")
    assert out.startswith("❌ Error")
    assert calls == []  # never reached the model
