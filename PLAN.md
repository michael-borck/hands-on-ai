# Plan: voice + vision for HandsOnAI

Add two small modules — `vision` (describe images) and `voice` (STT/TTS) — in
the house style: one concept, a few dozen readable lines, provider-agnostic via
OpenAI-compatible HTTP, runnable locally with no API keys. Image/music/song
*creation* is out of scope: nothing trivial fits the philosophy (heavy installs,
or teaches nothing beyond `chat`). The gap is the lesson — point to ComfyUI,
AudioCraft, and friends in "Going deeper".

## Decisions

1. **Skip image/song/music creation.** Heavy models or redundant concepts.
2. **Pipecat is the graduation path, not a dependency.** Link it from the
   philosophy "Going deeper" map and from the voice project; never import it.
3. **"Going deeper" stays canonical.** LlamaIndex, LangGraph, Instructor,
   Pydantic AI, LiteLLM are already listed in `docs/philosophy.md`. New module
   docs link to that section instead of repeating link lists.
4. **Curated OSS mentions** (each teaches a concept, map not manual):
   - Local STT: whisper.cpp, faster-whisper
   - Local TTS: Piper, Kokoro
   - Turn-taking/VAD: Silero VAD
   - Tiny vision models: moondream, SmolVLM
   - Production voice frameworks: Pipecat, LiveKit Agents
   - Beyond using models → building them: Karpathy's nanoGPT / Zero-to-Hero

## Phases

### Phase 1 — `vision` module (zero new deps)

- `src/hands_on_ai/vision/` with one function:
  `describe(image, prompt="Describe this image.") -> str`
  - Accepts a local path or URL; base64-encodes local files into an
    OpenAI-format `image_url` content part; one `chat/completions` call.
  - Works with Ollama (moondream, llava, qwen2.5-vl), OpenAI, Groq, Gemini.
- Config key `HANDS_ON_AI_VISION_MODEL` (default `moondream`, 1.6B and
  classroom-friendly), reusing existing server/key config.
- CLI: `vision ask photo.jpg "What's in this?"` plus `vision describe photo.jpg`.
- Docs: `vision-concepts.md`, `vision-guide.md`; update README module table,
  LLM.txt, api-reference, mkdocs.yml.
- Tests mocking HTTP like existing test files.

### Phase 2 — `voice` module

- Two thin HTTP functions, same provider-agnostic pattern:
  - `transcribe(audio_path) -> str` — POST `/v1/audio/transcriptions`
  - `speak(text, voice=None, out_path=None) -> Path` — POST `/v1/audio/speech`
- Config: `HANDS_ON_AI_STT_SERVER/_MODEL`, `HANDS_ON_AI_TTS_SERVER/_MODEL`
  (defaulting to the main server).
- CLI: `voice transcribe audio.wav`, `voice speak "..."`, and the flagship
  **`voice chat`** — a REPL looping listen → `chat.ask` → speak.
- Mic capture stays out of core (would need sounddevice); it is an extension
  exercise in the project.

### Phase 3 — local audio server guide

- `docs/deploy-audio-server.md`: one Docker container (speaches serves
  OpenAI-compatible Whisper STT + Kokoro TTS; whisper.cpp server as an
  alternative) — keeps the "free local models, no API keys" promise.

### Phase 4 — projects

- `docs/projects/voice/build-the-worlds-smallest-pipecat.md` — build a
  push-to-talk voice loop, try continuous listening, hit the turn-taking
  problem, then read Pipecat's pipeline with new eyes.
- `docs/projects/vision/talking-picture.md` — vision + voice combined:
  describe an image aloud. Capstone using both modules.
- Update `projects/index.md` and `mini-projects.md` categories.

### Phase 5 — polish

- philosophy.md "Going deeper": add a voice-frameworks bullet.
- README/LLM.txt module tables, CHANGELOG, version bump.

## Order

Vision first (smallest, de-risks the config pattern), voice second, projects
last since they use both.
