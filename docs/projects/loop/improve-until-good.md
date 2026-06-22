# Improve Until Good

**Difficulty**: Beginner / Intermediate  
**Time**: 30 minutes  
**Learning Focus**: Loops, trigger and goal, LLM-as-judge as a stopping condition  
**Module**: loop

## Overview

In this project you'll build a loop that rewrites a paragraph over and over until
a judge says it is good enough. You'll see the two pieces every loop has: a
**trigger** (what runs each turn) and a **goal** (when to stop).

> 🧠 **The big idea: do, check, repeat.** A loop is just a step you run again and
> again until a goal is met. See [Understanding Loops](../../loop-guide.md) for
> the concepts.

## What you'll build

A "polish" loop:

```
draft -> improve -> judge -> good enough? -> stop
              ^___________________|  (if not, go again)
```

## Step 1: A loop with a plain goal

Start simple. The goal is just a Python function. Here we keep asking the model
to shorten a sentence until it is under 80 characters.

```python
from hands_on_ai.chat import get_response
from hands_on_ai.loop import run_loop

result = run_loop(
    step=lambda text: get_response(f"Rewrite this in fewer words:\n{text}"),
    goal=lambda text: len(text) <= 80,
    start="In this particular instance, it would seem that brevity is somewhat lacking.",
    max_iters=5,
)

print(result["result"])
print("Took", result["iterations"], "turns. Met goal:", result["met_goal"])
```

Run it a few times. Notice:

- `step` is the **trigger**: it fires every turn, and each turn gets the previous
  turn's output as its input.
- `goal` is the **stopping condition**.
- `max_iters` guarantees the loop ends even if the goal is never met. Look at
  `met_goal` to see which way it stopped.

## Step 2: A goal the model decides (LLM-as-judge)

"Under 80 characters" is easy to check in code. But most real goals are fuzzy:
*is this clear? is it friendly?* For those, use `judged`, which turns the
[eval](../../eval-guide.md) LLM judge into a goal.

```python
from hands_on_ai.chat import get_response
from hands_on_ai.loop import run_loop, judged

draft = "loops are when you do stuff again and again until its done i guess"

result = run_loop(
    step=lambda text: get_response(f"Improve this explanation, keep it short:\n{text}"),
    goal=judged("clear, accurate, and friendly for a beginner", threshold=4),
    start=draft,
    max_iters=6,
)

print(result["result"])
```

Now the loop keeps polishing until the judge scores the text 4 out of 5 or
better. The same LLM-as-judge idea you used to *score* an answer in the eval
module is now being used to *end a loop*.

## Step 3: Watch the loop think

The result includes the full `history`, so you can see every draft the loop
produced:

```python
for i, draft in enumerate(result["history"], start=1):
    print(f"--- turn {i} ---")
    print(draft)
```

## Make it your own

- Swap the goal: "no longer than three sentences", "contains a concrete
  example", "reading level of a 12 year old" (use `judged` for the fuzzy ones).
- Change `threshold` to 5 and watch how many more turns it takes (or whether it
  gives up at `max_iters`).
- Loop over something other than text: a number, a list of ideas, a bit of code.

## Where to go next

When a single forward pass is not enough and you want the loop to *only keep
improvements*, move on to [Build a Ralph Loop](build-a-ralph-loop.md), where the
loop ratchets toward a higher score and uses git to remember its best work.
