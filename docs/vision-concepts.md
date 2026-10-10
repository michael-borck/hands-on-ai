# Understanding Vision (Image Description)

So far every module in this toolkit has dealt with **text**: a
[chat](chat-concepts.md) reply, a [RAG](rag-llm-explain.md) answer, an
[agent](agent-concepts.md) reading tool output. The vision module asks a
different question: what happens when the *input* is an image instead?

## The one-sentence version

A **vision-language model (VLM)** turns an image into tokens -- the same kind
of input a chat model already reads -- so describing a picture is just another
prompt, answered with ordinary text.

## It's still the same shape

Here is the surprising part. You already know this pattern:

```python
from hands_on_ai.chat import get_response

get_response("What's in this photo?")        # text in, text out
```

Vision adds one kind of input, nothing else:

```python
from hands_on_ai.vision import describe

describe("photo.jpg", "What's in this photo?")   # image in, text out
```

Underneath, `describe` builds the same message list chat does, except the user
message carries the image *alongside* your question:

```python
[
    {"role": "system", "content": "You are a helpful assistant..."},
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this photo?"},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}},
        ],
    },
]
```

The image is base64-encoded into a long string (a **data URL**) and travels in
the same HTTP request as your text. The model splits the image into small
patches, encodes each patch as tokens, and reads them next to the words of
your prompt. From there it's the same next-token prediction as
[chat](chat-concepts.md). That's the whole idea: **one model, one more kind of
input**.

## Describing is not creating

Hands-On AI describes images; it does not generate them. The two directions
turn out to be very different problems:

- **Image → text** (this module): a VLM reads the image like a second language
  and answers with text. Small models (around 1--4 billion parameters) do this
  well enough to run on a laptop, which is why it fits here.
- **Text → image** (not this module): diffusion models denoise random pixels
  step by step. The good ones are large and slow, and the *idea* (diffusion) is
  a different lesson entirely.

If you finish this module wondering "but how do I *make* pictures?", that's
the gap doing its job -- go look up Stable Diffusion and diffusion models. For
describing, the small local models -- **moondream**, **LLaVA**,
**qwen2.5-vl** -- are the classroom sweet spot.

## What VLMs are (honestly) bad at

Keep these in mind when you read an answer:

- **Counting.** "How many people are in the photo?" is famously unreliable.
- **Small text.** Signs, labels, and handwriting are hit-and-miss.
- **Left/right and spatial precision.** Descriptions get the gist, not the
  geometry.
- **Confident nonsense.** Like any LLM, a VLM will sometimes *hallucinate*
  plausible-sounding details that aren't in the image at all. Small local
  models do this more than the big cloud ones.

The cure is the same as everywhere in this toolkit: ask precise questions,
look at the raw output, and don't trust a single answer.

## Where it fits

Vision is a side door off the main path -- chat, RAG, agent, workflow, loop,
eval -- not a stop on it. It's here because it is the smallest possible
demonstration of a big idea: **multimodality**. Models that read text, images,
and audio all reduce to the same trick: turn the input into tokens, then
predict. Voice (speech in, speech out) works the same way -- see
[Understanding Voice](voice-concepts.md) -- which is why real-world voice
agents like [Pipecat](https://github.com/pipecat-ai/pipecat) are "just"
pipelines around the same kind of model call.

Want to try it? The [vision guide](vision-guide.md) has setup, examples, and
the CLI.
