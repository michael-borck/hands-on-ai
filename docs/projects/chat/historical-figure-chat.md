# Historical Figure Chat

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Historical research, character perspective, dialogue  
**Module**: chat

## Overview

Chat with simulated historical figures to learn about their lives, achievements, and time periods.

> 🧠 **LLMs have no memory of their own.** Each `get_response()` call is
> independent: the model only sees the `system` prompt plus the single `prompt`
> you pass *this* call. To make a bot that "remembers" earlier turns, **you** keep
> the conversation history and resend it each time, as this project does below.
> There is no hidden state doing it for you.

## Instructions

```python
from hands_on_ai.chat import get_response
import random

def historical_figure_chat():
    """Chat with simulated historical figures"""
    # Available historical figures
    figures = {
        "Albert Einstein": "physicist who developed the theory of relativity",
        "Marie Curie": "physicist and chemist who conducted pioneering research on radioactivity",
        "Leonardo da Vinci": "Renaissance polymath known for art and inventions",
        "Ada Lovelace": "mathematician and writer, known for work on Babbage's Analytical Engine",
        "Martin Luther King Jr.": "civil rights leader and advocate for nonviolent resistance",
        "Cleopatra": "last active ruler of the Ptolemaic Kingdom of Egypt",
        "Mahatma Gandhi": "leader of India's nonviolent independence movement",
        "Confucius": "Chinese philosopher and politician of the Spring and Autumn period",
        "Frida Kahlo": "Mexican painter known for her portraits and works inspired by nature",
        "Nelson Mandela": "revolutionary and political leader who served as President of South Africa"
    }
    
    print("=== Historical Figure Chat ===")
    print("Available historical figures:")
    
    figure_list = list(figures.keys())
    for i, figure in enumerate(figure_list):
        print(f"{i+1}. {figure} - {figures[figure]}")
    
    figure_choice = int(input("\nSelect a figure (1-10): ")) - 1
    figure = figure_list[figure_choice]
    
    system_prompt = f"""
    You are {figure}, {figures[figure]}.
    Respond as if you are this historical figure, with appropriate knowledge, perspective, and speaking style.
    Your knowledge is limited to what was known during your lifetime and your own experiences.
    If asked about events after your lifetime, you should acknowledge you wouldn't know about them.
    Maintain the personality, values, and worldview of {figure} based on historical accounts.
    """
    
    print(f"\n=== Conversation with {figure} ===")
    print(f"You are now chatting with {figure}. Type 'exit' to end.")
    
    # Welcome message
    greetings = [
        f"Greetings! I am {figure}. What would you like to discuss?",
        f"Hello there! {figure} at your service. How may I assist you?",
        f"Welcome! You're speaking with {figure}. What's on your mind?",
        f"Ah, a visitor! I am {figure}. What would you like to know?",
        f"Good day! It's {figure} here. What shall we talk about?"
    ]
    
    print("\n" + random.choice(greetings))
    
    # Chat loop. get_response is stateless, so we keep our own running transcript
    # and resend it every turn. That is what gives the figure "memory" of the
    # conversation so it can follow up on what was said earlier.
    transcript = ""
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            print(f"\n{figure}: Farewell! It was a pleasure speaking with you.")
            break

        # Send the conversation so far plus the new question
        prompt = f"{transcript}You: {user_input}\n{figure}:"
        response = get_response(prompt, system=system_prompt)
        print(f"\n{figure}: {response}")

        # Remember this exchange for the next turn
        transcript += f"You: {user_input}\n{figure}: {response}\n"

# Run the historical figure chat
if __name__ == "__main__":
    historical_figure_chat()
```

## Extension Ideas

Add a "time travel interview" mode where students can interview multiple figures about the same topic or event.

---