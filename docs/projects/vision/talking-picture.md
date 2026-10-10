# The Talking Picture

**Difficulty**: Beginner  
**Time**: 45 minutes  
**Learning Focus**: Vision-language models, multimodal pipelines, accessibility  
**Module**: vision (with a little voice)

## Overview

You'll build a "talking picture": give the program an image and it *describes
the image out loud*. Along the way you'll generate alt-text for a whole folder
of images -- the same technique used to make the web accessible to screen
readers.

> 🧠 **Vision in one line:** a vision-language model turns an image into
> tokens, so describing a picture is just another prompt. See
> [Understanding Vision](../../vision-concepts.md) for the concepts.

## What you need

- A vision-language model on your server. For local Ollama:
  `ollama pull moondream` (small) or use `gemma3:4b` if you have it
  (`export HANDS_ON_AI_VISION_MODEL=gemma3:4b`)
- Any voice setup from the [Voice Guide](../../voice-guide.md) for the
  speaking steps (skip them if you don't have an audio server yet)
- A few images: photos you have, or grab a couple from the web (URLs work)

## Step 1: Describe one picture

One call. Notice this is the [chat](../../chat-guide.md) shape with an image
riding along:

```python
from hands_on_ai.vision import describe

print(describe("photo.jpg"))
```

Try the same image with a specific question:

```python
print(describe("photo.jpg", "What is the mood of this photo?"))
```

## Step 2: Quiz the picture

Ask three questions and print question and answer together. Good questions
test what VLMs are *good* at (objects, scenes, text on signs) and what they're
*bad* at (counting, precise positions) -- try at least one of each and see:

```python
questions = [
    "What objects can you see?",
    "How many people are in the image?",      # famously unreliable!
    "What text appears in the image, if any?",
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {describe('photo.jpg', q)}\n")
```

## Step 3: Give the picture a voice

Now the image talks. `speak` writes a WAV file your OS can play
(`afplay` on macOS, `aplay` on Linux):

```python
from hands_on_ai.voice import speak

description = describe("photo.jpg")
print(description)
speak(description, out_path="description.wav")
```

Play `description.wav`. You've built a multimodal pipeline: **image -> text ->
speech** -- three plain function calls, no framework.

## Step 4: A folder of pictures

Point it at a folder and describe everything in it:

```python
from pathlib import Path

folder = Path("pictures")          # make this folder, drop in a few images
for image in sorted(folder.glob("*.jpg")):
    print(f"\n{image.name}:")
    print(describe(str(image), "Describe this image in one sentence."))
```

## Step 5: Alt-text generator (the useful version)

Alt-text is the short description screen readers announce for images. Generate
it for every image in a folder and collect the results in a markdown file,
ready to paste into a website:

```python
from hands_on_ai.vision import describe
from pathlib import Path

lines = ["# Alt-text for my images\n"]
for image in sorted(Path("pictures").glob("*")):
    if image.suffix.lower() not in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        continue
    alt = describe(str(image), "Write one sentence of alt-text for this image. "
                               "Describe what is visually there, no preamble.")
    lines.append(f"**{image.name}**: {alt}\n")

Path("alt-text.md").write_text("\n".join(lines))
print("Wrote alt-text.md")
```

Open `alt-text.md` and judge each line: would a screen-reader user get the
point from it? Good alt-text is specific and short; VLMs are usually verbose.
That gap is your editorial job.

## Extensions

Pick any of these:

- **Follow-up questions.** Wrap the image in a real conversation: describe the
  image with `Conversation`, then ask follow-ups that reference earlier
  answers. (Hint: pass the image in the first user message yourself, or
  describe first and feed the description into `Conversation`.)
- **Two models, one picture.** Run `describe(..., model="llava")` and
  `describe(..., model="moondream")` on the same image and compare. Which
  hallucinates less? Which is faster?
- **Other languages.** `describe(img, "Décris cette image en français.")`,
  then speak the result -- instant listening-comprehension practice for a
  language class.
- **The full tour.** Combine with the voice module's loop from
  [Build the World's Smallest Pipecat](../voice/build-the-worlds-smallest-pipecat.md):
  say which photo to describe, hear the answer.

> 💡 A type-hints exercise works as an extension for almost any project: the
> example code is kept plain on purpose (see [Mini-Projects Overview](../../mini-projects.md#a-note-on-type-hints)),
> so adding annotations and running `mypy`/`pyright` is a great next step for
> students ready for industry best practice.

## How it works under the hood

`describe` is about 50 lines of plain Python in
[`hands_on_ai/vision/describe.py`](https://github.com/michael-borck/hands-on-ai/blob/main/src/hands_on_ai/vision/describe.py):
local files are base64-encoded into a `data:` URL, dropped into the user
message next to your question, and sent through the usual chat completion
call. `speak` is one HTTP call to `/v1/audio/speech`. No magic -- the
"multimodal" part is just a second kind of input riding in a message you
already understand.
