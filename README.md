# HandsOnAI: Your AI Learning Lab

<!-- BADGES:START -->
[![ai-education](https://img.shields.io/badge/-ai--education-blue?style=flat-square)](https://github.com/topics/ai-education) [![chatbots](https://img.shields.io/badge/-chatbots-blue?style=flat-square)](https://github.com/topics/chatbots) [![cli-tool](https://img.shields.io/badge/-cli--tool-blue?style=flat-square)](https://github.com/topics/cli-tool) [![natural-language-processing](https://img.shields.io/badge/-natural--language--processing-blue?style=flat-square)](https://github.com/topics/natural-language-processing) [![python](https://img.shields.io/badge/-python-3776ab?style=flat-square)](https://github.com/topics/python) [![react-framework](https://img.shields.io/badge/-react--framework-blue?style=flat-square)](https://github.com/topics/react-framework) [![retrieval-augmented-generation](https://img.shields.io/badge/-retrieval--augmented--generation-blue?style=flat-square)](https://github.com/topics/retrieval-augmented-generation) [![educational-toolkit](https://img.shields.io/badge/-educational--toolkit-blue?style=flat-square)](https://github.com/topics/educational-toolkit) [![edtech](https://img.shields.io/badge/-edtech-4caf50?style=flat-square)](https://github.com/topics/edtech) [![artificial-intelligence](https://img.shields.io/badge/-artificial--intelligence-blue?style=flat-square)](https://github.com/topics/artificial-intelligence)
<!-- BADGES:END -->

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/licence-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Classroom Ready](https://img.shields.io/badge/classroom-ready-brightgreen.svg)]()
[![Beginner Friendly](https://img.shields.io/badge/beginner-friendly-orange.svg)]()
[![DeepWiki](https://deepwiki.com/badge-maker?url=https%3A%2F%2Fdeepwiki.com%2Fmichael-borck%2Fhands-on-ai)](https://deepwiki.com/michael-borck/hands-on-ai)

> AI learning made simple for students and educators

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/michael-borck/hands-on-ai/blob/main/notebooks/quickstart.ipynb) **New here? Try the [quickstart notebook](notebooks/quickstart.ipynb) in your browser, no install needed.**

HandsOnAI is a unified educational toolkit designed to teach students how modern AI systems work, by building and interacting with them directly.

It provides a clean, modular structure that introduces core AI concepts progressively through five modules:

## 🧱 Module Overview

| Module | Purpose | CLI Name |
|--------|---------|----------|
| chat | Chatbot with system prompts, personalities, and memory | chat |
| rag | Retrieval-Augmented Generation (RAG) over your documents | rag |
| agent | Tool use and step-by-step reasoning | agent |
| workflow | Orchestrate multi-step tasks as folders of stages | (library) |
| eval | Evaluate output quality with an LLM judge | (library) |

(A small `models` utility module handles model detection and capabilities.)

Each module is:
- 🔌 Self-contained
- 🧩 Installable via one package: `pip install hands-on-ai`
- 🧠 Designed for progressive learning

## 🗂 Project Structure

```
hands_on_ai/
├── chat/           ← A simple prompt/response chatbot
├── rag/            ← Ask questions using your own documents
├── agent/          ← Agent reasoning + tools (ReAct-style)
├── config.py       ← Shared config (model, chunk size, paths)
├── cli.py          ← Meta CLI (list, config, version)
├── models.py       ← Centralized model utilities
├── utils/          ← Shared tools, prompts, paths, etc.
└── commands/       ← Shared CLI commands
```

Examples and scripts are available in the repository:

```
hands-on-ai/
├── examples/       ← Example scripts for all modules
└── scripts/        ← Utility scripts for package maintenance
```

## 🧑‍🏫 Why This Matters for Students

Each tool teaches a different level of modern AI interaction:

- **chat** – Prompt engineering, roles, and LLMs
- **rag** – Document search, embeddings, and grounded answers
- **agent** – Multi-step reasoning, tool use, and planning

## 🚀 Getting Started

### Installation

```bash
# Install from PyPI
pip install hands-on-ai

# Or directly from GitHub
pip install git+https://github.com/michael-borck/hands-on-ai.git
```

### Prerequisites

- Python 3.10 or higher
- Any OpenAI-compatible LLM provider (see [Provider Compatibility](#provider-compatibility))

### Quick Start

Prefer a notebook? Open the starter in Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/michael-borck/hands-on-ai/blob/main/notebooks/quickstart.ipynb)

#### Option 1: Set configuration in Python (Recommended for beginners)

```python
import os

# Configure your provider
os.environ['HANDS_ON_AI_SERVER'] = 'https://ollama.serveur.au'
os.environ['HANDS_ON_AI_MODEL'] = 'llama3.2'
os.environ['HANDS_ON_AI_API_KEY'] = input('Enter your API key: ')

# Now use HandsOnAI
from hands_on_ai.chat import pirate_bot
print(pirate_bot("What is photosynthesis?"))
```

#### Option 2: Use environment variables

Run a local Ollama server, then set environment variables and start chatting:

```bash
export HANDS_ON_AI_SERVER="http://localhost:11434"
# No API key needed for local Ollama
```

```python
from hands_on_ai.chat import pirate_bot
print(pirate_bot("What is photosynthesis?"))
```

For more options:

```python
from hands_on_ai.chat import get_response, friendly_bot, pirate_bot

# Basic usage with default model
response = get_response("Tell me about planets")
print(response)

# Use a personality bot
pirate_response = pirate_bot("Tell me about sailing ships")
print(pirate_response)
```

`get_response` is stateless: each call is independent. For a multi-turn chat
that remembers what was said, use `Conversation`:

```python
from hands_on_ai.chat import Conversation

chat = Conversation(system="You are a helpful tutor.")
chat.ask("My name is Sam.")
print(chat.ask("What's my name?"))   # -> remembers "Sam"

print(f"Tokens used so far: {chat.total_tokens}")

chat.save("chat.json")               # persist and resume later
later = Conversation.load("chat.json")
```

You can also see token usage for a single call with `get_response(..., return_usage=True)`,
which returns a `(response, usage)` tuple (or `chat ask "..." --usage` on the CLI).

Stream a response as it is generated:

```python
from hands_on_ai.chat import stream_response

for chunk in stream_response("Tell me a short story"):
    print(chunk, end="", flush=True)
```

Want reproducible, free reruns (great for classrooms)? Set `HANDS_ON_AI_CACHE` to
a directory and identical calls return a cached answer instead of calling the model.

## 🌍 Provider-Agnostic Architecture

HandsOnAI is designed to work with **any OpenAI-compatible LLM provider**. The system uses standard OpenAI API endpoints (`/v1/chat/completions`, `/v1/models`) making it compatible with a wide range of AI services.

### Configuration

Set your provider using environment variables:

```bash
# Set your provider's base URL
export HANDS_ON_AI_SERVER="https://your-provider-url"

# Set API key if required
export HANDS_ON_AI_API_KEY="your-api-key"

# Enable debug logging
export HANDS_ON_AI_LOG="debug"
```

### Provider Examples

#### Ollama (Local)
```bash
export HANDS_ON_AI_SERVER="http://localhost:11434"
# No API key needed for local Ollama
```

#### OpenAI
```bash
export HANDS_ON_AI_SERVER="https://api.openai.com"
export HANDS_ON_AI_API_KEY="sk-your-openai-key"
```

#### Together AI
```bash
export HANDS_ON_AI_SERVER="https://api.together.xyz"
export HANDS_ON_AI_API_KEY="your-together-key"
```

#### OpenRouter
```bash
export HANDS_ON_AI_SERVER="https://openrouter.ai/api"
export HANDS_ON_AI_API_KEY="your-openrouter-key"
export HANDS_ON_AI_MODEL="openai/gpt-4o"  # or any model they support
```

#### Google Gemini
```bash
export HANDS_ON_AI_SERVER="https://generativelanguage.googleapis.com/v1beta/openai"
export HANDS_ON_AI_API_KEY="your-gemini-key"
export HANDS_ON_AI_MODEL="gpt-4o-mini"  # maps to gemini-1.5-flash
```

#### Groq
```bash
export HANDS_ON_AI_SERVER="https://api.groq.com/openai"
export HANDS_ON_AI_API_KEY="your-groq-key"
```

#### LocalAI
```bash
export HANDS_ON_AI_SERVER="http://localhost:8080"
# API key optional depending on setup
```

## 📊 Provider Compatibility

HandsOnAI works with any service that implements OpenAI-compatible endpoints:

| **Provider** | **Base URL Example** | **Authentication** | **Status** |
|--------------|---------------------|-------------------|------------|
| **Ollama** | `http://localhost:11434` | None (local) | ✅ Tested |
| **OpenAI** | `https://api.openai.com` | Bearer token | ✅ Compatible |
| **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai` | Bearer token | ✅ Compatible |
| **Groq** | `https://api.groq.com/openai` | Bearer token | ✅ Compatible |
| **OpenRouter** | `https://openrouter.ai/api` | Bearer token | ✅ Compatible |
| **Together AI** | `https://api.together.xyz` | Bearer token | ✅ Compatible |
| **LocalAI** | `http://localhost:8080` | Optional | ✅ Compatible |
| **vLLM** | `http://your-vllm-server` | Optional | ✅ Compatible |
| **Hugging Face** | `https://api-inference.huggingface.co` | Bearer token | ✅ Compatible |
| **Any OpenAI-compatible server** | `http://your-server` | Varies | ✅ Compatible |

### Requirements for Compatibility

Your provider must support:
- ✅ `/v1/chat/completions` endpoint
- ✅ `/v1/models` endpoint  
- ✅ OpenAI message format (`{"role": "user", "content": "..."}`)
- ✅ Bearer token authentication (if API key required)

### Educational Benefits

This provider-agnostic approach offers several educational advantages:
- 🌍 **No vendor lock-in** - Switch providers without code changes
- 📚 **Industry standards** - Students learn OpenAI API patterns used across the industry
- 🔧 **Real-world skills** - Transferable knowledge to other AI tools and platforms
- 💡 **Flexibility** - Use local models for privacy or cloud models for power

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get involved.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤖 LLM Ready

This package is designed to work seamlessly with Large Language Models for coding assistance and learning:

### For Students & Educators
- **[LLM.txt](https://github.com/michael-borck/hands-on-ai/blob/main/LLM.txt)** - Complete reference guide for LLMs
- **[Documentation](https://michael-borck.github.io/hands-on-ai/)** - Full documentation site
- **[DeepWiki](https://deepwiki.com/michael-borck/hands-on-ai)** - Interactive code exploration and wiki

### How to Use with LLMs
1. **Download** the [LLM.txt file](https://github.com/michael-borck/hands-on-ai/blob/main/LLM.txt)
2. **Upload** it to your LLM (Claude, ChatGPT, etc.)
3. **Ask** for help with HandsOnAI projects - get complete, working code examples

Example prompts:
- *"Create a pirate chatbot using hands-on-ai"*
- *"Build a document Q&A system with the RAG module"*  
- *"Make an agent that can calculate and search the web"*

The LLM will have complete knowledge of the API, examples, and best practices.

## Acknowledgments

- Built with education in mind
- Powered by open-source LLM technology
- Inspired by educators who want to bring AI into the classroom responsibly