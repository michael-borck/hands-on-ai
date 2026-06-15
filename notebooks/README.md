# Notebooks

Runnable notebooks for Hands-On AI.

## Quickstart

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/michael-borck/hands-on-ai/blob/main/notebooks/quickstart.ipynb)

[`quickstart.ipynb`](quickstart.ipynb) is a short tour: install, connect to a
model, then chat, personality bots, `Conversation` memory, a tool-using agent,
and a two-stage workflow.

**On Colab or another hosted notebook,** run the setup cell to point at a
provider you can reach over the internet (for example, an Ollama server with a
bearer key hosted by your educator). **Running locally** with Ollama? Skip that
cell and it connects to `http://localhost:11434` automatically.

## RAG (Retrieval-Augmented Generation)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/michael-borck/hands-on-ai/blob/main/notebooks/rag.ipynb)

[`rag.ipynb`](rag.ipynb) goes deeper on the `rag` module: it builds a search
index over a few documents, retrieves the most relevant chunks for a question,
and grounds the model's answer in them. It also needs an embedding model (for
local Ollama, `ollama pull nomic-embed-text`).

See the [Notebooks & Colab guide](https://michael-borck.github.io/hands-on-ai/notebooks/)
for details.
