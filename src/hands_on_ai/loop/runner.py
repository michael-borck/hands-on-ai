"""
A tiny loop runner: repeat a step until a goal is met.

The whole of "agentic loops" boils down to one shape: do something, check
whether you are done, and repeat. This module gives you two small functions for
that, and nothing more:

- :func:`run_loop` keeps calling a ``step`` until a ``goal`` is satisfied.
- :func:`run_ratchet` (the "Ralph Wiggum" technique) only moves forward: it
  keeps a new result only when it scores higher than the best so far.

Both compose with the rest of the package. A ``step`` is usually a ``chat``
call, and a ``goal`` can be the ``eval`` LLM judge:

    from hands_on_ai.chat import get_response
    from hands_on_ai.loop import run_loop, judged

    result = run_loop(
        step=lambda draft: get_response(f"Improve this paragraph:\\n{draft}"),
        goal=judged("clear, concise, and friendly", threshold=4),
        start="loops are when you do stuff again and again",
        max_iters=5,
    )
    print(result["result"], "in", result["iterations"], "iterations")

Two ideas are worth naming as you read the code:

- **Trigger** - what starts and drives the loop: the ``start`` state plus the
  ``step`` that fires every turn.
- **Goal** - how the loop knows to stop: a ``goal(state) -> bool`` check. It can
  be a plain Python test, or an LLM judge via :func:`judged`.

Loops here are bounded by ``max_iters``, not a wall-clock budget. In a classroom
you want them to stop, stay cheap, and be reproducible. When you outgrow this,
graduate to a real agent framework with time budgets, parallel sub-agents, and
git-as-memory.
"""

from ..eval import judge


def judged(criteria, threshold=4, question=None, model=None, scale=5):
    """
    Build a goal that stops when an LLM judge scores the output high enough.

    This wraps the :mod:`hands_on_ai.eval` LLM-as-judge so you can use a fuzzy,
    natural-language standard ("clear, concise, and friendly") as a loop's
    stopping condition.

    Args:
        criteria: What "good" means (passed straight to the judge).
        threshold: Minimum score (1..``scale``) that counts as done (default 4).
        question: Optional original question for the judge's context.
        model: LLM model to use (defaults to config).
        scale: Top of the judge's scoring scale (default 5).

    Returns:
        A ``goal(state) -> bool`` function suitable for :func:`run_loop`.
    """
    def goal(state):
        verdict = judge(state, criteria, question=question, model=model, scale=scale)
        return verdict["score"] is not None and verdict["score"] >= threshold

    return goal


def run_loop(step, goal, start=None, max_iters=10):
    """
    Repeat ``step`` until ``goal`` is satisfied (or ``max_iters`` is reached).

    Args:
        step: ``step(state) -> new_state``. One iteration of work. The first
            call receives ``start``; each later call receives the previous
            result. This is the loop's "trigger" - what fires every turn.
        goal: ``goal(state) -> bool``. The stopping condition; return True when
            the result is good enough. Use a plain check or :func:`judged`.
        start: Initial state passed to the first ``step`` (default ``None``).
        max_iters: Safety bound so the loop always stops (default 10).

    Returns:
        dict with ``result`` (final state), ``iterations`` (how many steps ran),
        ``met_goal`` (whether ``goal`` was satisfied), and ``history`` (every
        intermediate state, in order).
    """
    state = start
    history = []
    for i in range(1, max_iters + 1):
        state = step(state)
        history.append(state)
        if goal(state):
            return {"result": state, "iterations": i, "met_goal": True, "history": history}
    return {"result": state, "iterations": len(history), "met_goal": False, "history": history}


def run_ratchet(step, score, start=None, max_iters=10):
    """
    Loop that only moves forward: keep a candidate only if it scores higher.

    This is the "Ralph Wiggum" / ratchet technique. Each iteration proposes one
    change, and the change is kept only when it improves the score - otherwise it
    is discarded (the loop's version of ``git revert``). Like a mechanical
    ratchet, the result only ever moves in one direction: toward a higher score.

    Args:
        step: ``step(best) -> candidate``. Propose one improvement to the
            current best state. Keep it to one change per loop.
        score: ``score(state) -> number | None``. Higher is better; often
            ``lambda s: judge(s, criteria)["score"]``. A ``None`` score is
            treated as "not an improvement" (never kept).
        start: Initial state; its score becomes the baseline to beat.
        max_iters: Number of proposals to try (default 10).

    Returns:
        dict with ``best`` (highest-scoring state), ``score`` (its score), and
        ``log`` - one row per iteration (``{"iteration", "score", "kept"}``),
        a tiny ``results.tsv`` you can inspect to see the ratchet at work.
    """
    best = start
    best_score = score(start) if start is not None else None
    log = []
    for i in range(1, max_iters + 1):
        candidate = step(best)
        s = score(candidate)
        kept = s is not None and (best_score is None or s > best_score)
        if kept:
            best, best_score = candidate, s
        log.append({"iteration": i, "score": s, "kept": kept})
    return {"best": best, "score": best_score, "log": log}
