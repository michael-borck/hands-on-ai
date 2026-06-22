# Build a Ralph Loop

**Difficulty**: Advanced  
**Time**: 90 minutes  
**Learning Focus**: Ratchet loops, the three-file contract, git as memory, backpressure  
**Module**: loop

## Overview

In this project you'll build a small **autonomous improvement loop** by hand, the
kind people mean by "agentic engineering". The loop proposes one change at a
time, scores it, keeps it only if it got better, and uses git to remember its
best work and undo its mistakes. It is sometimes called the **Ralph Wiggum
loop**: even a very simple, repetitive agent does well if it can only ever
ratchet forward.

You'll build it on top of [`run_ratchet`](../../loop-guide.md) and the
[eval judge](../../eval-guide.md). Nothing here needs a new framework. The point
is to see the moving parts before you ever reach for one.

> 🧠 **The big idea: forward-only.** A ratchet loop keeps a change *only if it
> scores higher* than the best so far. Everything else is thrown away, so the
> result can only improve.

## The three-file contract

The trick that makes an autonomous loop trustworthy is separating what the agent
may touch from what it may not. We use three roles:

| File | Role | Who may change it |
|------|------|-------------------|
| `judge.py` | **The immutable judge.** Defines what "good" means and how to score. | You only. The loop must never edit it. |
| `work.txt` (or `solution.py`) | **The sandbox.** The thing being improved. | The loop, freely. |
| `program.md` | **The human directive.** The goal, constraints, and baseline score. | You only. |

Why keep the judge off-limits to the loop? So the loop cannot "cheat" by making
the test easier. The standard stays fixed, so every turn is measured the same
way. This is the single most important idea in the whole project.

## Step 1: Write the immutable judge

`judge.py` is the standard the loop is held to. Keep it small and never let the
loop modify it.

```python
# judge.py
from hands_on_ai.eval import judge

CRITERIA = "a clear, friendly, beginner-level explanation of what a loop is"

def score(text):
    """Return an integer 1..5. Higher is better. Never edited by the loop."""
    verdict = judge(text, CRITERIA)
    return verdict["score"] or 1   # treat an unparseable verdict as the worst
```

## Step 2: Write the human directive

`program.md` is where *you* set the agenda. The loop reads it for priorities; you
also record the baseline so you can see progress.

```markdown
# Goal
Explain "what is a loop" so a 12 year old understands it in under 4 sentences.

# Constraints
- All else being equal, simpler is better.
- No jargon without a one-line definition.

# Baseline
score: 2   (the starting draft below)
```

## Step 3: The ratchet

This is the heart of the loop. `run_ratchet` proposes a change, scores it with
the immutable judge, and keeps it only if it beats the best so far.

```python
from pathlib import Path
from hands_on_ai.chat import get_response
from hands_on_ai.loop import run_ratchet
from judge import score, CRITERIA

directive = Path("program.md").read_text()
start = "a loop is when the computer does the thing over and over"

def propose(best):
    return get_response(
        f"{directive}\n\n"
        f"Here is the current best version:\n{best}\n\n"
        "Make ONE small improvement. Return only the improved text."
    )

result = run_ratchet(step=propose, score=score, start=start, max_iters=15)

print("Best score:", result["score"])
print(result["best"])
```

> 📏 **One thing per loop.** Notice the prompt asks for *one* small change, not a
> rewrite. Small steps are easier to score and easier to undo. This is the
> discipline that keeps a ratchet loop stable.

## Step 4: A budget you can reason about

Real systems cap each turn by wall-clock time (a "fixed time budget") so that
slow, over-complex attempts are naturally penalised. Here we use `max_iters`
instead: it is deterministic, cheap, and always stops. As a stretch goal, wrap
`propose` with a timer and abandon a turn that runs too long, then compare the
behaviour.

## Step 5: Git as memory

The ratchet remembers the *best text in memory*. To make it survive across runs,
write the best version to the sandbox file and commit every time it improves,
so git becomes your log of progress and your undo button.

```python
import subprocess
from pathlib import Path

def commit_if_improved(result, row):
    if row["kept"]:
        Path("work.txt").write_text(result["best"])
        subprocess.run(["git", "add", "work.txt"])
        subprocess.run(["git", "commit", "-m", f"score {row['score']}"])
```

Now `git log` is the history of the loop's wins, and `git reset --hard <commit>`
sends it back to any earlier high point. That "reset to an earlier checkpoint"
move is how a human breaks the loop out of a rut.

## Step 6: Backpressure (reject bad work before it lands)

A judge score is one form of **backpressure**: a gate that stops weak work from
being kept. Add more gates and the loop gets sturdier:

- **A hard check before scoring.** Reject a candidate outright if it is empty,
  contains `TODO`, or is shorter than a sentence, before you even pay for a judge
  call. Make `score` return `1` for those.
- **"Full implementations only."** When the sandbox is code, run a type checker
  or the test suite and treat a failure as the worst score. The loop literally
  cannot keep code that does not compile or pass.
- **An auditor pass.** Every few turns, ask a separate model "what is missing or
  faked here?" and feed its answer back into `program.md` as the next priority.

## Step 7: Watch the ratchet work

```python
print("iter\tscore\tkept")
for row in result["log"]:
    print(f"{row['iteration']}\t{row['score']}\t{row['kept']}")
```

The scores will bounce around, but `result["best"]` only ever goes up. That is
the ratchet.

## Reflection: the creativity ceiling

Run the loop long enough and it stalls. Because the ratchet only accepts
immediate improvements, it cannot take a step backward to make a leap forward, so
it gets stuck at a local best. This is the **creativity ceiling**, and it is
exactly where a human belongs: rewrite `program.md` with a new priority, hard
reset to an earlier checkpoint, or start the draft from a different angle.

## Where to go next

You have now built, by hand, the core of an autonomous coding loop: a fixed
judge, a sandbox, a directive, a forward-only ratchet, git memory, and
backpressure. When you want time budgets, parallel sub-agents, and richer state
management for real, that is the point to graduate to a dedicated agent
framework. You'll understand exactly what it is doing for you, because you built
the simple version first.
