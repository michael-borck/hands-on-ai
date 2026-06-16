"""
Optional on-disk response cache.

Caching is **off by default**. Enable it by setting the ``HANDS_ON_AI_CACHE``
environment variable to a directory:

    export HANDS_ON_AI_CACHE=~/.hands-on-ai/cache

When enabled, :func:`hands_on_ai.chat.get_response` returns a saved answer for an
identical ``(model, system, prompt)`` instead of calling the model again. This is
useful in classrooms: reruns are reproducible, repeated calls cost nothing, and a
warmed cache works offline.

The cache is intentionally simple: one plain-text file per entry, named by a hash
of the inputs. Delete the directory to clear it.
"""

import hashlib
import json
import os
from pathlib import Path


def cache_dir():
    """Return the cache directory as a Path if caching is enabled, else None."""
    d = os.environ.get("HANDS_ON_AI_CACHE")
    return Path(d).expanduser() if d else None


def _key(model, system, prompt):
    raw = json.dumps({"model": model, "system": system, "prompt": prompt}, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get(model, system, prompt):
    """Return a cached response string, or None on a miss (or when disabled)."""
    d = cache_dir()
    if d is None:
        return None
    f = d / f"{_key(model, system, prompt)}.txt"
    return f.read_text(encoding="utf-8") if f.exists() else None


def put(model, system, prompt, response):
    """Store a response in the cache. No-op when caching is disabled."""
    d = cache_dir()
    if d is None:
        return
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{_key(model, system, prompt)}.txt").write_text(response, encoding="utf-8")
