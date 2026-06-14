# Educational Assistant

**Difficulty**: Advanced  
**Time**: 120 minutes  
**Learning Focus**: Planning, educational content creation, tool orchestration  
**Module**: agent

## Overview
Create a comprehensive educational assistant that helps students learn a specific topic by providing explanations, examples, practice problems, and personalized feedback.

> ⚙️ **Small local models have limits.** This project chains several reasoning or
> tool-use steps. Small models (the kind you often run locally on Ollama) can be
> unreliable at multi-step reasoning — expect occasional wrong turns or dropped
> steps. If results are poor, try a larger/more capable model. Note that the
> library routes small models to JSON tool-calling rather than the ReAct format.

## Instructions
1. Choose an educational topic that can leverage multiple agent tools (e.g., chemistry, mathematics, language learning)
2. Design a learning plan with these components:
   - A diagnostic assessment to identify what the student already knows
   - Explanations of key concepts with relevant examples
   - Interactive practice problems of varying difficulty
   - A final assessment to measure learning progress
3. Implement your plan by creating specific prompts for the agent
4. Test your educational assistant with at least 3 different scenarios:
   - A beginner with no prior knowledge
   - An intermediate learner who needs to fill knowledge gaps
   - An advanced student looking for challenging applications
5. Document how the agent adapts to different learning needs and which tools are most useful for educational purposes

## Extension Ideas
- Create a spaced repetition system that uses the agent to generate review questions
- Develop a project-based learning module where the agent guides students through a complex problem
- Design a collaborative learning activity where multiple students interact with the agent together