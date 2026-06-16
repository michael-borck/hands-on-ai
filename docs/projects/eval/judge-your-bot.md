# Judge Your Bot

**Difficulty**: Intermediate  
**Time**: 40 minutes  
**Learning Focus**: Evaluation, LLM-as-judge, rubrics  
**Module**: eval

## Overview

You've built bots in the earlier projects. Now you'll build a tiny **evaluation
harness**: a handful of test questions, a bot that answers them, and a *judge*
model that scores each answer against criteria you define. By the end you'll have
a small score table and an average, and you'll see how much those scores wobble
between runs.

> 🧠 **Evaluation in one line:** instead of guessing whether an answer is good,
> ask a capable model to score it against clear criteria. See
> [Understanding Evaluation](../../eval-guide.md) for the concepts.

## Step 1: Define your test questions

Start with a few questions where *you* know roughly what a good answer looks like.
Keep it small so you can sanity-check the judge's scores yourself.

```python
questions = [
    "What is the capital of France?",
    "Explain what a variable is in programming, in one sentence.",
    "What is 17 multiplied by 4?",
]
```

## Step 2: Generate answers with a bot

Use the chat module to answer each question. This is the "thing under test".

```python
from hands_on_ai.chat import get_response

answers = [get_response(q) for q in questions]

for q, a in zip(questions, answers):
    print(f"Q: {q}\nA: {a}\n")
```

## Step 3: Score each answer with the judge

Now bring in the judge. For each answer, score it against criteria. Passing the
original `question` gives the judge context, so it knows what the answer was
supposed to address.

```python
from hands_on_ai.eval import judge

criteria = "Accurate, directly answers the question, and concise."

results = []
for q, a in zip(questions, answers):
    r = judge(a, criteria, question=q)
    results.append(r)
```

Each `r` is a dict: `{"score": int or None, "reasoning": str, "raw": str}`.

## Step 4: Print a small score table

```python
print(f"{'Score':<6} | Question")
print("-" * 50)
for q, r in zip(questions, results):
    score = r["score"] if r["score"] is not None else "?"
    print(f"{str(score):<6} | {q[:40]}")
```

You'll get something like:

```
Score  | Question
--------------------------------------------------
5      | What is the capital of France?
4      | Explain what a variable is in programming
5      | What is 17 multiplied by 4?
```

## Step 5: Average the scores

Skip any `None` scores (a reply the judge couldn't be parsed from), then average
what's left.

```python
scores = [r["score"] for r in results if r["score"] is not None]
average = sum(scores) / len(scores) if scores else 0
print(f"Average score: {average:.2f} over {len(scores)} answers")
```

## Step 6: Run it twice and watch the variance

Run Steps 3 to 5 again without changing anything. You'll likely see at least one
score move (a 4 becomes a 3, or the average shifts by half a point). That wobble
is the single most important lesson here: **a judge gives you a signal, not a
verdict.** One run is noisy. Trends across runs are trustworthy.

## Extensions

Pick any of these to go deeper:

- **A richer rubric.** Replace the single criteria string with several explicit
  checks, and let the judge weigh them: `"Score on: (1) factual accuracy, (2)
  staying on topic, (3) brevity under 30 words."`
- **Head-to-head.** Generate answers from two different bots or models, judge
  both with the same criteria, and compare their averages to see which wins.
- **Median of three.** Judge each answer three times and take the median score.
  This smooths out the run-to-run wobble you saw in Step 6.

  ```python
  import statistics

  def stable_score(answer, criteria, question, runs=3):
      scores = []
      for _ in range(runs):
          r = judge(answer, criteria, question=question)
          if r["score"] is not None:
              scores.append(r["score"])
      return statistics.median(scores) if scores else None
  ```

- **Flag the failures.** Print only the answers that score below a threshold, so
  you can review the weak ones by hand:

  ```python
  threshold = 4
  for q, a, r in zip(questions, answers, results):
      if r["score"] is not None and r["score"] < threshold:
          print(f"LOW ({r['score']}): {q}\n  -> {a}\n  reason: {r['reasoning']}\n")
  ```

## How it works under the hood

The judge is about 40 lines of plain Python in
[`hands_on_ai/eval/judge.py`](https://github.com/teaching-repositories/hands-on-ai/blob/main/src/hands_on_ai/eval/judge.py).
It builds a system prompt asking the model to reply with exactly two lines,
`SCORE:` and `REASONING:`, sends your question, criteria, and answer through
`get_response`, then uses a small regex to pull the number and the sentence back
out. The score is clamped into the `1..scale` range, and if no `SCORE:` line is
found, `score` comes back as `None` with the full reply preserved in `raw`. No
magic: just a careful prompt and some parsing.
