# Bot Personality Menu Generator

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Dictionaries, functions, menu systems  
**Module**: chat

## Overview

Create a flexible menu system that allows users to interact with multiple bot personalities on demand, practicing dictionary management, function mappings, and user interface design.

> 🧠 **LLMs have no memory of their own.** Each `get_response()` call is
> independent: the model only sees the `system` prompt plus the single `prompt`
> you pass *this* call. If you want the bot to "remember" earlier turns, keep a
> running transcript and include it in the prompt yourself; nothing does it
> automatically.

## Instructions

```python
from hands_on_ai.chat import get_response

def personality_menu():
    print("=== Bot Personality Menu Generator ===")
    print("Interact with various bot personalities!")
    print("Type 'exit' at any time to quit.\n")
    
    # Define different bot personalities
    def friendly_bot(prompt):
        return get_response(
            prompt,
            system="You are a friendly, helpful assistant who is always positive and encouraging. You use warm language and provide supportive responses."
        )
    
    def emoji_bot(prompt):
        return get_response(
            prompt,
            system="You are an emoji enthusiast who includes multiple relevant emojis in every response. Your tone is upbeat and playful. Make sure to use at least 3-5 emojis in each message."
        )
    
    def pirate_bot(prompt):
        return get_response(
            prompt,
            system="You are a salty pirate captain from the Golden Age of Piracy. You speak with pirate slang (arr, matey, avast, etc.) and make frequent references to sailing, treasure, and the sea. Your responses are brief and colorful."
        )
    
    def teacher_bot(prompt):
        return get_response(
            prompt,
            system="You are a patient, knowledgeable teacher who explains concepts clearly. You break down complex ideas into simple terms and use examples to illustrate points. Your tone is educational but never condescending."
        )
    
    def detective_bot(prompt):
        return get_response(
            prompt,
            system="You are a sharp-witted detective with keen analytical skills. You approach every question like a mystery to solve, looking for clues and making deductions. Your tone is contemplative and slightly dramatic, similar to classic detective novels."
        )
    
    def poet_bot(prompt):
        return get_response(
            prompt,
            system="You are a lyrical poet who often speaks in verse or uses metaphorical language. Your responses are thoughtful and artistic, with attention to the rhythm and beauty of language. Occasionally include short poems in your responses."
        )
    
    # Store bot functions in a dictionary for easy access
    bots = {
        "1": {"name": "Friendly Assistant", "function": friendly_bot, "description": "Warm and supportive"},
        "2": {"name": "Emoji Enthusiast", "function": emoji_bot, "description": "Playful with lots of emojis"},
        "3": {"name": "Pirate Captain", "function": pirate_bot, "description": "Salty sea dog with nautical flair"},
        "4": {"name": "Wise Teacher", "function": teacher_bot, "description": "Patient and educational"},
        "5": {"name": "Detective", "function": detective_bot, "description": "Analytical problem-solver"},
        "6": {"name": "Poet", "function": poet_bot, "description": "Lyrical and metaphorical"}
    }
    
    # Function to display the menu
    def show_menu():
        print("\n=== Available Bot Personalities ===")
        for key, bot_info in bots.items():
            print(f"{key}. {bot_info['name']} - {bot_info['description']}")
        print("7. Exit")
    
    # Main interaction loop
    current_bot = None
    current_bot_name = None
    
    while True:
        if current_bot is None:
            show_menu()
            choice = input("\nSelect a bot personality (1-7): ")
            
            # Exit condition
            if choice == "7" or choice.lower() == "exit":
                print("Thanks for using the Bot Personality Menu! Goodbye!")
                break
                
            if choice in bots:
                current_bot = bots[choice]["function"]
                current_bot_name = bots[choice]["name"]
                print(f"\nYou're now chatting with the {current_bot_name}!")
                
                # Welcome message from the selected bot
                welcome = current_bot("Give a brief introduction of yourself.")
                print(f"{current_bot_name}: {welcome}")
            else:
                print("Invalid choice. Please select a number from 1-7.")
                continue
        
        # Interaction with the current bot
        user_input = input("\nYou: ")
        
        # Check for exit or menu commands
        if user_input.lower() == "exit":
            print("Thanks for using the Bot Personality Menu! Goodbye!")
            break
        elif user_input.lower() == "menu":
            current_bot = None
            continue
        
        # Get response from the current bot
        response = current_bot(user_input)
        print(f"\n{current_bot_name}: {response}")
        
        # Option to change bots
        print("\nType 'menu' to switch bots or 'exit' to quit")

# Run the personality menu
if __name__ == "__main__":
    personality_menu()
```

## Extension Ideas

- Allow users to create and save their own custom bot personalities
- Add a "random" option that selects a personality at random
- Create a rating system where users can score responses
- Implement a "conversation history" feature that remembers past interactions
- Create themed conversation scenarios for different bot personalities