# Install & First Run

This page gets you from nothing to a working AI response in a few minutes.

## 1. Requirements

- **Python 3.10 or newer**
- A connection to an LLM provider. The simplest is **local [Ollama](ollama-guide.md)**
  (free, no API key), but any [OpenAI-compatible provider](providers.md) works.

## 2. Install the package

```bash
pip install hands-on-ai
```

Or install the latest from GitHub:

```bash
pip install git+https://github.com/teaching-repositories/hands-on-ai.git
```

The RAG module can read PDFs and Word documents. If you plan to use those,
install the optional extras:

```bash
pip install "hands-on-ai[rag]"
```

## 3. Connect a provider

The quickest path is local Ollama (no API key):

```bash
# Install Ollama from https://ollama.com, then pull a model:
ollama pull llama3
```

Ollama runs at `http://localhost:11434` and Hands-On AI connects to it
automatically, with no configuration needed.

Using OpenAI, OpenRouter, Groq, an authenticated Ollama server, or anything else?
See [Choose a Provider](providers.md).

## 4. Run your first bot

```python
from hands_on_ai.chat import get_response

print(get_response("Explain photosynthesis like I'm 10."))
```

You should see a real response from the model. Try a personality bot:

```python
from hands_on_ai.chat import pirate_bot

print(pirate_bot("Tell me about sailing ships."))
```

## 5. Verify your setup

Hands-On AI ships a diagnostic command that checks your connection, shows the
resolved configuration, and lists available models:

```bash
handsonai doctor
```

If something isn't connecting, this is the fastest way to see why (wrong server
URL, missing API key, model not pulled, etc.).

## Next steps

- [Choose a Provider](providers.md): Ollama, cloud providers, or an authenticated server
- [Configuration](configuration.md): environment variables and the config file
- [Browse the projects](projects/index.md): build something with what you've installed
