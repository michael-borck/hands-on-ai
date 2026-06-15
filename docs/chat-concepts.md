# Understanding Chat & Bots

This is the starting point for the whole toolkit: talking to a large language
model (LLM) and shaping *how* it talks back. Once you understand this, RAG,
agents, and workflows are all variations on the same idea.

## What a chat model actually does

An LLM is, at heart, a very good *next-text predictor*. You give it some text (a
**prompt**), and it continues it with the most plausible response. There's no
database lookup and no "understanding" in the human sense — just a model trained
on a huge amount of text producing a likely continuation.

In Hands-On AI, one function does this:

```python
from hands_on_ai.chat import get_response

print(get_response("Explain gravity in one sentence."))
```

## The two messages: system and user

Every request sends the model **two** messages:

- a **user** message — your actual question or instruction, and
- a **system** message — a behind-the-scenes instruction that sets the model's
  role, tone, and rules.

The system prompt is the single most powerful lever you have:

```python
get_response(
    "Explain gravity.",
    system="You are a pirate. Answer in pirate slang.",
)
```

Same question, completely different answer — because the system prompt changed
*who the model is being*.

## So what is a "bot"?

In this toolkit a **bot** is nothing magical: it's just a small function that
calls `get_response` with a fixed system prompt baked in.

```python
def pirate_bot(prompt):
    return get_response(prompt, system="You are a pirate. Answer in pirate slang.")
```

That's the whole trick. The library ships a collection of these ready-made — the
[Personality Gallery](bot-gallery.md) — and a bot's "personality" is *entirely*
its system prompt. Change the prompt, change the personality. The
[Personality Bot Creator](projects/chat/personality-bot-creator.md) project has
you build your own.

## Prompting: getting better answers

Because the model just continues your text, *how you ask* matters a lot:

- **Be specific.** "Summarise this in 3 bullet points for a 12-year-old" beats
  "summarise this."
- **Give context.** Paste the material the model needs; it only knows what's in
  the prompt (plus its training).
- **Show an example.** Demonstrating the format you want ("Q: … A: …") steers the
  output more reliably than describing it.

This is the foundation of *prompt engineering* — and it's why the next module,
[RAG](rag-guide.md), exists: to put the *right* context into the prompt
automatically.

## The one surprise: the model has no memory

Each `get_response` call is **completely independent**. The model does not
remember your previous question — it only ever sees the system prompt and the one
prompt you send *this* call.

```python
get_response("My name is Sam.")
get_response("What's my name?")   # it has no idea — these are unrelated calls
```

To make a bot that *remembers*, you keep the conversation yourself and resend it
each turn. That's exactly what `Conversation` does for you:

```python
from hands_on_ai.chat import Conversation

chat = Conversation(system="You are a helpful tutor.")
chat.ask("My name is Sam.")
print(chat.ask("What's my name?"))   # → remembers "Sam"
```

Understanding that an LLM is *stateless* — and that "memory" just means resending
the transcript — is one of the most important ideas in the whole toolkit.

## Where to go next

- [Chat CLI Guide](chat-guide.md) — drive the chat module from the command line
- [Personality Gallery](bot-gallery.md) — the ready-made bots, and what makes each tick
- [Chat projects](projects/index.md) — build something: a tutor, a quiz bot, an adventure game
- Then layer on [RAG](rag-guide.md), [Agents](agent-guide.md), and [Workflows](workflow-guide.md)
