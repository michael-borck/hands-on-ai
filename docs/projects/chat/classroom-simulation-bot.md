# Classroom Simulation Bot

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Functions, menu systems, multiple bot use  
**Module**: chat

## Overview

Create a classroom simulation where students can interact with different characters or experts on various topics, practicing both coding skills and exploring different perspectives.

> 🧠 **LLMs have no memory of their own.** Each `get_response()` call is
> independent — the model only sees the `system` prompt plus the single `prompt`
> you pass *this* call. If you want the bot to "remember" earlier turns, keep a
> running transcript and include it in the prompt yourself; nothing does it
> automatically.

## Instructions

```python
from hands_on_ai.chat import get_response

def classroom_simulation():
    print("=== Virtual Classroom Simulation ===")
    print("Ask questions to different characters about any topic!")
    print("Type 'exit' at any time to quit.\n")
    
    # Define different bot personalities
    def teacher_bot(prompt):
        return get_response(
            prompt,
            system="You are a knowledgeable, patient teacher who explains concepts clearly with examples. You encourage critical thinking and use analogies to simplify complex ideas. Keep explanations concise but thorough."
        )
    
    def hacker_bot(prompt):
        return get_response(
            prompt,
            system="You are an ethical hacker with expertise in cybersecurity. You explain technical concepts with a slightly rebellious attitude but always emphasize ethical practices and security. Never provide instructions for illegal activities. Use technical terminology but explain it."
        )
    
    def pirate_bot(prompt):
        return get_response(
            prompt,
            system="You are a pirate captain from the Golden Age of Piracy. You speak with pirate slang and terminology (arr, matey, etc.). Despite your rough manner, you're surprisingly knowledgeable about navigation, history, and seafaring. Keep responses brief and entertaining."
        )
    
    def scientist_bot(prompt):
        return get_response(
            prompt,
            system="You are a brilliant scientist who is excited about all fields of science. You explain scientific concepts with enthusiasm and wonder, citing relevant research and discoveries. You are factual and precise but can make complex ideas accessible."
        )
    
    # Display available characters
    def show_menu():
        print("\n=== Available Characters ===")
        print("1. Teacher - Clear explanations and educational guidance")
        print("2. Hacker - Cybersecurity and tech knowledge with attitude")
        print("3. Pirate - Nautical expertise with a swashbuckling style")
        print("4. Scientist - Enthusiastic scientific explanations")
        print("5. Exit simulation")
    
    # Main interaction loop
    while True:
        show_menu()
        choice = input("\nChoose a character (1-5): ")
        
        # Exit condition
        if choice == "5" or choice.lower() == "exit":
            print("Exiting the classroom simulation. Thanks for participating!")
            break
            
        # Select the appropriate bot based on user choice
        if choice == "1":
            bot = teacher_bot
            name = "Teacher"
        elif choice == "2":
            bot = hacker_bot
            name = "Hacker"
        elif choice == "3":
            bot = pirate_bot
            name = "Pirate Captain"
        elif choice == "4":
            bot = scientist_bot
            name = "Scientist"
        else:
            print("Invalid choice. Please enter a number from 1-5.")
            continue
        
        # Get the question from the user
        question = input(f"\nWhat would you like to ask the {name}? ")
        
        # Exit condition
        if question.lower() == "exit":
            print("Exiting the classroom simulation. Thanks for participating!")
            break
            
        # Get the response from the selected bot
        print(f"\n{name}:")
        response = bot(question)
        print(response)
        
        # Ask if they want to ask another question to the same character
        while True:
            another = input(f"\nWould you like to ask the {name} another question? (yes/no): ").lower()
            
            if another == "no" or another == "exit":
                break
            elif another == "yes":
                question = input(f"\nWhat's your next question for the {name}? ")
                
                # Exit condition
                if question.lower() == "exit":
                    print("Exiting the classroom simulation. Thanks for participating!")
                    return
                    
                print(f"\n{name}:")
                response = bot(question)
                print(response)
            else:
                print("Please answer 'yes' or 'no'.")

# Run the classroom simulation
if __name__ == "__main__":
    classroom_simulation()
```

## Extension Ideas

- Add more character types like historian, artist, or fictional character
- Create a debate mode where two characters discuss the same topic
- Add a quiz feature where characters test the user's knowledge
- Create a storyline or scenario that involves multiple characters
- Allow characters to "remember" previous interactions in the session

---