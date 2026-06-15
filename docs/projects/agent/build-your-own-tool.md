# Build Your Own Tool (Cookbook)

**Difficulty**: Intermediate  
**Time**: 30 minutes  
**Learning Focus**: The tool contract, extending agents, calling external APIs safely  
**Module**: agent

## Overview

Agents are only as capable as the tools you give them. This cookbook shows the
one pattern behind *every* tool — built-in or your own — so you can add new
abilities without guessing.

## The one rule: a tool is `str -> str`

An agent tool is just a function that takes a single string and returns a single
string. You `register_tool` it so the agent can call it by name.

```python
from hands_on_ai.agent import register_tool, run_agent

def shout(text: str) -> str:
    """Return the text in uppercase."""
    return text.upper()

register_tool(
    name="shout",
    description="Convert text to uppercase. Input: the text to shout.",
    function=shout,
)

# The agent can now choose to call `shout` when it helps.
print(run_agent("Use the shout tool on 'hello world'"))
```

That's the whole contract:

- **Input** — one string (whatever the model decides to pass).
- **Output** — one string (what the agent reads back).
- **Description** — the model reads *this* to decide when and how to use your
  tool. Write it like a help message, and say what the input should look like.

> 💡 A tool can do anything a Python function can — math, a lookup, an API call,
> reading a file. The agent doesn't care how; it only sees the string you return.

## Handling more than one input

The agent passes a *single* string, so if your tool needs several values, parse
them yourself. Pick a simple, documented format and split on it:

```python
def repeat(spec: str) -> str:
    """Input format: 'text | count', e.g. 'ha | 3'."""
    try:
        text, count = spec.split("|")
        return text.strip() * int(count)
    except Exception:
        return "Error: expected input like 'text | count'."
```

Then describe that format in the `description` so the model sends the right shape.

## The web pattern: fetch → parse → return

Every tool that reaches the internet follows the same three steps. Here's one
that reports a GitHub repo's star count:

```python
import requests   # pip install requests

def github_stars(repo: str) -> str:
    """Input: 'owner/name', e.g. 'python/cpython'."""
    try:
        # 1. FETCH
        resp = requests.get(f"https://api.github.com/repos/{repo}", timeout=10)
        resp.raise_for_status()
        # 2. PARSE — pull out just the fact you need
        stars = resp.json()["stargazers_count"]
        # 3. RETURN a short, plain-text answer
        return f"{repo} has {stars:,} stars."
    except Exception as e:
        return f"Error fetching repo info: {e}"

register_tool(
    "github_stars",
    "Get the star count of a GitHub repo. Input: 'owner/name'.",
    github_stars,
)
```

Fetch, keep only what you need, return a short string. The same shape works for
weather, news, dictionaries — anything.

> ⚠️ **External APIs are the part that dates.** Endpoints change, fields get
> renamed, and services add rate limits or sign-up requirements. The *library*
> stays deliberately offline and stable — wiring up a live API is your code's job,
> not the library's. Treat a broken API as a real-world lesson, not a bug in
> `hands-on-ai`.

### If the API needs a key

Never hard-code secrets or commit them to git. Read them from an environment
variable instead:

```python
import os

def weather(city: str) -> str:
    key = os.environ.get("OPENWEATHER_API_KEY")
    if not key:
        return "Error: set OPENWEATHER_API_KEY in your environment first."
    # ... fetch → parse → return as above ...
```

The [Weather Dashboard](../chat/weather-dashboard.md) project shows this end to end.

## Simulated vs. real

The built-in `search` and `weather` tools return **simulated** data on purpose:
no keys, no rate limits, identical results every run — ideal for a classroom. A
real version trades that reliability for fresh data. Both are valid, and choosing
between them *is* part of the lesson.

## A good-tool checklist

- ✅ One string in, one string out.
- ✅ A clear `description` — the model uses it to decide when to call the tool and what to pass.
- ✅ Return concise text. The agent re-reads your output; a wall of JSON confuses small models.
- ✅ Handle errors by **returning** an error string — don't `raise`. A tool that crashes can end the agent run.
- ✅ Prefer deterministic/offline tools; reach for the network only when freshness is the whole point.
- ✅ Keep secrets in environment variables, never in code.

## Try it

1. Build a tool that reverses a string, then ask the agent to use it.
2. Build a dictionary tool using a free, keyless API (fetch → parse → return).
3. Convert one of your tools to read an API key from the environment.

Once you're comfortable here, the [Custom Tool Creator](custom-tool-creator.md)
project challenges you to build a small toolbox of your own.
