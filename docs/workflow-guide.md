# Understanding Workflows (Folders over Frameworks)

So far you've built single steps: a [chat](chat-guide.md) reply, a [RAG](rag-guide.md)
answer, an [agent](agent-guide.md) that calls a tool. Real work is usually
*several* steps — research, then outline, then draft, then check. This guide is
about orchestrating those steps **without** a heavy framework.

## The problem with one giant prompt

The obvious way to do a multi-step task is to stuff everything into a single
enormous prompt: "research X, then outline it, then write 800 words, then…".
Two things go wrong:

- **The model loses focus.** Buried instructions get ignored (the "lost in the
  middle" effect). More context is not always better context.
- **You can't see or steer the middle.** If the final draft is wrong, you can't
  tell *which* step went wrong, and you can't fix the outline before it becomes
  a bad draft.

## The idea: folders *are* the architecture

The **Interpretable Context Methodology (ICM)** — "folders over frameworks" —
takes the Unix philosophy ("make each stage do one thing well") and applies it
to AI. Instead of orchestration code, a workflow is just a **folder of numbered
stages**:

```
workspace/
├── CONTEXT.md            # the overall goal / system prompt (optional)
├── references/           # stable rules — the "factory"
└── stages/
    ├── 01_research/
    │   ├── CONTEXT.md    # instructions for THIS stage
    │   └── output/       # output.md is written here
    └── 02_draft/
        ├── CONTEXT.md
        └── output/
```

One orchestrating model walks the stages in order. For each stage it reads that
stage's `CONTEXT.md` plus the **previous stage's output**, does the work, and
writes a new file. That's the whole mechanism.

Why this is nice for *learning* (and for real work):

- **It's a glass box.** Every intermediate result is a readable file you can open.
- **Anyone can change it.** Reorder steps by renaming folders; change a prompt by
  editing a markdown file. No code, no redeploy.
- **It's portable and durable.** The "logic" is just text and folders — it
  survives model upgrades and copies with `cp -r`.

> 💡 This is how the tools you already use work. Claude Code reads a `CLAUDE.md`,
> loads "skills" from folders, and delegates to sub-agents — the **filesystem is
> the coordination layer**. Learn this and you understand modern agentic tooling.

## Two ideas worth internalising

**1. Factory vs. Product.** Keep *rules* separate from *data*.

- `references/` (the **factory**) holds stable constraints — a voice guide, a
  rubric, domain facts. These are *rules to follow*, the same on every run.
- A stage's input (the **product**) is the specific material to transform — the
  previous step's output.

Separating them tells the model what to *obey* versus what to *work on*, and
keeps each step's context small and focused.

**2. Review gates: fix the source, not the output.** Because every step writes a
file, you can stop, read it, and edit it before the next step runs — your edit
becomes the new ground truth. If a step is *consistently* wrong, don't keep
hand-fixing its output ("patching the binary"). Edit the stage's `CONTEXT.md` or
a reference file ("fixing the source") so it's right on every future run.

In practice, human attention follows a **U-shape**: heavy at the start (setting
direction), light in the middle (the model follows the rules), and heavy again
at the end (final alignment).

## Doing it in Hands-On AI

Hands-On AI ships a tiny runner — the `Pipeline` — that does exactly this. It is
deliberately **sequential and human-in-the-loop**: `run_next()` runs *one* stage
and stops, so you review the file before continuing.

```python
from hands_on_ai.workflow import Pipeline, init_workspace

# Create a starter workspace with two stages
init_workspace("essay", ["research", "draft"], system="You are a writing assistant.")
# ...edit stages/01_research/CONTEXT.md and stages/02_draft/CONTEXT.md...

pipe = Pipeline("essay")
pipe.status()        # [ ] 01_research   [ ] 02_draft
pipe.run_next()      # runs 01, writes stages/01_research/output/output.md, stops
# open that file, read it, edit if needed...
pipe.run_next()      # runs 02 using your (possibly edited) research
```

`run_all()` exists for when you trust a pipeline, but `run_next()` — run, review,
continue — is the point.

The [Build a Pipeline](projects/workflow/build-a-pipeline.md) project walks
through this end to end.

## When to use what

ICM is one tool, not the only one. Be honest about the fit:

| Use | Reach for |
|-----|-----------|
| Sequential, reviewable steps (research → draft → polish) | **A workflow (this)** |
| One question, maybe one tool call | [An agent](agent-guide.md) |
| Thousands of concurrent users, millisecond agent-to-agent messaging | A real framework (LangChain, etc.) |

Workflows are **sequential and human-in-the-loop by design**. Need parallelism?
Run separate workflows yourself and decide how to combine them — a deliberate
human choice, not a hidden autonomous loop.

For more on where this little runner fits next to production frameworks (and when
to reach for one), see [What this is (and isn't)](philosophy.md).

> The honest summary: models are ephemeral, but **context and structure are
> durable**. Organising the information well often matters more than the
> orchestration code you didn't have to write.
