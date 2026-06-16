"""
Tests for stream_response and Conversation persistence (network mocked).
"""

import sys

import hands_on_ai.chat.conversation as conv_mod
from hands_on_ai.chat import stream_response, Conversation

# The submodule name `get_response` is shadowed by the function of the same name
# in the package namespace, so fetch the module object directly.
gr = sys.modules["hands_on_ai.chat.get_response"]


class _Delta:
    def __init__(self, content):
        self.content = content


class _Choice:
    def __init__(self, content):
        self.delta = _Delta(content)


class _Chunk:
    def __init__(self, content):
        self.choices = [_Choice(content)]


class _Msg:
    def __init__(self, content):
        self.content = content


class _NonStreamChoice:
    def __init__(self, content):
        self.message = _Msg(content)


class _Usage:
    prompt_tokens = 7
    completion_tokens = 3
    total_tokens = 10


class _NonStreamResp:
    choices = [_NonStreamChoice("hi")]
    usage = _Usage()


class _FakeCompletions:
    def create(self, **kwargs):
        if kwargs.get("stream"):
            # Streaming response: an iterable of chunks (last one empty).
            return iter([_Chunk("Hello"), _Chunk(", "), _Chunk("world"), _Chunk(None)])
        return _NonStreamResp()


class _FakeClient:
    class chat:  # noqa: D106
        completions = _FakeCompletions()


def test_stream_response_yields_chunks(monkeypatch):
    monkeypatch.setattr(gr, "_build_client", lambda: _FakeClient())
    monkeypatch.setattr(gr, "_warm_up", lambda model: None)  # skip sleep/print

    chunks = list(stream_response("hi"))
    assert "".join(chunks) == "Hello, world"


def test_stream_response_empty_prompt():
    assert list(stream_response("   ")) == ["⚠️ Empty prompt."]


def test_get_last_usage(monkeypatch):
    from hands_on_ai.chat import get_response, get_last_usage
    monkeypatch.setattr(gr, "_build_client", lambda: _FakeClient())
    monkeypatch.setattr(gr, "_warm_up", lambda model: None)
    monkeypatch.delenv("HANDS_ON_AI_CACHE", raising=False)

    assert get_response("hi") == "hi"
    assert get_last_usage()["total_tokens"] == 10


def test_conversation_save_and_load(tmp_path, monkeypatch):
    monkeypatch.setattr(
        conv_mod, "chat_completion",
        lambda messages, **kw: ("reply", {"total_tokens": 5}),
    )

    chat = Conversation(system="sys")
    chat.ask("hello")

    path = tmp_path / "conv.json"
    chat.save(path)

    loaded = Conversation.load(path)
    assert loaded.system == "sys"
    assert loaded.total_tokens == 5
    assert loaded.history() == chat.history()
    assert loaded.history()[0]["content"] == "hello"
