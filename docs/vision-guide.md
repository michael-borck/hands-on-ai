# Vision Guide

The vision module answers questions about images. One function, one CLI
command, no new dependencies -- it's the chat module with an image riding
along in the prompt.

Before you start, read [Understanding Vision](vision-concepts.md) for the idea
(an image becomes tokens; describing is not creating). This page is the
practical bits.

## Setup

Vision needs a *vision-language model* (VLM) rather than a plain chat model.
The default is `moondream`, a small (~2 GB) model that runs fine on a laptop.

For local Ollama:

```bash
ollama pull moondream
```

That's it -- the server URL and API key are shared with the rest of the
toolkit. To use a different model, set the environment variable:

```bash
export HANDS_ON_AI_VISION_MODEL=llava          # or qwen2.5-vl, minicpm-v, ...
```

Cloud providers work the same way (set `HANDS_ON_AI_SERVER` and
`HANDS_ON_AI_API_KEY` as usual):

| Provider | Vision model examples |
|----------|----------------------|
| Ollama (local) | `moondream`, `llava`, `qwen2.5-vl` |
| OpenAI | `gpt-4o-mini`, `gpt-4o` |
| Google Gemini | `gemini-2.0-flash` |
| Groq | `meta-llama/llama-4-scout-17b-16e-instruct` |

## Python API

```python
from hands_on_ai.vision import describe

# Describe an image with the default question
print(describe("photos/cat.jpg"))

# Ask a specific question
print(describe("photos/cat.jpg", "What breed is this cat?"))

# Point at an image on the web (local files and URLs both work)
print(describe("https://example.com/classroom.jpg", "How many students?"))

# Choose a specific model for one call
print(describe("map.png", "Which line goes to the airport?", model="qwen2.5-vl"))
```

The signature:

```python
describe(image, prompt="Describe this image.", model=None, retries=2)
```

- `image` is a path to a local file (`jpg`, `png`, `gif`, `webp`, `bmp`) or an
  http(s) URL. Local files are base64-encoded into the request automatically.
- The result is a string, in the same style as
  [`get_response`](chat-guide.md): the answer, or a `❌ Error: ...` message
  when something went wrong (missing file, no VLM on the server, and so on).

## CLI

```bash
vision photos/cat.jpg                                  # default description
vision photos/cat.jpg "What breed is this cat?"        # ask a question
vision https://example.com/map.png "Where is the library?"
vision --model llava photos/cat.jpg                    # model for one call
```

## Config reference

| Setting | Default | Purpose |
|---------|---------|---------|
| `HANDS_ON_AI_VISION_MODEL` | `moondream` | Which VLM to use for `describe` |

The server and API key come from `HANDS_ON_AI_SERVER` /
`HANDS_ON_AI_API_KEY`, shared with every other module.

## Troubleshooting

- **"model not found"**: the server doesn't have that VLM. For Ollama,
  `ollama pull moondream` first. Plain chat models (`llama3`, `gpt-3.5-turbo`)
  cannot see images -- check you set `HANDS_ON_AI_VISION_MODEL`, not
  `HANDS_ON_AI_MODEL`.
- **File not found / ❌ Error**: check the path; URLs must start with
  `http://` or `https://`.
- **Vague or wrong answers**: try a more specific prompt ("What colour is the
  front door?"), or a bigger VLM. See the
  [honest limitations](vision-concepts.md#what-vlms-are-honestly-bad-at) in
  the concepts page.

## Where to next

- [Understanding Vision](vision-concepts.md) -- how VLMs work, and what
  describing *isn't*.
- Once you're comfortable, the natural extension is combining vision with
  voice (speech in and out around the same model call). For production-grade
  real-time voice and video agents, graduate to
  [Pipecat](https://github.com/pipecat-ai/pipecat).
