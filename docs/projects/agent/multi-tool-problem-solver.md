# Multi-Tool Problem Solver

**Difficulty**: Intermediate  
**Time**: 60 minutes  
**Learning Focus**: Tool combinations, complex problem-solving  
**Module**: agent

## Overview
Challenge the agent to solve complex problems that require using multiple tools together in creative ways.

> ⚙️ **Small local models have limits.** This project chains several reasoning or
> tool-use steps. Small models (the kind you often run locally on Ollama) can be
> unreliable at multi-step reasoning — expect occasional wrong turns or dropped
> steps. If results are poor, try a larger/more capable model. Note that the
> library routes small models to JSON tool-calling rather than the ReAct format.

## Instructions
1. Launch the agent using `hands-on-ai agent interactive`
2. Create 3 multi-step problems that each require at least 2 different tools. For example:
   - "If I drive 65 miles at 55 mph, then walk 3 kilometers, how many minutes will my journey take in total?"
   - "I need to mix a solution that's 35% acid. If I have 200ml of 50% acid solution, how much water should I add?"
   - "A recipe needs 2 cups of flour for 12 cookies. If I want to make 30 cookies but measure in grams, how much flour do I need?"
3. For each problem, ask the agent to explain its reasoning step by step
4. Identify which tools were used to solve each problem
5. Document any creative or unexpected approaches the agent took

## Extension Ideas
- Create a scavenger hunt with clues that require different tools to solve
- Design a multi-stage problem where each answer leads to the next question
- Challenge the agent with a problem where the most obvious tool isn't the best approach