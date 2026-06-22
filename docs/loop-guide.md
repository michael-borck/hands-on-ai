# Understanding Loops

So far every module has been a single pass: send a prompt, get a response. But a
lot of useful AI work is not one-shot. You draft, you check, you revise, and you
keep going until the result is good enough. That is a **loop**.

> 🧠 **The big idea: a loop is the same shape, repeated.** Do something, check
> whether you are done, repeat. Two small functions cover it.

## The two pieces of any loop

Every loop, no matter how fancy, has just two parts:

- **A trigger.** What starts and drives the loop. Here that is a `start` value
  plus a `step` function that runs each turn.
- **A goal.** How the loop knows to stop. Here that is a `goal(state)` check that
  returns `True` when you are done. The goal can be a plain Python test, or an
  LLM judge from the [eval module](eval-guide.md).

That is the whole concept. The rest is detail.

## `run_loop`: repeat until the goal is met

```python
from hands_on_ai.chat import get_response
from hands_on_ai.loop import run_loop, judged

result = run_loop(
    step=lambda draft: get_response(f"Improve this paragraph, keep it short:\n{draft}"),
    goal=judged("clear, concise, and friendly", threshold=4),
    start="loops are when you do stuff again and again",
    max_iters=5,
)

print(result["result"])       # the final paragraph
print(result["iterations"])   # how many turns it took
print(result["met_goal"])     # did we reach the goal, or run out of turns?
```

`run_loop` calls `step` over and over. The first call gets `start`; each later
call gets the previous result. After every step it asks `goal`: done yet? It
stops the moment the goal is satisfied, or when it hits `max_iters`.

> ⏱️ **Why `max_iters` and not a timer?** Real agent frameworks often cap a loop
> by wall-clock time (a "fixed time budget"). For learning we cap by *number of
> iterations* instead: it always stops, it is cheap, and it gives the same
> result every run. That is the right trade for a classroom.

### The goal can be code, or a judge

A goal is just a function that returns `True` or `False`. Sometimes a plain check
is all you need:

```python
run_loop(
    step=lambda n: n + 1,
    goal=lambda n: n >= 10,
    start=0,
)
```

When "good" is fuzzy ("is this explanation clear?"), use `judged`, which wraps
the eval LLM judge so a natural-language standard becomes your stopping
condition. This is the same "LLM-as-judge" idea from the eval module, now used
to *end a loop* instead of just scoring one answer.

## `run_ratchet`: only move forward (the Ralph Wiggum loop)

What if every improvement is not actually an improvement? Models wander. A
"better" rewrite can quietly make things worse. The **ratchet loop** fixes this:
it keeps a change *only if it scores higher* than the best so far. Everything
else is thrown away.

```python
from hands_on_ai.eval import judge
from hands_on_ai.loop import run_ratchet

result = run_ratchet(
    step=lambda best: get_response(f"Make one small improvement:\n{best}"),
    score=lambda text: judge(text, "clear and accurate")["score"],
    start="my first draft",
    max_iters=10,
)

print(result["best"])    # highest-scoring version found
print(result["log"])     # one row per turn: {"iteration", "score", "kept"}
```

Like a mechanical ratchet, the result only ever moves in one direction: toward a
higher score. A turn that does not improve things is simply not kept, which is
the loop's version of "undo". This technique is sometimes called the **Ralph
Wiggum loop** after the idea that even a very simple, repetitive agent reaches a
good result if it can only ever ratchet forward.

The `log` it returns is a tiny results table. Print it and you can watch the
ratchet work: scores bounce around, but `best` never goes down.

## Where this goes next

This module is deliberately small so the *shape* is obvious. The serious version
of this idea, sometimes called "agentic engineering", adds a lot more:

- a **fixed time budget** per turn instead of an iteration count,
- a **three-file contract** that makes the judge immutable so the agent cannot
  cheat by editing the test,
- **git as memory**, committing each kept change and resetting to undo a bad one,
- **backpressure**: type checkers, tests, and "no placeholder code" rules that
  reject low-quality work before it lands.

You do not need a new library to try those. You build them on top of the two
functions here. The [Build a Ralph Loop](projects/loop/build-a-ralph-loop.md)
project walks through exactly that. When you outgrow hand-rolled loops, that is
the moment to reach for a dedicated agent framework.
