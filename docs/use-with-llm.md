# Teaching an AI about Hands-On AI

You can get an AI assistant (Claude, ChatGPT, and others) to write correct
Hands-On AI code for you. There are two easy ways.

## Option 1: Paste `LLM.txt` into the chat

[`LLM.txt`](https://github.com/michael-borck/hands-on-ai/blob/main/LLM.txt) is a
single-file reference for the whole package: the four modules, the real function
signatures, and worked examples. Drop it into the assistant's context window and
it can answer questions and generate working code that uses the current API
instead of guessing from older training data.

1. Open `LLM.txt`
   ([view](https://github.com/michael-borck/hands-on-ai/blob/main/LLM.txt) or
   [raw](https://raw.githubusercontent.com/michael-borck/hands-on-ai/main/LLM.txt)).
2. Copy its contents, or upload the file, into your AI chat.
3. Ask away. For example:
   - "Using hands-on-ai, write a pirate chatbot."
   - "Build a document Q&A script with the RAG module."
   - "Make an agent with a calculator tool."
   - "Show me a two-stage workflow that researches a topic, then drafts a summary."

> **Tip:** `LLM.txt` is kept in sync with the package by hand, and it lists the
> version it describes at the top. If you are on a different version, grab the
> `LLM.txt` that matches your install.

## Option 2: Chat with the repo on DeepWiki

[DeepWiki](https://deepwiki.com/michael-borck/hands-on-ai) builds an AI-powered
wiki and chat interface over the whole repository. Instead of browsing the code
on [GitHub](https://github.com/michael-borck/hands-on-ai), you can ask DeepWiki
how something works and it answers with references back to the source.

It is a good way to explore the internals (for example, "how does the agent loop
parse tool calls?") without reading every file yourself.

## Which one to use

- **Writing code *with* the package?** Paste `LLM.txt` into your assistant (Option 1).
- **Understanding how the package works *inside*?** Ask DeepWiki (Option 2).

Both are read-only helpers for learning and building. The package itself does not
send your code anywhere.
