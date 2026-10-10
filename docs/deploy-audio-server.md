# Host an Audio Server (for Educators)

The [voice module](voice-guide.md) needs an OpenAI-compatible **audio**
server -- something serving `/v1/audio/transcriptions` (speech-to-text) and
`/v1/audio/speech` (text-to-speech). Plain Ollama serves text models only, so
voice needs one extra piece of infrastructure. This page is the educator
recipe, in the same spirit as [Host a Shared Ollama](deploy-ollama.md): you
run the server once, students set two environment variables.

If every student can install Docker (or you have one lab machine), this is a
ten-minute setup. If you'd rather skip self-hosting entirely, the cloud
options at the bottom work with nothing but an API key.

## The shape

One container -- [speaches](https://github.com/speaches-ai/speaches) -- serves
both directions of voice with OpenAI-compatible endpoints:

- **STT**: faster-whisper (the same Whisper models, faster)
- **TTS**: Kokoro (small, surprisingly good voices)

Students point `HANDS_ON_AI_STT_SERVER` and `HANDS_ON_AI_TTS_SERVER` at it.
Everything else (chat, RAG, agent, vision) keeps using your existing
`HANDS_ON_AI_SERVER`.

## Quick start (one machine, one class)

On a machine the classroom network can reach (your laptop, the lab server):

```bash
docker run -d --name audio -p 8000:8000 speaches-ai/speaches:latest-cpu
# With an NVIDIA GPU, for faster transcription:
# docker run -d --name audio --gpus all -p 8000:8000 speaches-ai/speaches:latest-cuda
```

Then check which model names the server actually exposes (they vary between
versions):

```bash
curl http://localhost:8000/v1/models
```

Tell students those two model names (see below). If you use the speaches
defaults, the toolkit's defaults (`whisper-1`, `kokoro`) usually just work.

## What students do

Two more environment variables alongside their usual setup:

```bash
export HANDS_ON_AI_STT_SERVER="http://YOUR-LAB-MACHINE:8000"
export HANDS_ON_AI_TTS_SERVER="http://YOUR-LAB-MACHINE:8000"
# Only if the server's model names differ from the defaults:
# export HANDS_ON_AI_STT_MODEL="whisper-1"
# export HANDS_ON_AI_TTS_MODEL="kokoro"
```

Then a thirty-second smoke test:

```bash
voice speak "Can everyone hear me?" --play
voice transcribe some-recording.wav
```

No Docker, no install, no model downloads on the student side.

## docker-compose (persisted, always on)

For a server that survives reboots:

```yaml
services:
  audio:
    image: speaches-ai/speaches:latest-cpu   # or latest-cuda on GPU machines
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - audio_models:/home/user/.cache/huggingface

volumes:
  audio_models:
```

The named volume keeps downloaded models across container updates, so
restarts are quick after the first run.

## Honest notes before class

- **First request is slow.** The server downloads and loads each model on
  first use (a minute or more on CPU). Warm the server up *before* students
  arrive: run one `voice speak` and one `voice transcribe` yourself.
- **CPU is fine for a class.** Whisper on CPU transcribes faster than
  real-time for short clips; GPU is only worth it for long recordings or
  large models.
- **This is a LAN service by default.** The container listens on port 8000
  with no authentication -- same as Ollama. Keep it on the classroom network.
  If you must expose it publicly, put the same Caddy bearer-token proxy in
  front of it described in [Host a Shared Ollama](deploy-ollama.md).
- **Microphones are a separate problem.** The toolkit's CLI works on audio
  *files*; students can record with their OS tools (or the
  "world's smallest Pipecat" project, which adds mic capture as the lesson).
- **Prefer zero infrastructure?** The same code works against the cloud: set
  the STT/TTS servers to `https://api.openai.com` (models `whisper-1`,
  `tts-1`) or Groq for fast transcription, with `HANDS_ON_AI_API_KEY` as
  usual. You trade the API key for the server.

## Where this fits

The audio server is infrastructure, not a lesson. The lesson is
[Understanding Voice](voice-concepts.md): listen, think, speak -- and the
[projects](mini-projects.md) that build on it. When students outgrow the
three-line loop, [Pipecat](https://github.com/pipecat-ai/pipecat) is where
the streaming, interruptions, and phone-line transports live.
