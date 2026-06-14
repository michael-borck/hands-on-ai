# Science Explorer

**Difficulty**: Intermediate  
**Time**: 45 minutes  
**Learning Focus**: Educational tools, multi-tool queries  
**Module**: agent

## Overview
Use the agent as a science learning companion to explore elements, mathematical properties, and scientific concepts.

> ⚙️ **Small local models have limits.** This project chains several reasoning or
> tool-use steps. Small models (the kind you often run locally on Ollama) can be
> unreliable at multi-step reasoning — expect occasional wrong turns or dropped
> steps. If results are poor, try a larger/more capable model. Note that the
> library routes small models to JSON tool-calling rather than the ReAct format.

## Instructions
1. Launch the agent using `hands-on-ai agent interactive`
2. Explore the periodic table tool by asking about different elements:
   - "Tell me about oxygen"
   - "What's the atomic number of gold?"
   - "Compare the properties of sodium and potassium"
3. Use the prime check tool to investigate number properties:
   - "Is 97 a prime number?"
   - "What are the factors of 144?"
4. Combine tools by asking questions that require multiple lookups:
   - "What's the sum of the atomic numbers of iron and calcium?"
   - "If I have a sample with 12 atoms of carbon and 18 atoms of oxygen, what's the ratio?"
5. Create a mini science quiz with 5 questions that the agent can help answer

## Extension Ideas
- Design a chemistry experiment and ask the agent to help with calculations
- Create a periodic table scavenger hunt with clues about element properties
- Compare how the agent answers science questions with and without using tools