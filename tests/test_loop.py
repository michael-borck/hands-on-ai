"""
Tests for the loop runner.

The engine (run_loop / run_ratchet) takes plain callables, so most tests need no
LLM at all. The `judged` helper is tested by monkeypatching the eval judge.
"""

import hands_on_ai.loop.runner as runner_mod
from hands_on_ai.loop import run_loop, run_ratchet, judged


def test_run_loop_stops_when_goal_met():
    # Count up from 0; stop as soon as we reach 3.
    result = run_loop(step=lambda n: (n or 0) + 1, goal=lambda n: n >= 3, start=0)
    assert result["met_goal"] is True
    assert result["result"] == 3
    assert result["iterations"] == 3
    assert result["history"] == [1, 2, 3]


def test_run_loop_respects_max_iters():
    # Goal never satisfied -> stops at max_iters and reports met_goal False.
    result = run_loop(step=lambda n: (n or 0) + 1, goal=lambda n: False, start=0, max_iters=4)
    assert result["met_goal"] is False
    assert result["iterations"] == 4
    assert result["result"] == 4
    assert len(result["history"]) == 4


def test_run_loop_threads_state_through_step():
    result = run_loop(step=lambda s: (s or "") + "x", goal=lambda s: len(s) >= 3, start="")
    assert result["result"] == "xxx"


def test_run_ratchet_only_keeps_improvements():
    # Candidates score 5, 3, 7, 2; only 5 and 7 should be kept (one direction).
    scores = iter([5, 3, 7, 2])
    result = run_ratchet(
        step=lambda best: next(scores),   # candidate *is* its score here
        score=lambda x: x,
        start=None,
        max_iters=4,
    )
    assert result["best"] == 7
    assert result["score"] == 7
    assert [row["kept"] for row in result["log"]] == [True, False, True, False]
    assert [row["iteration"] for row in result["log"]] == [1, 2, 3, 4]


def test_run_ratchet_respects_starting_baseline():
    # Start already scores 10; a candidate of 4 must not replace it.
    result = run_ratchet(
        step=lambda best: 4,
        score=lambda x: x,
        start=10,
        max_iters=2,
    )
    assert result["best"] == 10
    assert all(row["kept"] is False for row in result["log"])


def test_run_ratchet_treats_none_score_as_not_improvement():
    # A None score (e.g. a judge parse failure) is never kept.
    result = run_ratchet(
        step=lambda best: "candidate",
        score=lambda x: None,
        start=None,
        max_iters=3,
    )
    assert result["best"] is None
    assert all(row["kept"] is False for row in result["log"])


def test_judged_builds_goal_from_llm_judge(monkeypatch):
    # Judge returns a rising score; goal(threshold=4) should flip True at 4.
    scores = iter([2, 3, 4])
    monkeypatch.setattr(
        runner_mod, "judge",
        lambda output, criteria, **kw: {"score": next(scores), "reasoning": "", "raw": ""},
    )
    goal = judged("clear and concise", threshold=4)
    assert goal("draft a") is False   # score 2
    assert goal("draft b") is False   # score 3
    assert goal("draft c") is True    # score 4


def test_judged_none_score_is_not_done(monkeypatch):
    monkeypatch.setattr(
        runner_mod, "judge",
        lambda output, criteria, **kw: {"score": None, "reasoning": "", "raw": ""},
    )
    assert judged("anything")("output") is False
