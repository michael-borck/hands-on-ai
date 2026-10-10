#!/usr/bin/env python3
"""
Simple Voice Example - Demonstrates basic usage of hands-on-ai voice.

This example shows how to:
1. Speak text aloud to a WAV file (text-to-speech)
2. Check the generated audio file
3. Transcribe an audio file (speech-to-text) -- pass one as an argument
4. The whole voice agent in three lines (shown, and runnable with a WAV)

Requirements:
- hands-on-ai package installed
- An OpenAI-compatible AUDIO server for speak/transcribe. Plain Ollama does
  not serve audio. Quickest local option:
    docker run -p 8000:8000 speaches-ai/speaches:latest-cpu
    export HANDS_ON_AI_STT_SERVER=http://localhost:8000
    export HANDS_ON_AI_TTS_SERVER=http://localhost:8000
"""

import sys
import wave
from pathlib import Path

from hands_on_ai.voice import speak, transcribe


def main():
    """Run the simple voice example."""
    print("🚀 Simple Voice Example")
    print("=" * 50)

    # Step 1: Text-to-speech -- text in, WAV file out
    print("\n🗣️  Step 1: speak('...') -- writing speech.wav ...")
    result = speak("Hello class! This is your computer talking.")
    if isinstance(result, str):  # error message (❌/⚠️) in the toolkit style
        print(result)
        print("\n💡 Tip: point HANDS_ON_AI_TTS_SERVER at an audio server")
        print("   (plain Ollama does not serve audio -- see the module docs).")
        return
    print(f"✅ Audio written to: {result}")

    # Step 2: Peek inside the WAV header to see what came back
    print("\n🔬 Step 2: Checking the generated audio file...")
    with wave.open(str(result), "rb") as f:
        print(f"   channels={f.getnchannels()} rate={f.getframerate()}Hz "
              f"seconds={f.getnframes() / f.getframerate():.2f}")

    # Step 3: Speech-to-text -- transcribe any audio file you have
    print("\n👂 Step 3: transcribe(file) -- pass a WAV/MP3 as an argument")
    if len(sys.argv) > 1:
        print(f"   -> {transcribe(sys.argv[1])}")
    else:
        print("   (skipped: run `python simple_voice_example.py some-audio.wav`)")

    # Step 4: The whole voice agent, in three lines:
    #   conversation.ask(transcribe(audio)) -> speak(reply)
    print("\n🤖 Step 4: The three-line voice agent")
    print("""
    from hands_on_ai.chat import Conversation
    from hands_on_ai.voice import speak, transcribe

    conversation = Conversation()
    speak(conversation.ask(transcribe("question.wav")))
    """)
    if len(sys.argv) > 1:
        from hands_on_ai.chat import Conversation

        conversation = Conversation(system="Answer in one short sentence.")
        reply = conversation.ask(transcribe(sys.argv[1]))
        print(f"   Bot: {reply}")
        spoken = speak(reply, out_path="agent_answer.wav")
        print(f"   Spoken via: {spoken}")

    print("\n🎉 Example completed!")
    print("\nTo try the CLI commands:")
    print("  voice speak 'Well done, class.' --play")
    print("  voice transcribe recording.wav")
    print("  voice chat")


if __name__ == "__main__":
    main()
