#!/usr/bin/env python3
"""
Simple Vision Example - Demonstrates basic usage of hands-on-ai vision.

This example shows how to:
1. Generate a small test image (so the script runs with no downloads)
2. Describe an image with the default prompt
3. Ask specific questions about an image
4. Describe an image from a URL

Requirements:
- hands-on-ai package installed
- A vision-language model reachable on your configured server, e.g.:
    ollama pull moondream        # then: export HANDS_ON_AI_VISION_MODEL=moondream
  (any VLM works: llava, qwen2.5-vl, gemma3:4b, gpt-4o-mini, ...)
"""

from pathlib import Path

import fitz  # PyMuPDF, installed with hands-on-ai

from hands_on_ai.vision import describe
from hands_on_ai.config import get_vision_model


def make_test_image(path="vision_example.png"):
    """Draw a simple scene: a red square on a blue background."""
    doc = fitz.open()
    page = doc.new_page(width=200, height=200)
    page.draw_rect(fitz.Rect(0, 0, 200, 200), color=(0, 0, 1), fill=(0, 0, 1))
    page.draw_rect(fitz.Rect(50, 50, 150, 150), color=(1, 0, 0), fill=(1, 0, 0))
    page.get_pixmap().save(path)
    doc.close()
    return path


def main():
    """Run the simple vision example."""
    print("🚀 Simple Vision Example")
    print("=" * 50)
    print(f"Vision model: {get_vision_model()}\n")

    # Step 1: Make an image to talk about
    print("\n🖼️  Step 1: Generating a test image...")
    image = make_test_image()
    print(f"✅ Saved: {image}")

    # Step 2: Describe it with the default prompt
    print("\n👁️  Step 2: describe(image) -- the default description...")
    print(describe(image))

    # Step 3: Ask specific questions
    print("\n❓ Step 3: Asking specific questions...")
    for question in [
        "What colour is the square? One word.",
        "What shape is in the middle of the image? One word.",
    ]:
        print(f"  Q: {question}")
        print(f"  A: {describe(image, question)}\n")

    # Step 4: Describe an image from the web (same function, URL in).
    # NOTE: cloud providers (OpenAI, Groq, Gemini) fetch URLs server-side, but
    # Ollama does not -- there the answer comes back as an error, shown here.
    print("🌐 Step 4: describe(url) works on providers that fetch URLs...")
    url = "https://raw.githubusercontent.com/michael-borck/hands-on-ai/main/docs/assets/icon-192.png"
    answer = describe(url, "What does this icon depict? In one sentence.")
    if answer.startswith("❌"):
        print("  (This server does not fetch URLs -- download the file and")
        print("   describe the local path instead. Cloud providers accept URLs.)")
    else:
        print(f"  A: {answer}\n")

    # Tidy up, but keep the image if something failed so it can be inspected
    if Path(image).exists():
        Path(image).unlink()

    print("🎉 Example completed!")
    print("\nTo try the CLI command:")
    print("  vision photo.jpg 'What is in this image?'")


if __name__ == "__main__":
    main()
