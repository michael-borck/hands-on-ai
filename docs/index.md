# Learn how modern AI actually works — by building it

**Hands-On AI** is an educational toolkit for *understanding* AI, not just using it.
You build the things you hear about — a chatbot, a retrieval system, a
tool-using agent — in small, readable Python, and run them on free local models.

It's designed for the classroom: no API keys required, works offline, and one
install (`pip install hands-on-ai`) gives you three progressively deeper modules.

## Start in 3 steps

```bash
# 1. Install
pip install hands-on-ai

# 2. Connect a provider (easiest: local Ollama — no API key)
ollama pull llama3
```

```python
# 3. Run your first bot
from hands_on_ai.chat import get_response
print(get_response("Explain photosynthesis like I'm 10."))
```

New here? Follow the [Install & First Run](installation.md) guide, then
[Choose a Provider](providers.md).

## Where to go next

<div class="grid cards" markdown>

-   🎓 **I'm a Student / Learner**

    ---

    Start with the [Bot Gallery](bot-gallery.md), then learn the ideas behind
    [Chat](chat-guide.md), [RAG](rag-guide.md), and [Agents](agent-guide.md) —
    and build your own in the [Projects](mini-projects.md).

    [Browse the projects →](projects/index.md)

-   🧑‍🏫 **I'm an Educator**

    ---

    See how to run Hands-On AI in class — setup, provider choices, and ready-made
    assignments with learning objectives and assessment ideas.

    [Education Guide →](education-guide.md) · [Classroom Setup →](classroom-setup.md)

-   🛠️ **I'm a Developer**

    ---

    Wire up any OpenAI-compatible provider, explore the CLI, extend agents with
    your own tools, or contribute back.

    [CLI Reference →](cli-guide.md) · [Build Your Own Tool →](projects/agent/build-your-own-tool.md)

</div>

## The three modules

Each module introduces the next layer of how modern AI systems are built:

<div class="grid cards" markdown>

-   💬 **Chat** — `chat`

    ---

    Prompting, system prompts, personalities, and multi-turn conversation.
    The foundation: talking to an LLM.

    [Learn Chat →](chat-guide.md)

-   📚 **RAG** — `rag`

    ---

    Retrieval-Augmented Generation: chunk your documents, embed them, and ground
    the model's answers in your own sources.

    [Learn RAG →](rag-guide.md)

-   🤖 **Agent** — `agent`

    ---

    Tool use and step-by-step reasoning. The model decides *which tool to call*
    to solve a problem.

    [Learn Agents →](agent-guide.md)

</div>

## Why Hands-On AI

- 🔑 **No API keys required** — runs on free local models via [Ollama](ollama-guide.md)
- 🌍 **Provider-agnostic** — swap to OpenAI, OpenRouter, Together, Groq, or any [OpenAI-compatible provider](providers.md) without changing code
- 📴 **Works offline** — ideal for classrooms with unreliable internet
- 🧠 **Beginner-friendly** — small, readable code you're meant to open and understand
- 🧩 **Progressive** — chat → RAG → agents mirrors a real learning path

## Offline resources

- **[Project Browser](project_browser.html)** — a standalone HTML file to browse
  and filter every project offline. Great for classrooms without reliable internet.
