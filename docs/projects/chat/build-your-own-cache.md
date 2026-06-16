# Build Your Own Cache

**Difficulty**: Intermediate  
**Time**: 35 minutes  
**Learning Focus**: Caching, hashing, reproducibility  
**Module**: chat

## Overview

A cache remembers an answer the first time you ask for it, then hands back the
saved copy whenever you ask the same thing again. In this project you will build
a tiny response cache from scratch (about 25 lines), understand exactly how it
works, and then meet the built-in version that does the same job with a single
environment variable.

> 🧠 **Why caching matters in a classroom.** Caching turns a chatty,
> network-dependent tool into something calm and predictable:
> - **Reproducible reruns**: every student who runs the same notebook gets the same answer.
> - **No repeated cost**: the model is only called once per unique question.
> - **Works offline once warmed**: after the first run, answers come from disk.
> - **Survives flaky wifi**: a lab full of laptops will not stall on a slow connection.

## Build it yourself

A cache only needs to do two things: turn the inputs into a stable filename, and
read or write that file. We will use `hashlib.sha256` to turn `(model, system,
prompt)` into a short, unique key.

```python
import hashlib
from pathlib import Path
from hands_on_ai.chat import get_response

MY_CACHE = Path("./my_cache")  # a folder to hold one file per answer


def cached_response(prompt, system="You are a helpful assistant.", model="llama3"):
    # Turn the three inputs into one stable filename.
    key_text = f"{model}\n{system}\n{prompt}"
    key = hashlib.sha256(key_text.encode("utf-8")).hexdigest()
    cache_file = MY_CACHE / f"{key}.txt"

    # Cache hit: read the saved answer and skip the model entirely.
    if cache_file.exists():
        print("(from cache)")
        return cache_file.read_text(encoding="utf-8")

    # Cache miss: call the model, then save the answer for next time.
    print("(calling the model)")
    answer = get_response(prompt, system=system, model=model)
    MY_CACHE.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(answer, encoding="utf-8")
    return answer


# First call hits the model and writes a file. Second call reads the file.
print(cached_response("Name three primary colours."))
print(cached_response("Name three primary colours."))
```

Run it twice and watch the printout: the first call says `(calling the model)`,
the second says `(from cache)` and returns instantly. That is the whole idea.
Notice the key depends on the model, system, and prompt together, so changing any
one of them produces a different filename and a fresh answer.

## Use the built-in cache

The library already ships exactly this behaviour. It is **off by default** and
opt-in: you switch it on by pointing the `HANDS_ON_AI_CACHE` environment variable
at a directory.

```bash
export HANDS_ON_AI_CACHE=~/.hands-on-ai/cache
```

Now ordinary `get_response` calls are cached automatically, with no change to
your code:

```python
from hands_on_ai.chat import get_response

# First call: reaches the model and saves the answer.
print(get_response("Name three primary colours."))

# Second identical call: returned from disk, instant and free.
print(get_response("Name three primary colours."))
```

The cache key is the same `(model, system, prompt)` triple you built by hand. To
clear the cache, just delete the directory. Note that caching is skipped while
streaming (`stream=True`), since streamed output arrives piece by piece.

You can also reach the helpers directly to inspect or pre-warm the cache:

```python
from hands_on_ai import cache

print(cache.cache_dir())                         # where files live (or None if disabled)
cache.put("llama3", "You are a helpful assistant.", "Hi", "Hello there!")
print(cache.get("llama3", "You are a helpful assistant.", "Hi"))  # "Hello there!"
```

## Extensions

**Add a max-age (expiry).** Treat files older than, say, one day as a miss so
content refreshes occasionally:

```python
import time

MAX_AGE_SECONDS = 24 * 60 * 60
if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < MAX_AGE_SECONDS:
    return cache_file.read_text(encoding="utf-8")
```

**Cache embeddings for RAG.** Embedding the same documents every run is slow.
Apply the same pattern, but hash the document text and store the vector (as JSON)
instead of a chat answer.

**Warm the cache before class.** Pre-run a list of prompts so every answer is
already on disk when students arrive:

```python
from hands_on_ai.chat import get_response  # uses HANDS_ON_AI_CACHE if it is set

prompts = [
    "What is a variable?",
    "Explain a for loop in one sentence.",
    "Name three primary colours.",
]
for p in prompts:
    get_response(p)  # answer is fetched once and saved
print("Cache warmed.")
```

**Peek at a cache file on disk.** Each entry is one plain-text file named by its
sha256 hash. Have a look:

```bash
ls ~/.hands-on-ai/cache
cat ~/.hands-on-ai/cache/3f9a...c1.txt   # the saved answer, in plain text
```

## A note on natural variation

Caching assumes that the same input always means the same answer. That is exactly
what you want for teaching and reproducibility: stable, repeatable results that do
not cost anything to rerun. The trade-off is that it hides the model's natural
variation, so two "identical" questions will never surprise you with a different
phrasing. When you want fresh responses (for brainstorming, or to show how a model
varies), turn caching off by unsetting the variable:

```bash
unset HANDS_ON_AI_CACHE
```
