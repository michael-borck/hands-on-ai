"""
LLM-as-judge: ask a language model to score an output against criteria.

This is how a lot of modern AI evaluation works: instead of hand-writing graders,
you ask a capable model to score a response. It is fast and flexible, but not
infallible, so treat the score as a signal, not a verdict.
"""

import re

from ..chat import get_response


def judge(output, criteria, question=None, model=None, scale=5):
    """
    Ask an LLM to score ``output`` against ``criteria``.

    Args:
        output: The text to evaluate.
        criteria: What "good" means here (e.g. "accurate, concise, and friendly").
        question: The original question the output answers (optional context).
        model: LLM model to use (defaults to config).
        scale: Top of the scoring scale (default 5; 1 is worst).

    Returns:
        dict: ``{"score": int | None, "reasoning": str, "raw": str}``.
    """
    system = (
        "You are a strict but fair evaluator. Score the response against the "
        f"criteria on a scale of 1 to {scale}, where {scale} is best. "
        "Reply with exactly two lines:\n"
        "SCORE: <number>\n"
        "REASONING: <one short sentence>"
    )

    parts = []
    if question:
        parts.append(f"Question:\n{question}")
    parts.append(f"Criteria:\n{criteria}")
    parts.append(f"Response to evaluate:\n{output}")

    reply = get_response("\n\n".join(parts), system=system, model=model)
    return _parse_verdict(reply, scale)


def _parse_verdict(reply, scale):
    """Pull a SCORE and REASONING out of the judge's reply."""
    score_match = re.search(r"SCORE:\s*(\d+)", reply, re.IGNORECASE)
    reason_match = re.search(r"REASONING:\s*(.*)", reply, re.IGNORECASE | re.DOTALL)

    score = None
    if score_match:
        score = max(1, min(scale, int(score_match.group(1))))  # clamp into range
    reasoning = reason_match.group(1).strip() if reason_match else reply.strip()

    return {"score": score, "reasoning": reasoning, "raw": reply}
