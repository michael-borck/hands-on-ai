# AI Persona Dialogue Simulator

**Difficulty**: Intermediate  
**Time**: 45-60 minutes  
**Learning Focus**: Function calls, lists, creativity, dialogue simulation  
**Module**: chat

## Overview

Simulate interactive dialogues between multiple AI personas with different personalities or perspectives. This flexible tool enables both multi-participant panel discussions and focused one-on-one debates, allowing students to explore how different characters approach the same topics. The simulator can also be configured to run simulated interviews by selecting appropriate personas and question formats.

Simulate an interview or debate between multiple bots with different personalities or perspectives, exploring how different characters might approach the same questions or topics.

This project offers flexibility to run either panel discussions with multiple participants or focused one-on-one debates, allowing students to explore how different personas respond to the same topics.

> 🧠 **LLMs have no memory of their own.** Each `get_response()` call is
> independent — the model only sees the `system` prompt plus the single `prompt`
> you pass *this* call. If you want the bot to "remember" earlier turns, keep a
> running transcript and include it in the prompt yourself; nothing does it
> automatically.

## Instructions

```python
from hands_on_ai.chat import get_response
import time

def ai_persona_dialogue_simulator():
    """
    Simulate a dialogue between multiple AI personas with different personalities,
    exploring how different characters approach the same questions or topics.
    
    This tool supports multiple dialogue formats:
    1. Panel discussion - Multiple personas exchange views with less structure
    2. Formal debate - Two personas engage in structured argument with multiple rounds
    3. Interview - One persona can be set as an "interviewer" asking questions 
       of other personas serving as "interviewees"
    """
    print("=== AI Persona Dialogue Simulator ===")
    
    # Define different bot personalities
    # Each personality has a unique perspective that influences how they respond
    bot_personalities = {
        "Professor": "You are a logical, analytical professor who values facts, research, and intellectual rigor. You speak formally and cite evidence for your claims. You believe in rational inquiry and skepticism.",
        "Coach": "You are an inspirational coach who focuses on motivation, emotional intelligence, and personal growth. You believe in the power of passion, intuition, and human potential. You speak with enthusiasm and use motivational language.",
        "Artist": "You are a creative artist who values beauty, expression, and innovation. You think metaphorically and appreciate the abstract and subjective. You believe in breaking rules to create something new. Your language is colorful and expressive.",
        "Entrepreneur": "You are a practical entrepreneur focused on results, efficiency, and real-world applications. You value solutions that work and ideas that can be implemented. You speak directly and focus on action.",
        "Dr. Logic": "You value logical reasoning and empirical evidence above all. You cite studies and statistics to support your points. You believe decisions should be made based on data, not emotions.",
        "Empathetic Emma": "You believe emotional impact and human stories are most important. You consider how policies and ideas affect real people. You speak with compassion and emphasize the human element in every issue.",
        "Traditional Tom": "You value tradition, stability, and time-tested approaches. You're skeptical of rapid change and new untested ideas. You believe in preserving what works and making careful, incremental improvements.",
        "Interviewer": "You are a professional interviewer who asks insightful, probing questions. You're curious and neutral, aiming to bring out the most interesting perspectives from others. You follow up with clarifying questions when needed."
    }
    
    # List of debate/discussion topics
    # These can be used for debates, panel discussions, or interview topics
    dialogue_topics = [
        "What's more important: creativity or logic?",
        "Is technology improving or harming society?",
        "Should education focus more on facts or skills?",
        "Is it better to be a specialist or a generalist?",
        "Are humans naturally cooperative or competitive?",
        "What's the best way to measure success in life?",
        "Should we prioritize individual freedom or collective welfare?",
        "Is artificial intelligence more likely to help or harm humanity?",
        "Should governments regulate social media platforms?"
    ]
    
    # Let user select a dialogue topic
    # TODO: Add input validation to handle non-integer inputs
    print("Choose a topic:")
    for i, question in enumerate(dialogue_topics, 1):
        print(f"{i}. {question}")
    print(f"{len(dialogue_topics) + 1}. Custom topic (enter your own)")
    
    # Input validation could be added here to handle non-integer inputs
    try:
        choice = int(input("\nEnter topic number: "))
        if choice <= 0 or choice > len(dialogue_topics) + 1:
            print("Invalid choice. Using default topic #1.")
            choice = 1
    except ValueError:
        print("Invalid input. Using default topic #1.")
        choice = 1
    
    if choice <= len(dialogue_topics):
        dialogue_topic = dialogue_topics[choice - 1]
    else:
        dialogue_topic = input("\nEnter your custom topic: ")
    
    # Choose dialogue format
    # The format affects how the personas interact with each other
    print("\nChoose dialogue format:")
    print("1. Panel discussion (multiple personas participate in an open exchange)")
    print("2. One-on-one debate (two personas engage in structured argument)")
    print("3. Interview (one persona interviews the others)")
    
    # TODO: Add input validation for format choice
    try:
        format_choice = int(input("\nEnter format number (1-3): "))
        if format_choice < 1 or format_choice > 3:
            print("Invalid format. Using panel discussion (1).")
            format_choice = 1
    except ValueError:
        print("Invalid input. Using panel discussion (1).")
        format_choice = 1
    
    # Select personas based on format
    if format_choice == 1:
        # Panel discussion - let user select multiple participants
        # This mode simulates a roundtable where each persona responds to the previous one
        print("\nAvailable personalities:")
        for i, (name, perspective) in enumerate(bot_personalities.items(), 1):
            print(f"{i}. {name}: {perspective[:60]}...")
        
        # TODO: Add more robust input validation for selections
        selections = input("\nSelect personalities (comma-separated numbers, e.g., 1,3,4): ")
        try:
            selected_indices = [int(idx.strip()) - 1 for idx in selections.split(",")]
            # Check if indices are valid
            if any(idx < 0 or idx >= len(bot_personalities) for idx in selected_indices):
                print("Some selections were invalid. Using first 3 personalities.")
                selected_indices = [0, 1, 2]
        except ValueError:
            print("Invalid input. Using first 3 personalities.")
            selected_indices = [0, 1, 2]
        
        # Get the selected personalities
        personalities = list(bot_personalities.items())
        participants = {personalities[idx][0]: personalities[idx][1] for idx in selected_indices if 0 <= idx < len(personalities)}
        
        # Panel discussions typically have fewer rounds with more participants
        rounds = 1  
        
    elif format_choice == 2:
        # One-on-one debate - let user select exactly two participants
        # This mode creates a structured back-and-forth exchange with multiple rounds
        print("\nChoose two debaters:")
        for i, (name, perspective) in enumerate(bot_personalities.items(), 1):
            print(f"{i}. {name}: {perspective[:60]}...")
        
        # TODO: Add input validation for debater selections
        try:
            choice1 = int(input("\nSelect first debater (1-8): ")) - 1
            choice2 = int(input("Select second debater (1-8): ")) - 1
            
            if choice1 < 0 or choice1 >= len(bot_personalities) or choice2 < 0 or choice2 >= len(bot_personalities):
                print("Invalid selection. Using Professor and Coach.")
                choice1, choice2 = 0, 1
        except ValueError:
            print("Invalid input. Using Professor and Coach.")
            choice1, choice2 = 0, 1
        
        # Get the selected personalities
        personalities = list(bot_personalities.items())
        participants = {
            personalities[choice1][0]: personalities[choice1][1],
            personalities[choice2][0]: personalities[choice2][1]
        }
        
        # Set number of rounds for one-on-one debate
        try:
            rounds = int(input("\nHow many response rounds? (1-5): "))
            rounds = min(max(1, rounds), 5)  # Ensure rounds is between 1 and 5
        except ValueError:
            print("Invalid input. Using 2 rounds.")
            rounds = 2
    
    else:  # format_choice == 3
        # Interview format - one interviewer, multiple interviewees
        # This mode has one persona asking questions and others responding
        print("\nSelect the interviewer:")
        for i, (name, perspective) in enumerate(bot_personalities.items(), 1):
            print(f"{i}. {name}")
        
        # TODO: Add input validation for interviewer selection
        try:
            interviewer_idx = int(input("\nSelect interviewer (1-8, recommend #8 'Interviewer'): ")) - 1
            if interviewer_idx < 0 or interviewer_idx >= len(bot_personalities):
                print("Invalid selection. Using 'Interviewer' persona.")
                # Find the Interviewer in the list
                interviewer_idx = list(bot_personalities.keys()).index("Interviewer") if "Interviewer" in bot_personalities else 0
        except ValueError:
            print("Invalid input. Using 'Interviewer' persona.")
            interviewer_idx = list(bot_personalities.keys()).index("Interviewer") if "Interviewer" in bot_personalities else 0
        
        print("\nSelect interviewees:")
        personalities = list(bot_personalities.items())
        interviewees = list(range(len(personalities)))
        interviewees.remove(interviewer_idx)  # Remove interviewer from potential interviewees
        
        for i, idx in enumerate(interviewees, 1):
            name, perspective = personalities[idx]
            print(f"{i}. {name}: {perspective[:60]}...")
        
        # TODO: Add input validation for interviewee selections
        selections = input("\nSelect interviewees (comma-separated numbers): ")
        try:
            selected = [int(idx.strip()) - 1 for idx in selections.split(",")]
            # Convert selected indices to actual personality indices
            selected_indices = [interviewees[idx] for idx in selected if 0 <= idx < len(interviewees)]
            if not selected_indices:
                print("No valid selections. Using first two personalities.")
                selected_indices = interviewees[:2]
        except ValueError:
            print("Invalid input. Using first two personalities.")
            selected_indices = interviewees[:2]
        
        # Add interviewer and interviewees to participants
        participants = {personalities[interviewer_idx][0]: personalities[interviewer_idx][1]}
        for idx in selected_indices:
            participants[personalities[idx][0]] = personalities[idx][1]
        
        # Set number of interview questions
        try:
            rounds = int(input("\nHow many interview questions? (1-5): "))
            rounds = min(max(1, rounds), 5)  # Ensure rounds is between 1 and 5
        except ValueError:
            print("Invalid input. Using 3 questions.")
            rounds = 3
    
    # Function to get response from a bot
    def get_bot_response(prompt, perspective, name):
        """Generate a response from a persona based on their perspective."""
        system_prompt = f"You are {name}. {perspective} Keep responses under 100 words to keep the dialogue flowing."
        return get_response(prompt, system=system_prompt)
    
    # Start the dialogue
    participant_names = list(participants.keys())
    print(f"\n=== Dialogue on: {dialogue_topic} ===\n")
    time.sleep(1)
    
    # Opening statements (except for interview format)
    if format_choice != 3:  # Not interview format
        print("=== Opening Statements ===\n")
        statements = {}
        
        for name, perspective in participants.items():
            print(f"{name}'s opening statement:")
            statement = get_bot_response(
                f"Give an opening statement on the topic of {dialogue_topic}",
                perspective,
                name
            )
            statements[name] = statement
            print(statement)
            print()
            time.sleep(1)
    
    # Discussion rounds based on format
    if format_choice == 1:
        # Panel discussion - each persona responds to the previous speaker
        # This creates a chain of responses where each builds on the last
        print("\n=== Panel Discussion ===\n")
        
        previous_statement = statements[participant_names[-1]]
        previous_name = participant_names[-1]
        
        for round_num in range(rounds):
            print(f"--- Round {round_num + 1} ---\n")
            
            for name in participant_names:
                time.sleep(1)
                print(f"{name} responds to {previous_name}:")
                response = get_bot_response(
                    f"The topic is: {dialogue_topic}\n{previous_name} said: '{previous_statement}'\n\nRespond to {previous_name}'s perspective with your own viewpoint.",
                    participants[name],
                    name
                )
                print(response)
                print()
                
                previous_statement = response
                previous_name = name
    
    elif format_choice == 2:
        # One-on-one debate - alternating responses with structured format
        # This simulates a formal debate with clear turns and direct responses
        print("\n=== Debate Rounds ===\n")
        
        debater1 = participant_names[0]
        debater2 = participant_names[1]
        current_statement = statements[debater2]
        
        for round_num in range(rounds):
            print(f"--- Round {round_num + 1} ---\n")
            
            # First debater responds
            time.sleep(1)
            print(f"{debater1} responds:")
            response = get_bot_response(
                f"Respond to this statement on {dialogue_topic}: '{current_statement}'",
                participants[debater1],
                debater1
            )
            print(response)
            print()
            current_statement = response
            
            # Second debater responds
            time.sleep(1)
            print(f"{debater2} responds:")
            response = get_bot_response(
                f"Respond to this statement on {dialogue_topic}: '{current_statement}'",
                participants[debater2],
                debater2
            )
            print(response)
            print()
            current_statement = response
    
    else:  # format_choice == 3
        # Interview format - interviewer asks questions, interviewees respond
        # This simulates a talk show or interview panel with one host
        print("\n=== Interview Session ===\n")
        
        interviewer = participant_names[0]
        interviewees = participant_names[1:]
        
        # Opening question about the topic
        print(f"{interviewer} asks about {dialogue_topic}:")
        question = get_bot_response(
            f"As an interviewer, ask an insightful opening question about {dialogue_topic}",
            participants[interviewer],
            interviewer
        )
        print(question)
        print()
        
        # Each interviewee responds to the opening question
        for interviewee in interviewees:
            time.sleep(1)
            print(f"{interviewee} responds:")
            response = get_bot_response(
                f"You're being interviewed. The interviewer asked: '{question}' regarding {dialogue_topic}. Respond with your perspective.",
                participants[interviewee],
                interviewee
            )
            print(response)
            print()
        
        # Additional rounds of questions
        for round_num in range(1, rounds):
            time.sleep(1)
            print(f"--- Question {round_num + 1} ---\n")
            
            # Interviewer asks a follow-up question
            print(f"{interviewer} asks:")
            question = get_bot_response(
                f"Based on the previous responses about {dialogue_topic}, ask a follow-up question that explores a different angle or aspect of the topic.",
                participants[interviewer],
                interviewer
            )
            print(question)
            print()
            
            # Each interviewee responds to the new question
            for interviewee in interviewees:
                time.sleep(1)
                print(f"{interviewee} responds:")
                response = get_bot_response(
                    f"You're being interviewed. The interviewer asked: '{question}' regarding {dialogue_topic}. Respond with your perspective.",
                    participants[interviewee],
                    interviewee
                )
                print(response)
                print()
    
    # Closing statements (except for interview format which has a special closing)
    if format_choice != 3:
        print("=== Closing Statements ===\n")
        closing_statements = {}
        
        for name, perspective in participants.items():
            time.sleep(1)
            print(f"{name}'s closing remarks:")
            closing = get_bot_response(
                f"Give a brief closing statement summarizing your position on {dialogue_topic}",
                perspective,
                name
            )
            closing_statements[name] = closing
            print(closing)
            print()
    else:
        # Special closing for interview format
        print("=== Interview Wrap-up ===\n")
        closing_statements = {}
        
        # Interviewer provides a wrap-up
        time.sleep(1)
        print(f"{interviewer}'s wrap-up:")
        interviewer_closing = get_bot_response(
            f"Provide a thoughtful wrap-up to the interview about {dialogue_topic}, thanking your guests and highlighting key insights.",
            participants[interviewer],
            interviewer
        )
        closing_statements[interviewer] = interviewer_closing
        print(interviewer_closing)
        print()
        
        # Each interviewee gives a brief final thought
        for interviewee in interviewees:
            time.sleep(1)
            print(f"{interviewee}'s final thought:")
            closing = get_bot_response(
                f"The interview about {dialogue_topic} is ending. Share a brief, impactful final thought in 1-2 sentences.",
                participants[interviewee],
                interviewee
            )
            closing_statements[interviewee] = closing
            print(closing)
            print()
    
    # Moderator summary
    print("\n=== Summary ===\n")
    
    summary_prompt = f"Summarize the dialogue on '{dialogue_topic}' between the following participants:\n\n"
    
    for name, perspective in participants.items():
        summary_prompt += f"{name}'s perspective: {perspective}\n"
        if name in closing_statements:
            summary_prompt += f"{name}'s closing: {closing_statements[name]}\n\n"
    
    if format_choice == 1:
        summary_type = "panel discussion"
    elif format_choice == 2:
        summary_type = "debate"
    else:
        summary_type = "interview"
    
    summary_prompt += f"Provide a neutral, balanced summary of this {summary_type}, highlighting the key differences in their approaches and the strengths of each perspective."
    
    moderator = get_response(
        summary_prompt,
        system="You are a neutral, insightful moderator who can identify the merits of different viewpoints. Provide a balanced summary."
    )
    
    print(moderator)

# Run the dialogue simulator
if __name__ == "__main__":
    ai_persona_dialogue_simulator()
```

## Using the Simulator for Interviews

To use this simulator specifically for interview scenarios:

1. **Select Format #3 (Interview)** - This configures one persona to act as the interviewer and others as interviewees

2. **Choose the Interviewer** - Select the "Interviewer" persona (option #8) for best results, though any persona can serve as an interviewer

3. **Select Interviewees** - Choose which personas will be interviewed on the selected topic

4. **Set Number of Questions** - Determine how many rounds of questions the interviewer will ask

5. **Interview Structure:**
   - The interviewer begins with an opening question about the topic
   - Each interviewee responds from their unique perspective
   - The interviewer asks follow-up questions in subsequent rounds
   - The session concludes with a wrap-up from the interviewer and final thoughts from interviewees

This interview format is particularly useful for:
- Exploring multiple perspectives on controversial topics
- Demonstrating how different personality types respond to the same questions
- Simulating talk show or panel interview dynamics
- Teaching questioning techniques and response patterns

## Extension Ideas

- Add a feature for the user to join as an additional participant
- Create specialised formats for specific topics (ethics, technology, etc.)
- Implement a scoring system where users rate which perspective they found most compelling
- Add follow-up questions that challenge each persona's perspective
- Create a "change my mind" feature where personas try to persuade on a controversial topic
- Allow students to create their own custom persona profiles
- Add a feature to visualise the dialogue flow and connections between arguments
- Implement a fact-checker persona that evaluates claims made during discussions
- Create a mode where personas can switch perspectives mid-dialogue to show flexibility in thinking
- Add the ability to save transcripts for later analysis or comparison

---