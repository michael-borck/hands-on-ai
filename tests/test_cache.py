"""
Tests for the opt-in response cache (network mocked).
"""

import sys

from hands_on_ai.chat import get_response

gr = sys.modules["hands_on_ai.chat.get_response"]


def test_cache_hit_skips_second_call(tmp_path, monkeypatch):
    monkeypatch.setenv("HANDS_ON_AI_CACHE", str(tmp_path))
    calls = []

    def fake_completion(messages, **kw):
        calls.append(1)
        return ("cached answer", {"total_tokens": 3})

    monkeypatch.setattr(gr, "chat_completion", fake_completion)

    r1 = get_response("hello", system="s")
    r2 = get_response("hello", system="s")

    assert r1 == r2 == "cached answer"
    assert len(calls) == 1  # second response came from the cache


def test_cache_disabled_calls_every_time(tmp_path, monkeypatch):
    monkeypatch.delenv("HANDS_ON_AI_CACHE", raising=False)
    calls = []

    def fake_completion(messages, **kw):
        calls.append(1)
        return ("answer", None)

    monkeypatch.setattr(gr, "chat_completion", fake_completion)

    get_response("hi", system="s")
    get_response("hi", system="s")

    assert len(calls) == 2  # no caching, so the model is called each time
