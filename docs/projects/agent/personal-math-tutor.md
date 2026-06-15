# Personal Math Tutor

**Difficulty**: Beginner  
**Time**: 30 minutes  
**Learning Focus**: Basic agent interaction, calculator tools  
**Module**: agent

## Overview
Create a math tutor agent that helps solve arithmetic problems and explains the steps involved.

> ⚙️ **Small local models have limits.** This project chains several reasoning or
> tool-use steps. Small models (the kind you often run locally on Ollama) can be
> unreliable at multi-step reasoning: expect occasional wrong turns or dropped
> steps. If results are poor, try a larger/more capable model. Note that the
> library routes small models to JSON tool-calling rather than the ReAct format.

## Instructions
1. Start the agent in interactive mode using `hands-on-ai agent interactive`
2. Ask the agent to solve basic math problems like "What is 24 × 7?" or "Calculate 125 ÷ 5"
3. For each problem, ask the agent to explain its reasoning step by step
4. Try more complex problems like "If I have 3 boxes with 12 items each, and I add 7 more items, how many do I have total?"
5. Observe how the agent uses the calculator tools to solve these problems
6. Create a list of 5 progressively harder math problems that demonstrate the agent's capabilities

## Extension Ideas
- Ask the agent to solve algebraic equations like "If 2x + 7 = 15, what is x?"
- Challenge the agent with word problems that require multiple calculation steps
- Compare the agent's approach with how you would solve the same problems