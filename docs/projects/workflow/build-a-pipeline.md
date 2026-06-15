# Build a Pipeline

**Difficulty**: Intermediate  
**Time**: 45 minutes  
**Learning Focus**: Workflow orchestration, context engineering, human-in-the-loop  
**Module**: workflow

## Overview

In this project you'll build a multi-step AI workflow the simple way, as a
**folder of stages**, with no orchestration framework. You'll run it one step at
a time, reading and editing the intermediate files, so *you* stay in control of
the result.

> 🧠 **The big idea: folders over frameworks.** A workflow is just numbered
> stage folders. Each stage has a `CONTEXT.md` (its instructions) and writes an
> `output/output.md`. One model walks the stages in order, and you review the
> file between each step. See [Understanding Workflows](../../workflow-guide.md)
> for the concepts.

## What you'll build

A two-stage "explainer" pipeline:

```
01_research  →  02_explain
(gather facts)   (turn them into a friendly explanation)
```

You'll run stage 1, read its output, *optionally edit it*, then run stage 2,
which uses your reviewed research as its input.

## Step 1: Create the workspace

```python
from hands_on_ai.workflow import init_workspace

init_workspace(
    "explainer",
    ["research", "explain"],
    system="You are a careful assistant. Do exactly what each stage asks.",
)
```

This creates:

```
explainer/
├── CONTEXT.md
├── references/
└── stages/
    ├── 01_research/
    │   ├── CONTEXT.md
    │   └── output/
    └── 02_explain/
        ├── CONTEXT.md
        └── output/
```

## Step 2: Write the stage contracts

Each stage's `CONTEXT.md` is just instructions in plain English. Edit them:

`explainer/stages/01_research/CONTEXT.md`:

```markdown
# Stage 01: Research

Pick the topic "how vaccines work" and list 5 plain, accurate facts about it.
Output a numbered list. No introduction, just the list.
```

`explainer/stages/02_explain/CONTEXT.md`:

```markdown
# Stage 02: Explain

Using the research facts provided as input, write a friendly 150-word
explanation suitable for a 12-year-old. Keep every claim grounded in the facts.
```

Notice stage 2 never mentions the topic. It just transforms whatever stage 1
produced. That's the point: each stage does **one** thing.

## Step 3: Run it, one stage at a time

```python
from hands_on_ai.workflow import Pipeline

pipe = Pipeline("explainer")
pipe.status()        # [ ] 01_research   [ ] 02_explain

result = pipe.run_next()     # runs ONLY stage 01, then stops
print(result["output_path"]) # explainer/stages/01_research/output/output.md
```

Now **open that output file and read it.** This is the human-in-the-loop moment:
if a fact looks wrong, *edit the file and save it*. Your edit becomes the input
to the next stage.

```python
pipe.run_next()      # runs stage 02 using your (reviewed) research
pipe.status()        # [x] 01_research   [x] 02_explain
```

Read `stages/02_explain/output/output.md`: your finished explanation, built from
research you got to inspect first.

## Why this matters

- **You saw the middle.** If the explanation is off, you know whether the
  *research* or the *explaining* was at fault. Just open the files.
- **You could steer it.** Editing the intermediate file changed the outcome
  without touching any code.
- **It re-runs cleanly.** `pipe.reset()` clears the outputs so you can run again.

## Extensions

1. **Add a "factory" rule.** Drop a file in `explainer/references/voice.md`
   (e.g. *"Never use jargon; prefer everyday words."*). Re-run, and every stage now
   follows that rule. This is a *reference* (a rule), separate from the *input*
   (the data).
2. **Add a third stage** `03_quiz` that writes 3 quiz questions from the
   explanation. Just add the folder (`stages/03_quiz/CONTEXT.md`), no code
   changes needed.
3. **Fix the source, not the output.** If stage 2 keeps being too long, don't
   keep trimming its output. Edit `02_explain/CONTEXT.md` to say "100 words
   max." You just "fixed the compiler."
4. **Swap in an agent.** Make a stage that needs a calculation, and have a small
   script call [`run_agent`](../../agent-guide.md) instead of plain chat for that
   step.

## How it works under the hood

The `Pipeline` is deliberately tiny, about 100 lines. For each stage it builds a
prompt from: the stage's `CONTEXT.md`, any `references/` files (rules), and the
previous stage's `output.md` (input), then calls `get_response` and writes the
result. There's no hidden state: everything is a file you can read. Open
`hands_on_ai/workflow/runner.py` and see for yourself.
