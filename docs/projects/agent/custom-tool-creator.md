# Custom Tool Creator

**Difficulty**: Advanced  
**Time**: 75 minutes  
**Learning Focus**: Custom tool development, Python coding  
**Module**: agent

## Overview
Design and implement your own custom tools to extend the agent's capabilities for specialized tasks.

## Instructions
1. Read the [Build Your Own Tool (Cookbook)](build-your-own-tool.md) first — it
   covers the tool contract (`str -> str`), how to register a tool, and the
   fetch → parse → return pattern for tools that call an API
2. Create a Python file to define your custom tools (e.g., `my_tools.py`)
3. Implement at least 2 of the following custom tools:
   - A random quote generator that returns an inspirational quote
   - A tool that generates a strong password of a specified length
   - A simple game like rock-paper-scissors or number guessing
   - A tool that provides current weather information for a given location
4. Register your tools using the `register_tool` function
5. Test your tools by asking the agent to use them in various scenarios
6. Document how the agent integrates your custom tools with its existing capabilities

## Extension Ideas
- Create a tool that connects to an external API (like weather, news, or sports data)
- Design a tool that performs a specialized calculation relevant to your field of study
- Implement a tool that works with files (e.g., reading CSV data or creating simple charts)