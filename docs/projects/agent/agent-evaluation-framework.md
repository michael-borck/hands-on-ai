# Agent Evaluation Framework

**Difficulty**: Advanced  
**Time**: 90 minutes  
**Learning Focus**: Critical analysis, agent limitations, structured evaluation  
**Module**: agent

## Overview
Develop a framework to evaluate the agent's performance across different types of tasks and identify its strengths and limitations.

> ⚙️ **Small local models have limits.** This project chains several reasoning or
> tool-use steps. Small models (the kind you often run locally on Ollama) can be
> unreliable at multi-step reasoning: expect occasional wrong turns or dropped
> steps. If results are poor, try a larger/more capable model. Note that the
> library routes small models to JSON tool-calling rather than the ReAct format.

## Instructions
1. Design a test suite with 3-5 questions in each of these categories:
   - Factual (using educational tools)
   - Computational (using calculator tools)
   - Analytical (requiring multiple reasoning steps)
   - Creative (open-ended tasks)
2. For each question, define what an ideal answer would include
3. Run the agent through your test suite and score its responses
4. Analyze the results to identify patterns in the agent's performance:
   - Which types of questions does it handle well?
   - Where does it struggle or make mistakes?
   - How clear is its reasoning process?
5. Write a brief report summarizing your findings and recommendations for effective agent use

## Extension Ideas
- Compare the agent's performance with and without access to specific tools
- Test edge cases and ambiguous questions to see how the agent handles uncertainty
- Design prompts that intentionally challenge the agent's reasoning capabilities