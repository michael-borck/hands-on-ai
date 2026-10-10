# Understanding Voice (Speech In, Speech Out)

You can already talk to a model with your [fingers](chat-concepts.md) and show
it pictures with [vision](vision-concepts.md). The voice module adds the last
two senses: **ears** (speech-to-text) and a **mouth** (text-to-speech).

## The one-sentence version

Speech recognition and speech synthesis are just format converters --
sound waves to text, text to sound waves -- so a voice agent is the
[chat](chat-concepts.md) loop with two converters bolted on.

## The whole idea in three lines

```python
from hands_on_ai.chat import Conversation
from hands_on_ai.voice import speak, transcribe

conversation = Conversation()
reply = conversation.ask(transcribe("question.wav"))   # ears -> brain
speak(reply)                                           # brain -> mouth
```

Listen. Think. Speak. The model in the middle is the exact same
`get_response`-shaped call you met on day one -- no new kind of AI, just two
new kinds of plumbing:

- **STT** (speech-to-text): audio file in, words out. In the API this is one
  `POST /v1/audio/transcriptions` with the file attached.
- **TTS** (text-to-speech): text in, audio file out. One
  `POST /v1/audio/speech`.

That is genuinely all `transcribe` and `speak` do, which is the point: small
models (Whisper for listening, Kokoro and Piper for speaking) got good enough
and small enough that "add a voice" went from a research project to a
function call.

## Why your `voice chat` types instead of listens

The bundled `voice chat` REPL asks you to *type* your side of the
conversation and speaks the replies. That is honest about what the module
does: transcription and speech are solved; the hard part of a real voice
agent is everything *around* the loop:

- **Capturing the mic** needs extra machinery (recording libraries, audio
  devices, permissions).
- **Knowing when you stopped talking** (turn-taking) is its own problem. Say
  "um..." and a naive recorder keeps waiting. Detecting speech vs silence is
  called **voice activity detection (VAD)**, and tiny models like Silero VAD
  do it -- that's a whole concept on its own.
- **Interrupting the bot mid-sentence** (barge-in) means listening while
  speaking and deciding who should yield.

Those three problems are exactly what production voice frameworks handle.
Build the naive loop yourself, feel where it breaks, and you'll understand
why [Pipecat](https://github.com/pipecat-ai/pipecat) exists -- that's the
[Build the world's smallest Pipecat](projects/voice/build-the-worlds-smallest-pipecat.md)
project.

## Honest caveats

- **Accent and noise matter.** Small local STT models are impressive until
  the room gets noisy. Set a `language` hint to help.
- **Voices vary by provider.** The voice name `"alloy"` is a polite fiction:
  each server maps it to whatever voices it has. Don't expect the same voice
  everywhere.
- **Latency is the real enemy.** Each of the three steps adds delay; a chatty
  answer read aloud gets old fast. (This is why real systems stream and
  interrupt.)
- **Memory grows with the conversation.** `Conversation` resends the whole
  transcript every turn -- now read aloud. Keep answers short.

## Where it fits

Voice is a side module, like [vision](vision-concepts.md): it shows that the
chat loop is the universal skeleton, whatever the senses. Text, images, and
speech all reduce to the same trick -- convert the input into something the
model reads, then convert the output back. Once you've wired a voice agent
yourself, the jump to a production framework is a jump in *engineering*
(streaming, VAD, transports like WebRTC), not in AI.

Ready to try it? The [voice guide](voice-guide.md) covers setup and the CLI.
