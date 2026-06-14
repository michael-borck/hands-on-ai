# Emotional Support Bot

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: Selection, text analysis, branching logic  
**Module**: chat

## Overview

Create a bot that responds differently based on the user's emotional state, providing tailored support, advice, or encouragement depending on the mood expressed.

> 🧠 **LLMs have no memory of their own.** Each `get_response()` call is
> independent — the model only sees the `system` prompt plus the single `prompt`
> you pass *this* call. If you want the bot to "remember" earlier turns, keep a
> running transcript and include it in the prompt yourself; nothing does it
> automatically.

## Instructions

```python
from hands_on_ai.chat import get_response

def emotional_support_bot():
    print("=== Emotional Support Bot ===")
    print("This bot will respond differently based on how you're feeling.")
    print("Type 'exit' at any time to quit.\n")
    
    # Define different bot personalities for different moods
    def therapist_bot(prompt):
        return get_response(
            prompt,
            system="You are a compassionate and empathetic therapist. Provide supportive, thoughtful responses that validate the user's feelings. Offer gentle guidance and perspective without being pushy. Keep responses brief and focused on emotional support."
        )
    
    def coach_bot(prompt):
        return get_response(
            prompt,
            system="You are an energetic and motivational coach. Be enthusiastic, positive, and encouraging. Help channel the user's good energy into productive actions or goals. Keep responses upbeat and action-oriented."
        )
    
    def chill_bot(prompt):
        return get_response(
            prompt,
            system="You are a calm, relaxed friend. Your responses are low-pressure and soothing. Suggest restful activities and ways to recharge. Keep responses brief and gentle."
        )
    
    # Main interaction loop
    while True:
        # Ask how the user is feeling
        mood = input("\nHow are you feeling today? (happy, sad, tired, anxious, exit): ").lower()
        
        # Exit condition
        if mood == "exit":
            print("Take care! Remember I'm here whenever you need to talk.")
            break
        
        # Get more details about their state
        if mood in ["happy", "sad", "tired", "anxious"]:
            details = input(f"Tell me more about why you're feeling {mood}: ")
            
            # Select appropriate bot based on mood
            if mood == "sad" or mood == "anxious":
                response = therapist_bot(f"I'm feeling {mood}. {details}")
            elif mood == "happy":
                response = coach_bot(f"I'm feeling {mood}! {details}")
            elif mood == "tired":
                response = chill_bot(f"I'm feeling {mood}. {details}")
            
            print("\nBot's response:")
            print(response)
            
            # Follow-up question based on mood
            if mood in ["sad", "anxious"]:
                follow_up = input("\nWould you like some suggestions to help you feel better? (yes/no): ")
                if follow_up.lower() == "yes":
                    suggestions = get_response(
                        f"The user is feeling {mood} because: {details}. Provide 3 specific, helpful suggestions to improve their mood.",
                        system="You are a supportive counselor offering practical, actionable advice. Format your response as a numbered list."
                    )
                    print("\nHere are some suggestions:")
                    print(suggestions)
            elif mood == "happy":
                follow_up = input("\nWould you like ideas to make the most of your good mood? (yes/no): ")
                if follow_up.lower() == "yes":
                    ideas = get_response(
                        f"The user is feeling {mood} because: {details}. Suggest 3 ways to channel this positive energy productively.",
                        system="You are an enthusiastic coach offering creative ways to use positive energy. Format your response as a numbered list."
                    )
                    print("\nHere are some ideas:")
                    print(ideas)
            elif mood == "tired":
                follow_up = input("\nWould you like some relaxation or energy tips? (relax/energy): ")
                if follow_up.lower() == "relax":
                    tips = get_response(
                        "Suggest 3 calming activities for someone who is tired and wants to relax.",
                        system="You are a wellness coach specializing in restful activities. Format your response as a numbered list."
                    )
                    print("\nRelaxation suggestions:")
                    print(tips)
                elif follow_up.lower() == "energy":
                    tips = get_response(
                        "Suggest 3 gentle ways to boost energy when feeling tired without causing stress.",
                        system="You are a wellness coach specializing in natural energy boosters. Format your response as a numbered list."
                    )
                    print("\nEnergy-boosting suggestions:")
                    print(tips)
        else:
            print("I don't recognize that mood. Please try again with happy, sad, tired, or anxious.")

# Run the emotional support bot
if __name__ == "__main__":
    emotional_support_bot()
```

## Extension Ideas

- Add more emotional states and corresponding bot personalities
- Create a mood tracking feature that remembers past interactions
- Implement sentiment analysis to detect mood from user's free text input
- Create a guided meditation or breathing exercise option
- Allow users to rate how helpful the responses were to improve the bot

---