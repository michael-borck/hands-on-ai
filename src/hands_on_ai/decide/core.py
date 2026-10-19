"""
Typed judgments: small, fast decisions your code can use directly.

A chat model replies in prose. Programs usually need something smaller: one
of a fixed set of options, a yes/no decision, a score on a stated scale, or a
record pulled out of messy text. This module wraps those four judgments
(``classify``, ``decide``, ``score_output``, ``extract``) behind validated,
typed return values, so the rest of your program never parses paragraphs.

Two backends speak the same interface:

- ``backend="local"`` (default): your configured chat model, constrained to
  a Pydantic schema via Instructor. The *shape* is guaranteed; any
  confidence it reports is self-reported and uncalibrated.
- ``backend="jev"``: TypeSafe's Jev, a hosted System One model trained for
  calibrated decisions. Needs ``TYPESAFE_API_KEY``; probabilities there are
  the product. Returns ``None`` fields with an error when no key is set.

Every function returns a plain dict and never raises for a model-side
failure: unreadable or failed judgments come back with ``None`` values, the
raw text in ``raw``, and a message in ``error``, in the same spirit as
:func:`hands_on_ai.chat.get_response` returning error strings.
"""

import os

from pydantic import BaseModel, Field

from ..config import get_api_key, get_model, get_server_url, log

JEV_API_URL = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"


# --- schemas for the local (Instructor) backend ---


class _ChoiceReply(BaseModel):
    choice: str = Field(description="Exactly one of the listed options")
    confidence: float = Field(description="Your confidence from 0 to 1")
    reasoning: str = Field(description="One short sentence")


class _DecisionReply(BaseModel):
    answer: bool = Field(description="True if yes, False if no")
    probability: float = Field(description="Probability the answer is yes, 0 to 1")
    reasoning: str = Field(description="One short sentence")


class _ScoreReply(BaseModel):
    score: int = Field(description="Integer score on the stated scale")
    reasoning: str = Field(description="One short sentence")


# --- backends ---


def _structured_call(system, prompt, response_model, model):
    """
    One schema-validated call on the local backend. Returns the parsed
    Pydantic instance. Raises on failure; callers translate to dicts.
    Split out as the seam tests (and future backends) can stand in for.
    """
    import instructor
    from openai import OpenAI

    server_url = get_server_url()
    if not server_url.endswith("/v1"):
        server_url = server_url.rstrip("/") + "/v1"
    client = instructor.from_openai(
        OpenAI(base_url=server_url, api_key=get_api_key() or "hands-on-ai"),
        mode=instructor.Mode.JSON_SCHEMA,
    )
    return client.chat.completions.create(
        model=model or get_model(),
        response_model=response_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )


def _jev_call(state, questions):
    """
    One call to TypeSafe's System One endpoint. Returns the ``answers``
    dict. Raises on failure (including a missing API key).
    """
    import requests

    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        raise RuntimeError("TYPESAFE_API_KEY is not set")
    response = requests.post(
        JEV_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": JEV_MODEL, "state": state, "questions": questions},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["answers"]


def _empty(backend, error, **fields):
    out = dict(fields)
    out.update({"reasoning": "", "raw": "", "backend": backend, "error": str(error)})
    return out


# --- the four judgments ---


def classify(state, options, instructions=None, model=None, backend="local"):
    """
    Pick exactly one of ``options`` for ``state`` (TypeSafe's Choice,
    System-1 style).

    Returns dict: ``choice`` (one of options, or None), ``confidence``
    (Jev: derived from calibrated probabilities; local: self-reported),
    ``probabilities`` (Jev only, else None), ``reasoning``, ``raw``,
    ``backend``, ``error`` (None on success).
    """
    options = list(options)
    question = instructions or "Which option best fits this?"
    try:
        if backend == "jev":
            answers = _jev_call(state, {
                "q": {"type": "choice", "instructions": question,
                      "criteria": {o: None for o in options}},
            })
            a = answers["q"]
            choice = a["choice"] if a.get("choice") in options else None
            return {"choice": choice, "confidence": a.get("confidence"),
                    "probabilities": a.get("probabilities"), "reasoning": "",
                    "raw": str(a), "backend": backend, "error": None}
        reply = _structured_call(
            "You choose exactly one option from the list. "
            "Answer only through the required fields.",
            f"Text:\n{state}\n\nQuestion: {question}\nOptions: {', '.join(options)}",
            _ChoiceReply, model,
        )
        choice = reply.choice if reply.choice in options else None
        conf = max(0.0, min(1.0, float(reply.confidence)))
        return {"choice": choice, "confidence": conf, "probabilities": None,
                "reasoning": reply.reasoning, "raw": reply.model_dump_json(),
                "backend": backend, "error": None}
    except Exception as e:  # model or transport failure: report, never raise
        log.warning(f"classify failed ({backend}): {e}")
        return _empty(backend, e, choice=None, confidence=None, probabilities=None)


def decide(state, question, model=None, backend="local"):
    """
    Answer a yes/no ``question`` about ``state`` (TypeSafe's Noul).

    Returns dict: ``answer`` (bool or None), ``probability`` (P(yes);
    calibrated on Jev, self-reported locally), ``reasoning``, ``raw``,
    ``backend``, ``error``.
    """
    try:
        if backend == "jev":
            answers = _jev_call(state, {
                "q": {"type": "noul", "instructions": question},
            })
            p = answers["q"]["noul"]
            p = max(0.0, min(1.0, float(p)))
            return {"answer": p >= 0.5, "probability": p, "reasoning": "",
                    "raw": str(answers["q"]), "backend": backend, "error": None}
        reply = _structured_call(
            "You answer one yes/no question. Answer only through the required fields.",
            f"Text:\n{state}\n\nQuestion: {question}",
            _DecisionReply, model,
        )
        p = max(0.0, min(1.0, float(reply.probability)))
        return {"answer": bool(reply.answer), "probability": p,
                "reasoning": reply.reasoning, "raw": reply.model_dump_json(),
                "backend": backend, "error": None}
    except Exception as e:
        log.warning(f"decide failed ({backend}): {e}")
        return _empty(backend, e, answer=None, probability=None)


def score_output(output, criteria, question=None, model=None, scale=5, backend="local"):
    """
    Score ``output`` against ``criteria`` from 1 to ``scale`` (the Judge,
    in typed form).

    Returns the judge-shaped dict: ``score`` (int, clamped, or None),
    ``reasoning``, ``raw``, plus ``backend`` and ``error``. On Jev the
    weighted level score is rounded into 1..scale.
    """
    try:
        if backend == "jev":
            levels = [f"Score {i} of {scale}: {criteria}" for i in range(1, scale + 1)]
            state = f"Question:\n{question}\n\nResponse:\n{output}" if question else str(output)
            answers = _jev_call(state, {
                "q": {"type": "score",
                      "instructions": f"Score the response against: {criteria}",
                      "criteria": levels},
            })
            a = answers["q"]
            # Jev levels are 0-based and probability-weighted; +1, then round.
            score = max(1, min(scale, round(float(a["score"])) + 1))
            return {"score": score, "reasoning": "", "raw": str(a),
                    "backend": backend, "error": None}
        parts = []
        if question:
            parts.append(f"Question:\n{question}")
        parts.append(f"Criteria:\n{criteria}")
        parts.append(f"Response to evaluate:\n{output}")
        reply = _structured_call(
            "You are a strict but fair evaluator. Score the response against "
            f"the criteria on a scale of 1 to {scale}, where {scale} is best.",
            "\n\n".join(parts), _ScoreReply, model,
        )
        score = max(1, min(scale, int(reply.score)))
        return {"score": score, "reasoning": reply.reasoning,
                "raw": reply.model_dump_json(), "backend": backend, "error": None}
    except Exception as e:
        log.warning(f"score_output failed ({backend}): {e}")
        return _empty(backend, e, score=None)


def extract(text, schema, instructions=None, model=None):
    """
    Pull a typed record out of ``text`` using a Pydantic model class
    (``schema``). Local backend only; Jev judges, it does not extract.

    Returns dict: ``data`` (validated dict, or None), ``raw``,
    ``backend``, ``error``.
    """
    try:
        reply = _structured_call(
            "Extract exactly the requested fields from the text. "
            "Leave a field empty rather than inventing a value.",
            (instructions + "\n\n" if instructions else "") + f"Text:\n{text}",
            schema, model,
        )
        return {"data": reply.model_dump(), "raw": reply.model_dump_json(),
                "backend": "local", "error": None}
    except Exception as e:
        log.warning(f"extract failed: {e}")
        return _empty("local", e, data=None)
