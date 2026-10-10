# Build the World's Smallest Pipecat

**Difficulty**: Advanced  
**Time**: 90 minutes  
**Learning Focus**: Voice agents, turn-taking, VAD, streaming architecture  
**Module**: voice

## Overview

You'll build a working voice agent that *listens to your microphone*, thinks,
and *talks back*. Then you'll push it until it breaks -- and discover, first
hand, exactly the problems that production frameworks solve. When you finish,
you'll be able to read
[Pipecat](https://github.com/pipecat-ai/pipecat)'s pipeline and recognise
every piece of it.

> 🧠 **Voice agents in one line:** listen (STT) -> think (LLM) -> speak (TTS).
> See [Understanding Voice](../../voice-concepts.md) for the concepts. This
> project is the part the module deliberately left out: real microphone input.

## What you need

- A working audio server (see [Voice Guide](../../voice-guide.md) setup, or
  [Host an Audio Server](../../deploy-audio-server.md)), or cloud STT/TTS keys
- A microphone and speakers
- One extra package for recording: `pip install sounddevice numpy`

## Step 1: The loop, file to file (no mic yet)

Write `agent.py`. This is the whole voice agent -- say it out loud to
appreciate how small it is:

```python
from hands_on_ai.chat import Conversation
from hands_on_ai.voice import speak, transcribe

conversation = Conversation(system="Keep answers to one or two sentences.")

reply = conversation.ask(transcribe("question.wav"))
print("Bot:", reply)
speak(reply, out_path="answer.wav")
```

Record a `question.wav` with your OS voice recorder, play `answer.wav`, and
confirm the loop works end to end before adding any machinery.

## Step 2: Capture the microphone

Now replace the hand-made file with live recording. `sounddevice` grabs raw
samples; the `wave` module writes them to a file `transcribe` can read.

```python
import sounddevice as sd
import wave

def record(seconds=4, rate=16000):
    print("🎙️ Listening...")
    audio = sd.rec(int(seconds * rate), samplerate=rate, channels=1)
    sd.wait()                      # blocks until time is up
    with wave.open("question.wav", "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes((audio * 32767).astype("int16").tobytes())
```

## Step 3: Push-to-talk loop

Wire it together: press Enter, the computer listens for four seconds, then
thinks and speaks. This is the classic **push-to-talk** pattern -- a walkie-
talkie, not a conversation.

```python
while True:
    input("Press Enter to talk (or Ctrl-C to quit)...")
    record(seconds=4)
    reply = conversation.ask(transcribe("question.wav"))
    print("Bot:", reply)
    speak(reply, out_path="answer.wav")
```

Talk to it. Ask it two questions in a row. It works! Now try these, and note
what goes wrong:

1. Ask a question that takes more than four seconds to say.
2. Wait a beat before speaking. Count how long the dead air lasts.
3. Try to interrupt the bot while it's talking.

## Step 4: Meet the three walls

You have just met the three problems every real voice agent must solve:

- **Truncation.** A fixed recording length either cuts you off (too short) or
  wastes time (too long). You need to *detect when the person stopped
  talking* -- that's **turn-taking**.
- **Silence and noise.** "Um..." pauses, background chatter, and breathing all
  look like sound. Deciding *speech vs not-speech* is **voice activity
  detection (VAD)**.
- **No barge-in.** While the bot is speaking, it can't hear you. Humans
  interrupt each other constantly; real agents must listen *while* talking.

## Step 5: Your first VAD (record-until-quiet)

Replace the fixed timer with a simple energy gate: record in small chunks,
keep going while the sound is loud enough, stop after a short quiet spell.

```python
def record_until_silence(rate=16000, chunk=0.1, threshold=0.01, quiet_chunks=10):
    print("🎙️ Listening (speak up, then pause)...")
    frames, quiet = [], 0
    with sd.InputStream(samplerate=rate, channels=1, dtype="int16") as stream:
        while True:
            data, _ = stream.read(int(chunk * rate))
            frames.append(data)
            loud = abs(data).mean() > threshold * 32767
            quiet = 0 if loud else quiet + 1
            if frames and quiet >= quiet_chunks:   # ~1s of near-silence
                break
    with wave.open("question.wav", "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(b"".join(frames))
```

Swap this into the Step 3 loop. Better! Now try it across a noisy room, or
hum while it waits, or pause mid-sentence. Each failure is one of the walls
from Step 4, seen up close. Tune `threshold` and watch the trade-off: too low
and it never stops, too high and it clips your words.

## Step 6: Read Pipecat with new eyes

Open the [Pipecat repository](https://github.com/pipecat-ai/pipecat) and skim
`src/pipecat/`. With your agent in hand, you can now name what you see:

| Your 90 lines | Pipecat's answer |
|---|---|
| `record()` / `sounddevice` | **Transports** (WebRTC, Daily, websocket) moving audio frames both ways |
| Step 5's energy gate | **VAD analysers** (Silero VAD -- a tiny neural net, not an energy gate) |
| the `while True` loop | **Frame pipelines**: audio/video/text frames flowing through processors |
| `transcribe` per turn | **Streaming STT** services fed frames continuously |
| `speak` blocking | **Streaming TTS**, with interruption handling to cut speech mid-word |

Read one example (e.g. `examples/` -- the simple chatbot) and find where each
of your three walls is handled. You'll notice the *ideas* are the ones you
just learned; the framework is engineering for latency, interruption, and
scale.

## Extensions

Pick any of these:

- **Barge-in, cheap version.** Play `answer.wav` in a background thread and
  watch the mic's energy while it plays; abort the playback if the level
  spikes. (True echo cancellation is why this is hard -- that's a wall too.)
- **A real VAD.** `pip install silero-vad` (or use it via ONNX) and swap it in
  for the energy gate. Compare false-start behaviour in a noisy room.
- **Latency budget.** Time each stage (record, transcribe, LLM, TTS). Which
  dominates? What would you stream first to shrink the perceived delay?
- **Model swap.** Run the same agent against a cloud STT/TTS by changing two
  environment variables, and compare accuracy and latency.

> 💡 A type-hints exercise works as an extension for almost any project: the
> example code is kept plain on purpose (see [Mini-Projects Overview](../../mini-projects.md#a-note-on-type-hints)),
> so adding annotations and running `mypy`/`pyright` is a great next step for
> students ready for industry best practice.

## How it works under the hood

`transcribe` and `speak` are each about 40 lines of plain Python in
[`hands_on_ai/voice/`](https://github.com/michael-borck/hands-on-ai/blob/main/src/hands_on_ai/voice/):
one OpenAI-compatible HTTP call to `/v1/audio/transcriptions` (multipart
upload, text back) and one to `/v1/audio/speech` (text in, WAV bytes back).
There is no streaming, no VAD, and no transport -- deliberately. Once you've
felt why those matter, you know exactly what a framework like Pipecat is
*for*.
