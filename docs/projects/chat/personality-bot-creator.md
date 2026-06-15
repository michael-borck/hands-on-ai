# Personality Bot Creator

**Difficulty**: Beginner  
**Time**: 30-45 minutes  
**Learning Focus**: Functions, creativity, system prompts  
**Module**: chat

## Overview

Students create and interact with a bot that has a unique personality of their design. This project teaches function definition and the impact of system prompts on AI behavior.

## Instructions

```python
from hands_on_ai.chat import get_response

# A bot's personality comes entirely from its `system` prompt. That's the
# string that tells the model how to behave. (The optional `personality=`
# argument only selects which canned "please wait" message is shown if a request
# has to be retried, so we leave it at its default here.)
def superhero_bot(prompt):
    return get_response(
        prompt,
        system="You are a confident superhero who always thinks positively and believes any problem can be solved. You occasionally reference your superpowers and heroic deeds.",
    )

def grumpy_cat_bot(prompt):
    return get_response(
        prompt,
        system="You are a perpetually unimpressed cat. You respond with short, sarcastic comments and often mention how humans are inferior to cats.",
    )

def chef_bot(prompt):
    return get_response(
        prompt,
        system="You are an enthusiastic chef who relates everything to cooking. You use cooking metaphors and occasionally share recipe ideas regardless of the topic.",
    )

# Test your bot with various prompts
test_prompts = [
    "How's the weather today?",
    "Can you help me with my homework?",
    "What's the meaning of life?",
    "Tell me about yourself."
]

# Choose which bot to use
my_bot = superhero_bot  # Change to your custom bot

# Test it with each prompt
for prompt in test_prompts:
    print(f"Prompt: {prompt}")
    print(f"Response: {my_bot(prompt)}")
    print("-" * 50)
```

## Extension Ideas

Create a menu system that lets the user choose which personality to talk to.

---