"""
Tests for the decide module (all model calls mocked / scripted).
"""

import sys

from pydantic import BaseModel

from hands_on_ai.decide import classify, decide, extract, score_output

core = sys.modules["hands_on_ai.decide.core"]


class _Fake:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def model_dump(self):
        return dict(self.__dict__)

    def model_dump_json(self):
        return str(self.__dict__)


def _script(monkeypatch, reply):
    monkeypatch.setattr(core, "_structured_call", lambda *a, **k: reply)


def test_classify_local(monkeypatch):
    _script(monkeypatch, _Fake(choice="billing", confidence=0.8,
                               reasoning="Mentions payouts."))
    v = classify("My payouts are failing", ["billing", "technical"])
    assert v["choice"] == "billing"
    assert v["confidence"] == 0.8
    assert v["error"] is None
    assert v["backend"] == "local"


def test_classify_rejects_unknown_option(monkeypatch):
    _script(monkeypatch, _Fake(choice="sales", confidence=0.5, reasoning="x"))
    v = classify("text", ["billing", "technical"])
    assert v["choice"] is None


def test_classify_failure_returns_none_not_raise(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("server down")

    monkeypatch.setattr(core, "_structured_call", boom)
    v = classify("text", ["a", "b"])
    assert v["choice"] is None
    assert "server down" in v["error"]


def test_decide_local(monkeypatch):
    _script(monkeypatch, _Fake(answer=True, probability=0.9, reasoning="Refund asked."))
    v = decide("I want my money back", "Does this request a refund?")
    assert v["answer"] is True
    assert v["probability"] == 0.9


def test_decide_jev(monkeypatch):
    monkeypatch.setattr(core, "_jev_call",
                        lambda state, questions: {"q": {"type": "noul", "noul": 0.95}})
    v = decide("refund please", "Does this request a refund?", backend="jev")
    assert v["answer"] is True
    assert v["probability"] == 0.95
    assert v["backend"] == "jev"


def test_score_output_clamps(monkeypatch):
    _script(monkeypatch, _Fake(score=9, reasoning="too generous"))
    v = score_output("an answer", "accurate and clear", scale=5)
    assert v["score"] == 5


def test_score_output_jev_rounds_levels(monkeypatch):
    # Jev score is 0-based weighted: 2.4 -> level index 2 -> book score 3.
    monkeypatch.setattr(core, "_jev_call",
                        lambda state, questions: {"q": {"type": "score", "score": 2.4}})
    v = score_output("an answer", "clear", scale=5, backend="jev")
    assert v["score"] == 3


def test_extract_local(monkeypatch):
    class Person(BaseModel):
        name: str
        city: str

    _script(monkeypatch, _Fake(name="Sam", city="Perth"))
    v = extract("Sam lives in Perth.", Person)
    assert v["data"] == {"name": "Sam", "city": "Perth"}
    assert v["error"] is None


def test_jev_without_key_returns_error(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    v = classify("text", ["a", "b"], backend="jev")
    assert v["choice"] is None
    assert "TYPESAFE_API_KEY" in v["error"]
