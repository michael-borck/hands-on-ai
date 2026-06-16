# Understanding Evaluation (LLM as Judge)

So far you've learned to *build* things: a [chat](chat-guide.md) reply, a
[RAG](rag-guide.md) answer, an [agent](agent-guide.md) that calls tools, a
[workflow](workflow-guide.md) of stages. This guide is about a different
question: **how do you know if any of it is actually good?**

## The gap this fills

You can build a bot in ten minutes. Deciding whether its answers are *correct*,
*clear*, and *on-topic* is the hard part. A bot that confidently returns nonsense
looks exactly like a bot that returns gold, until you read the output. As soon as
you have more than a handful of answers, reading every one yourself stops scaling.

## The manual way (and why it hurts)

The two common approaches both have problems:

- **Eyeballing it.** You skim the answers and form a gut feeling. This works for
  five answers and falls apart at fifty. It's also inconsistent: your judgement
  drifts depending on how tired or distracted you are.
- **Brittle string checks.** You assert the answer contains the word `"Paris"`.
  But `"The capital is Paris."` passes while `"That would be the city of Paris,
  France."` might fail your exact check, and `"Paris Hilton"` passes when it
  shouldn't. Natural language has too many right answers to pin down with string
  matching.

## The LLM-as-judge way

Instead of hand-writing graders, you ask a *capable model* to score the output
against criteria you describe in plain English. The judge reads the question, the
answer, and your definition of "good", then returns a number and a reason. This
is how a lot of modern AI evaluation works, because it handles paraphrasing,
tone, and partial correctness the way a human grader would.

Hands-On AI ships one small function for this:

```python
from hands_on_ai.eval import judge

result = judge(
    output="Paris is the capital of France.",
    criteria="Accurate, directly answers the question, and concise.",
    question="What is the capital of France?",
)

print(result)
```

A typical result looks like this:

```python
{
    "score": 5,
    "reasoning": "The answer is correct, direct, and concise.",
    "raw": "SCORE: 5\nREASONING: The answer is correct, direct, and concise.",
}
```

## Reading the result dict

`judge(...)` always returns a dict with three keys:

- **`score`**: an integer from `1` to `scale` (default `5`), or `None` if the
  judge's reply could not be parsed. The score is clamped into range, so you
  never get a `7` on a 5-point scale.
- **`reasoning`**: a short sentence explaining the score. This is often more
  useful than the number, because it tells you *why* an answer lost points.
- **`raw`**: the judge's full unparsed reply, handy when you want to debug a
  surprising score or a `None`.

The signature is:

```python
judge(output, criteria, question=None, model=None, scale=5)
```

`question` is optional context (the judge scores better when it knows what was
asked). `model` lets you pick a specific judge model, and `scale` sets the top of
the scoring range.

## Honest caveats

A judge is a useful signal, not a verdict. Keep these in mind:

- **Judges can be biased or fooled.** They sometimes reward confident, verbose,
  or flattering answers over correct ones. A wrong answer that *sounds* sure can
  score higher than a right answer that hedges.
- **Judges are inconsistent.** Run the same evaluation twice and you may get a
  4 then a 3. Small local models vary the most. Average several runs (or take a
  median) rather than trusting one number.
- **Write clear criteria.** Vague criteria ("is it good?") produce vague scores.
  A small rubric ("accurate, on-topic, under 50 words") gives the judge something
  concrete to check.
- **Don't let a model grade its own homework.** A model judging its own output is
  a weak signal: it tends to agree with itself. Use a different (ideally stronger)
  model as the judge where you can.
- **Never ship on a single score.** Use evaluation to compare options and catch
  regressions, not to declare one answer definitively "correct".

## Where it fits

Evaluation is the last of the five core concepts, and it loops back over all the
others:

```
chat  ->  rag  ->  agent  ->  workflow  ->  evaluation
```

You build with the first four, then *evaluate* to see whether the building
worked. Ready to try it? The [Judge Your Bot](projects/eval/judge-your-bot.md)
project walks you through building a tiny evaluation harness end to end.
