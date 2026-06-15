# What Hands-On AI Is, and Isn't

Hands-On AI is a **learning lab**, not a production framework. Its goal is to help
you *understand* how modern AI systems work by building small, readable versions
of them yourself. That shapes every design choice, including the things it
deliberately leaves out.

## Small on purpose

You could read this entire package in an afternoon. That's the point.

Each module captures the **essence** of an idea (a [chat](chat-concepts.md)
reply, a [RAG](rag-llm-explain.md) answer, an [agent](agent-concepts.md) calling
a tool, a [workflow](workflow-guide.md) of folders) in a few dozen lines of
plain Python with no magic. The smallness isn't a limitation we're apologising
for; it's the feature. When the whole thing fits in your head, the *concept*
becomes visible instead of being buried under production machinery.

So we trade completeness for clarity, on purpose:

- **You'll find:** the core idea, written to be opened and read, runnable on a
  free local model, with no API keys or heavy setup.
- **You won't find:** retries and rate-limit handling, observability dashboards,
  streaming at scale, evaluation harnesses, vector databases, async pipelines, or
  the dozen other things real production systems need. Those aren't the lesson.

## It's all the same shape

Look closely and every module is identical underneath: one call to the model
(`get_response`), wrapped in plain Python. Chat adds a system prompt. RAG adds
code to fetch context. An agent adds a loop that runs your functions. A workflow
adds folders. The model is the only "AI" in the room; the rest is a thin harness
you can open and read. That's the whole package, and the whole point.

## Two friendly clarifications

**"Can I build my real product on top of this?"**
Please don't, and that's a compliment to your ambition, not a knock on the
package. Hands-On AI is the *on-ramp*, not the highway. Once the ideas here click,
you'll pick up a production-grade tool far faster *because* you understand what's
happening underneath. See [Going deeper](#going-deeper) for where to head next.

**"Isn't this too simple? It's missing X."**
Yes, and on purpose. Every gap is an invitation to go research further. If you
finish a module thinking *"but what about streaming / evaluation / bigger
context / a real vector store?"*, wonderful, that's the package working. It got
you to a good question. Now go chase it in the real libraries and papers.

We'd rather teach one idea so clearly that you outgrow us, than hand you a
framework you use without understanding.

## Going deeper

When you're ready to move from *understanding* to *shipping*, these are good next
stops (examples, not endorsements; the ecosystem moves fast, so treat this as a
map, not a manual):

- **Run models:** [Ollama](https://ollama.com), vLLM, LM Studio
- **Talk to providers directly:** the official OpenAI and Anthropic SDKs, or a
  thin multi-provider layer like LiteLLM
- **Build RAG for real:** LlamaIndex, and a vector database like Chroma, FAISS,
  Qdrant or pgvector
- **Structured output & agents:** Instructor or Pydantic AI for typed responses;
  LangChain / LangGraph, CrewAI, or a provider's agent SDK for orchestration
- **Go to the source:** read the original papers (ReAct, RAG, and the model cards
  for whatever you're using); they're more readable than you'd expect

## The spirit of it

Models change every few months; the *ideas* underneath them change slowly.
Hands-On AI bets on the ideas. If you leave understanding what a system prompt
really is, why an LLM is stateless, how retrieval grounds an answer, what a tool
call actually does, and why folders can orchestrate a workflow, then it did its
job, whatever you build next.

Welcome to the lab. Poke at things, break them, read the code. That's how it's
meant to be used. 🔬
