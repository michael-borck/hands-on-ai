# Choose a Provider

Hands-On AI talks to LLMs through the **standard OpenAI-compatible API**
(`/v1/chat/completions`, `/v1/models`). That means the same code works with many
providers — you only change a couple of environment variables.

This page covers the three setups people ask about most:

1. [Local Ollama (no key)](#1-local-ollama-no-api-key)
2. [Ollama (or any server) behind an API key](#2-ollama-behind-an-api-key)
3. [A cloud OpenAI-compatible provider](#3-a-cloud-openai-compatible-provider)

The two settings that do all the work:

| Variable | What it is |
|----------|-----------|
| `HANDS_ON_AI_SERVER` | Base URL of your provider |
| `HANDS_ON_AI_API_KEY` | Bearer token (omit for local Ollama) |
| `HANDS_ON_AI_MODEL` | Model name to use |

See [Configuration](configuration.md) for the full list and the config-file option.

---

## 1. Local Ollama (no API key)

The default and simplest setup — free, private, offline.

```bash
ollama pull llama3
```

Nothing to configure: Hands-On AI connects to `http://localhost:11434`
automatically. Full walkthrough in the [Ollama Setup guide](ollama-guide.md).

---

## 2. Ollama behind an API key

If you run Ollama on a shared/remote host (e.g. a classroom server behind an
auth proxy), point at it and supply a bearer token:

```bash
export HANDS_ON_AI_SERVER="https://ollama.your-school.edu"
export HANDS_ON_AI_API_KEY="your-classroom-key"
export HANDS_ON_AI_MODEL="llama3"
```

The key is sent as a standard `Authorization: Bearer …` header.

---

## 3. A cloud OpenAI-compatible provider

Set the server URL and your key. A few examples:

=== "OpenAI"

    ```bash
    export HANDS_ON_AI_SERVER="https://api.openai.com"
    export HANDS_ON_AI_API_KEY="sk-your-openai-key"
    export HANDS_ON_AI_MODEL="gpt-4o-mini"
    ```

=== "OpenRouter"

    ```bash
    export HANDS_ON_AI_SERVER="https://openrouter.ai/api"
    export HANDS_ON_AI_API_KEY="your-openrouter-key"
    export HANDS_ON_AI_MODEL="openai/gpt-4o"
    ```

=== "Groq"

    ```bash
    export HANDS_ON_AI_SERVER="https://api.groq.com/openai"
    export HANDS_ON_AI_API_KEY="your-groq-key"
    ```

=== "Together AI"

    ```bash
    export HANDS_ON_AI_SERVER="https://api.together.xyz"
    export HANDS_ON_AI_API_KEY="your-together-key"
    ```

=== "Google Gemini"

    ```bash
    export HANDS_ON_AI_SERVER="https://generativelanguage.googleapis.com/v1beta/openai"
    export HANDS_ON_AI_API_KEY="your-gemini-key"
    export HANDS_ON_AI_MODEL="gpt-4o-mini"  # maps to a Gemini model
    ```

> 💡 **Beginner tip:** you can also set these in Python before importing, which
> is handy in notebooks:
>
> ```python
> import os
> os.environ["HANDS_ON_AI_SERVER"] = "https://api.openai.com"
> os.environ["HANDS_ON_AI_API_KEY"] = input("Enter your API key: ")
> ```

---

## Provider compatibility

Hands-On AI works with any service that implements the OpenAI-compatible
endpoints below.

| Provider | Base URL example | Auth |
|----------|------------------|------|
| **Ollama** | `http://localhost:11434` | None (local) |
| **OpenAI** | `https://api.openai.com` | Bearer token |
| **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai` | Bearer token |
| **Groq** | `https://api.groq.com/openai` | Bearer token |
| **OpenRouter** | `https://openrouter.ai/api` | Bearer token |
| **Together AI** | `https://api.together.xyz` | Bearer token |
| **LocalAI** | `http://localhost:8080` | Optional |
| **vLLM** | `http://your-vllm-server` | Optional |
| **Hugging Face** | `https://api-inference.huggingface.co` | Bearer token |
| **Any OpenAI-compatible server** | `http://your-server` | Varies |

**Your provider must support:**

- `/v1/chat/completions` and `/v1/models` endpoints
- OpenAI message format (`{"role": "user", "content": "..."}`)
- Bearer token authentication (if a key is required)

---

## Verify it works

```bash
handsonai doctor
```

This checks the connection, shows the resolved configuration, and lists models
the provider reports — the quickest way to confirm your provider is wired up.
