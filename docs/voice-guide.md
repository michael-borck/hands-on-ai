# Voice Guide

The voice module adds ears and a mouth to the toolkit: `transcribe` turns
audio into text, `speak` turns text into audio, and `voice chat` loops them
around the chat model. Read [Understanding Voice](voice-concepts.md) for the
idea; this page is the practical bits.

## Setup

Voice needs an **audio-capable OpenAI-compatible server** -- this is the one
part where plain Ollama isn't enough (it serves text models only). Any server
implementing `/v1/audio/transcriptions` and `/v1/audio/speech` works:

| Need | Local options | Cloud options |
|------|---------------|---------------|
| STT | [speaches](https://github.com/speaches-ai/speaches) (Whisper), [whisper.cpp server](https://github.com/ggml-org/whisper.cpp) | Groq (`whisper-large-v3`), OpenAI (`whisper-1`) |
| TTS | [speaches](https://github.com/speaches-ai/speaches) (Kokoro), [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI), LocalAI (Piper) | OpenAI (`tts-1`) |

The quickest local setup is one Docker container serving both directions
(educators: see [Host an Audio Server](deploy-audio-server.md) for the
classroom recipe):

```bash
docker run --gpus all -p 8000:8000 speaches-ai/speaches:latest-cuda
# or CPU-only: docker run -p 8000:8000 speaches-ai/speaches:latest-cpu
```

Then point the toolkit at it (independent of your chat server):

```bash
export HANDS_ON_AI_STT_SERVER=http://localhost:8000
export HANDS_ON_AI_TTS_SERVER=http://localhost:8000
```

Defaults if you don't set them: STT model `whisper-1`, TTS model `kokoro`,
both on your main `HANDS_ON_AI_SERVER`.

## Python API

```python
from hands_on_ai.voice import speak, transcribe

# Ears: audio file in, text out
text = transcribe("question.wav")
text = transcribe("question.wav", language="en")     # language hint

# Mouth: text in, audio file out
path = speak("Hello class")                          # writes speech.wav
path = speak("Hello class", voice="alloy", out_path="greeting.wav")

# The whole voice agent in three lines
from hands_on_ai.chat import Conversation
conversation = Conversation()
speak(conversation.ask(transcribe("question.wav")))
```

The signatures:

```python
transcribe(audio_path, model=None, language=None, retries=2, timeout=120)
speak(text, voice="alloy", out_path=None, model=None, retries=2, timeout=120)
```

- `transcribe` returns the words as a string; `speak` returns the `Path` of
  the written WAV file. Errors come back as `"❌ Error: ..."` strings in the
  usual toolkit style (check for the emoji if it matters).
- `out_path` defaults to `speech.wav` in the current directory -- handy for
  loops, which just overwrite it each turn.

## CLI

```bash
voice transcribe lecture.wav                     # speech -> text
voice transcribe lecture.wav --language en       # with a language hint
voice speak "Well done, class."                  # text -> speech.wav
voice speak "Listen up." --play                  # ...and play it
voice speak "One at a time." -o turn1.wav        # choose the output file
voice chat                                       # type a question, hear the answer
```

`voice chat` is the smallest voice agent: you type (the mic comes later),
the chat model thinks, the TTS model speaks, and your computer plays it.
Quit with `q`, Ctrl-C, or Ctrl-D.

## Config reference

| Setting | Default | Purpose |
|---------|---------|---------|
| `HANDS_ON_AI_STT_SERVER` | main server | Where `/v1/audio/transcriptions` lives |
| `HANDS_ON_AI_STT_MODEL` | `whisper-1` | Which STT model to request |
| `HANDS_ON_AI_TTS_SERVER` | main server | Where `/v1/audio/speech` lives |
| `HANDS_ON_AI_TTS_MODEL` | `kokoro` | Which TTS model to request |

## Troubleshooting

- **Connection error from `speak`/`transcribe`**: your server doesn't serve
  audio (plain Ollama doesn't). Point `HANDS_ON_AI_STT_SERVER` /
  `HANDS_ON_AI_TTS_SERVER` at an audio server -- see Setup above.
- **Nothing plays**: generate first, play second (`afplay speech.wav` on
  macOS, `aplay speech.wav` on Linux), and check your output device.
- **Wrong words transcribed**: add `--language`, record closer to the mic,
  or try a larger STT model on the server.
- **Slow first response**: local models load on first use; later calls are
  much faster.

## Where to next

- [Understanding Voice](voice-concepts.md) -- why turn-taking and barge-in
  are the real problems, and what VAD is.
- The capstone: [Build the world's smallest Pipecat](projects/voice/build-the-worlds-smallest-pipecat.md)
  -- add a microphone, hit the hard problems yourself, then see how
  [Pipecat](https://github.com/pipecat-ai/pipecat) solves them for real.
