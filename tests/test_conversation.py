"""
Tests for Conversation memory and get_response token-usage reporting.

These monkeypatch the low-level chat_completion so no network/LLM is needed.
"""

import sys

import hands_on_ai.chat.conversation as conv_mod
from hands_on_ai.chat import Conversation, get_response

# The submodule name `get_response` is shadowed by the function of the same name
# in the package namespace, so fetch the module object directly.
gr_mod = sys.modules["hands_on_ai.chat.get_response"]


def _fake_completion_factory(records):
    """Return a fake chat_completion that records the messages it was sent."""
    def fake(messages, model=None, personality="friendly", stream=False, retries=2):
        records.append([dict(m) for m in messages])
        last_user = [m for m in messages if m["role"] == "user"][-1]["content"]
        usage = {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10}
        return (f"reply to: {last_user}", usage)
    return fake


def test_conversation_accumulates_history_and_tokens(monkeypatch):
    records = []
    monkeypatch.setattr(conv_mod, "chat_completion", _fake_completion_factory(records))

    chat = Conversation(system="sys")
    assert chat.ask("hello") == "reply to: hello"
    assert chat.ask("again") == "reply to: again"

    # The second call must resend the full prior transcript.
    assert [m["role"] for m in records[1]] == ["system", "user", "assistant", "user"]
    assert records[1][0] == {"role": "system", "content": "sys"}
    assert records[1][1]["content"] == "hello"
    assert records[1][2]["content"] == "reply to: hello"
    assert records[1][3]["content"] == "again"

    assert chat.total_tokens == 20
    assert chat.last_usage["total_tokens"] == 10
    assert len(chat.history()) == 4  # 2 user + 2 assistant, system excluded


def test_conversation_reset(monkeypatch):
    records = []
    monkeypatch.setattr(conv_mod, "chat_completion", _fake_completion_factory(records))

    chat = Conversation(system="sys")
    chat.ask("hi")
    chat.reset()

    assert chat.total_tokens == 0
    assert chat.last_usage is None
    assert chat.history() == []
    assert chat.messages == [{"role": "system", "content": "sys"}]


def test_get_response_return_usage(monkeypatch):
    monkeypatch.setattr(
        gr_mod, "chat_completion",
        lambda messages, **kw: ("hi there", {"total_tokens": 7}),
    )

    # Default: just the string (backward compatible).
    assert get_response("hello") == "hi there"

    # Opt-in: (text, usage) tuple.
    text, usage = get_response("hello", return_usage=True)
    assert text == "hi there"
    assert usage["total_tokens"] == 7


def test_get_response_empty_prompt():
    assert get_response("   ") == "⚠️ Empty prompt."
    text, usage = get_response("", return_usage=True)
    assert text == "⚠️ Empty prompt."
    assert usage is None
