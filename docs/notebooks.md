# Using Notebooks (Jupyter & Colab)

Hands-On AI is just Python, so it works anywhere Python does, notebooks included.
There's only one thing to think about: **where the model runs.**

```python
!pip install hands-on-ai

from hands_on_ai.chat import get_response
print(get_response("Explain photosynthesis like I'm 10."))
```

## Local notebooks (Jupyter, JupyterLab, VS Code)

If the notebook runs on **your own machine**, local [Ollama](ollama-guide.md)
works out of the box: it listens on `http://localhost:11434` and Hands-On AI
connects automatically, no configuration needed. You can also point at a remote
provider if you prefer (see [Choose a Provider](providers.md)).

## Google Colab and other hosted notebooks

The catch with Colab (or any hosted notebook) is that the code runs on a remote
server, **not your laptop**, so it cannot reach an Ollama running on your own
`localhost`. You need a provider the notebook can reach over the internet.

The recommended classroom setup is an **Ollama server with a bearer key**, hosted
by the educator, so a whole class can share it without anyone needing a paid API
key. Put this in the first cell:

```python
!pip install -q hands-on-ai

import os, getpass
os.environ["HANDS_ON_AI_SERVER"] = "https://ollama.your-school.edu"
os.environ["HANDS_ON_AI_API_KEY"] = getpass.getpass("Class API key: ")
os.environ["HANDS_ON_AI_MODEL"] = "llama3"

from hands_on_ai.chat import get_response
print(get_response("Hello from Colab!"))
```

A few notes:

- Set the environment variables **before your first `get_response` call**. A
  config cell at the top of the notebook is the simplest place.
- Use `getpass.getpass(...)` for the API key rather than `input(...)`, so the key
  stays out of the saved notebook and its output.
- Any OpenAI-compatible provider works the same way (OpenAI, Groq, OpenRouter,
  and so on). Just swap the server URL, key, and model. See
  [Choose a Provider](providers.md).
- For the RAG module's PDF/Word support, install the extras:
  `!pip install -q "hands-on-ai[rag]"`.

## For educators

Hosting one Ollama server with a bearer key is usually the smoothest classroom
path: students only paste a URL and a key, and no one needs their own cloud
account. The [Choose a Provider](providers.md) and
[Classroom Setup](classroom-setup.md) guides cover the details.
