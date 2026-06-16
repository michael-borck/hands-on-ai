"""
Tests for the LLM-as-judge evaluator (model call mocked).
"""

import sys

from hands_on_ai.eval import judge

# The `judge` submodule is shadowed by the function of the same name.
judge_mod = sys.modules["hands_on_ai.eval.judge"]


def test_judge_parses_score_and_reasoning(monkeypatch):
    monkeypatch.setattr(judge_mod, "get_response",
                        lambda *a, **k: "SCORE: 4\nREASONING: Clear and correct.")
    v = judge("the answer", "accurate and clear")
    assert v["score"] == 4
    assert "Clear and correct" in v["reasoning"]


def test_judge_clamps_out_of_range_score(monkeypatch):
    monkeypatch.setattr(judge_mod, "get_response",
                        lambda *a, **k: "SCORE: 9\nREASONING: too generous")
    assert judge("x", "y", scale=5)["score"] == 5


def test_judge_handles_unparseable_reply(monkeypatch):
    monkeypatch.setattr(judge_mod, "get_response",
                        lambda *a, **k: "I think it's pretty good overall")
    v = judge("x", "y")
    assert v["score"] is None
    assert v["reasoning"]  # falls back to the raw reply
