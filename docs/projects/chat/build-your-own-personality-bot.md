# Build Your Own Personality Bot

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Functions, system prompts, creative writing  
**Module**: chat

## Overview

Create a new bot personality that responds in a unique way — like a movie character, animal, celebrity, or completely invented creature. Students will learn how to craft system prompts that reflect specific voices or styles.

> 🧠 **LLMs have no memory of their own.** Each `get_response()` call is
> independent — the model only sees the `system` prompt plus the single `prompt`
> you pass *this* call. If you want the bot to "remember" earlier turns, keep a
> running transcript and include it in the prompt yourself; nothing does it
> automatically.

## Instructions

```python
from hands_on_ai.chat import get_response

# Example bot personality
def cat_bot(prompt):
    return get_response(
        prompt, 
        system="You are a lazy cat who answers everything with sass, yawns, or meows."
    )

# Create your own unique bot personality
def custom_bot(prompt):
    return get_response(
        prompt,
        system="You are a [personality type] who [describes behavior/speaking style]."
    )

# Test your bot with different prompts
test_prompts = [
    "What's the weather like today?",
    "Explain quantum physics to me.",
    "What should I do this weekend?",
    "Tell me a joke."
]

# Choose which bot to use
my_bot = cat_bot  # Replace with your custom bot

# Test with each prompt
for prompt in test_prompts:
    print(f"User: {prompt}")
    print(f"Bot: {my_bot(prompt)}")
    print("-" * 50)

# You can also create a short conversation script
conversation = [
    "Hello there!",
    "What's your favorite food?",
    "Tell me something interesting about yourself.",
    "Goodbye!"
]

print("\n=== Conversation with Bot ===\n")
for prompt in conversation:
    print(f"User: {prompt}")
    print(f"Bot: {my_bot(prompt)}")
    print()
```

## Extension Ideas

- Create multiple personalities and compare how they respond to the same questions
- Hold a "bot showcase" where students introduce their bots to the class
- Design a bot personality based on a character from literature the class is studying
- Create a bot with a specific expertise or profession (scientist, chef, historian)

---