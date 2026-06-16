#!/usr/bin/env python
"""
End-to-end smoke test for hands-on-ai against a live LLM provider.

This exercises the main features (chat, streaming, memory, caching, evaluation,
and RAG) against whatever provider you have configured, and prints a PASS/FAIL
for each. It is handy as a release checklist: run it after a change to confirm
nothing is broken against a real model.

Usage:

    # Point at your provider (local Ollama shown here) and run it:
    export HANDS_ON_AI_SERVER=http://localhost:11434
    export HANDS_ON_AI_MODEL=gemma3:4b
    export HANDS_ON_AI_EMBEDDING_MODEL=nomic-embed-text   # for the RAG check
    python examples/smoke_test.py

The RAG check is skipped automatically if no embedding model is reachable.
Exit code is 0 if everything passed, 1 otherwise.
"""

import os
import sys
import tempfile
import time
from pathlib import Path

results = []


def check(name, passed, detail=""):
    """Record and print a single result."""
    results.append(bool(passed))
    mark = "PASS" if passed else "FAIL"
    print(f"[{mark}] {name}" + (f"  ->  {detail}" if detail else ""))


def skip(name, reason):
    print(f"[SKIP] {name}  ->  {reason}")


def main():
    from hands_on_ai.config import get_server_url, get_model
    print(f"Server: {get_server_url()}")
    print(f"Model:  {get_model()}\n")

    from hands_on_ai.chat import get_response, stream_response, Conversation

    # 1. Basic response
    r = get_response("Reply with exactly the word: pong")
    check("get_response", isinstance(r, str) and r and not r.startswith("❌"), repr(r[:50]))

    # 2. Token usage
    _, usage = get_response("Say hi in one word.", return_usage=True)
    check("return_usage", isinstance(usage, dict) and usage.get("total_tokens"), str(usage))

    # 3. Streaming
    chunks = list(stream_response("Count to three, words only."))
    check("stream_response", len(chunks) >= 2 and "".join(chunks).strip(), f"{len(chunks)} chunks")

    # 4. Conversation memory + save/load
    chat = Conversation(system="Be very concise.")
    chat.ask("My name is Sam. Remember it.")
    recall = chat.ask("What is my name? One word.")
    check("Conversation memory", "sam" in recall.lower(), repr(recall[:40]))
    path = Path(tempfile.mktemp(suffix=".json"))
    chat.save(path)
    check("Conversation save/load", Conversation.load(path).history() == chat.history())

    # 5. Caching: same prompt twice, the second should be an instant cache hit
    cache_dir = tempfile.mkdtemp()
    os.environ["HANDS_ON_AI_CACHE"] = cache_dir
    try:
        t0 = time.time(); a = get_response("Name one planet, one word."); t1 = time.time()
        b = get_response("Name one planet, one word."); t2 = time.time()
        miss, hit = t1 - t0, t2 - t1
        check("cache hit (same + faster)", a == b and hit < miss / 5,
              f"miss={miss:.2f}s hit={hit:.4f}s")
    finally:
        del os.environ["HANDS_ON_AI_CACHE"]

    # 6. Evaluation: a correct answer should score higher than a wrong one
    from hands_on_ai.eval import judge
    good = judge("Paris is the capital of France.", "factually correct",
                 question="Capital of France?")
    bad = judge("Berlin is the capital of France.", "factually correct",
                question="Capital of France?")
    check("judge scores good > bad", (good["score"] or 0) > (bad["score"] or 0),
          f"good={good['score']} bad={bad['score']}")

    # 7. RAG end-to-end (skipped if embeddings are unavailable)
    from hands_on_ai.rag.utils import (
        load_text_file, chunk_text, get_embeddings, save_index_with_sources, get_top_k,
    )
    docs = Path(tempfile.mkdtemp())
    (docs / "a.txt").write_text(
        "The Zorblax 3000 uses a 240 watt-hour graphene battery and weighs 3.2 kg.")
    (docs / "b.txt").write_text("Polaris Robotics was founded in 2021 in Fremantle.")
    chunks_, sources_ = [], []
    for f in sorted(docs.glob("*.txt")):
        for c in chunk_text(load_text_file(f)):
            chunks_.append(c)
            sources_.append(str(f))
    try:
        vectors = get_embeddings(chunks_)
    except Exception as e:
        skip("RAG retrieval", f"no embedding model? ({e})")
    else:
        index = str(docs / "index.npz")
        save_index_with_sources(vectors, chunks_, sources_, index)
        retrieved, scores = get_top_k(
            "What battery does the Zorblax use?", index, k=2, return_scores=True)
        top = retrieved[0][0]
        check("RAG retrieval", "graphene" in top.lower() or "battery" in top.lower(),
              f"top score={scores[0]:.3f}")
        answer = get_response(
            f"Answer only from the context.\nContext: {top}\n"
            "Q: What battery does the Zorblax use?")
        check("RAG grounded answer", "graphene" in answer.lower() or "240" in answer,
              repr(answer[:60]))

    # Summary
    passed, total = sum(results), len(results)
    print(f"\n{passed}/{total} checks passed.")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
