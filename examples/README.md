# Hands-On AI Examples

This directory contains example scripts that demonstrate how to use the Hands-On AI package. These examples show different features and use cases to help you get started with the library.

## Basic Examples

- **`smoke_test.py`**: End-to-end checklist that exercises chat, streaming, memory, caching, evaluation, and RAG against your configured provider. Prints PASS/FAIL and exits non-zero on any failure, so it is handy after upgrades or before a release.
- **`simple_weather_agent_test.py`**: A basic example showing how to create an agent with weather-related tools
- **`test_agent.py`**: Demonstrates the agent functionality with multiple tools and format detection
- **`weather_graph_agent_example.py`**: Shows how to use graph-generating tools with the agent

## Advanced Examples

- **`debug_agent_prompt.py`**: Helps debug issues with agent prompts and tool calling
- **`debug_json_agent.py`**: Demonstrates the JSON-based agent format for debugging
- **`enhanced_test_agent.py`**: Shows enhanced agent capabilities with multiple formats
- **`json_agent.py`**: Example implementation of a pure JSON-based agent
- **`multi_format_agent_test.py`**: Tests both ReAct and JSON formats with various models

## Running the Examples

You can run any example script directly from this directory:

```bash
python examples/test_agent.py
```

Make sure you have Ollama running and appropriate models installed before running the examples.

## Using These Examples

These examples are meant to serve as learning resources and starting points for your own applications. Feel free to:

1. Study the code to understand how different features work
2. Copy and modify them for your specific needs
3. Use them as templates for your own projects

Each example includes comments explaining what it does and how it works.