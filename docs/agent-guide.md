# Agent Module Guide

The Agent module in AiLabKit provides a powerful way to create AI assistants that can use tools to accomplish tasks. This guide will help you understand how to use the Agent module effectively.

## What is an Agent?

An agent is an AI system that can:

1. **Reason** about a problem or question
2. **Decide** which tools (if any) it needs to use
3. **Act** by calling the appropriate tools
4. **Observe** the results
5. **Respond** to the user based on reasoning and observations

Unlike basic chat, an agent can interact with external tools to fetch information, perform calculations, or take actions in the world. This makes agents particularly useful for tasks that require combining reasoning with real-world interactions.

## Using the Agent CLI

The Agent module provides a command-line interface with several commands:

### Ask a question

```bash
ailabkit agent ask "What is 3 * 14?"
```

This runs the agent with a single question and returns the response.

### Interactive mode

```bash
ailabkit agent interactive
```

This starts an interactive session where you can have a conversation with the agent.

### Web interface

```bash
ailabkit agent web
```

This launches a web interface for the agent, accessible in your browser.

### List available tools

```bash
ailabkit agent tools
```

This lists all tools available to the agent.

## Built-in Agents and Tools

The Agent module comes with several built-in specialized agents:

### Calculator Agent

Mathematical tools for calculations and equation solving:

- **calc**: Basic calculator for arithmetic expressions
  - Example: `calc "2 * 3 + 4"`

- **advanced_calc**: Advanced calculator with math functions
  - Example: `advanced_calc "sqrt(16) + sin(pi/2)"`

- **solve_quadratic**: Solves quadratic equations
  - Example: `solve_quadratic "1" "2" "-3"` (solves x² + 2x - 3 = 0)

### Dictionary Agent

Language tools for word definitions and relationships:

- **define**: Looks up the definition of a word
  - Example: `define "happy"`

- **synonyms**: Finds synonyms for a word
  - Example: `synonyms "happy"`

- **antonyms**: Finds antonyms for a word
  - Example: `antonyms "happy"`

- **examples**: Shows example sentences using a word
  - Example: `examples "happy"`

### Converter Agent

Unit conversion tools for various measurements:

- **convert**: General-purpose unit converter
  - Example: `convert "10" "mi" "km"`

- **convert_length**: Converts between length units
  - Example: `convert_length "5" "ft" "m"`

- **convert_weight**: Converts between weight units
  - Example: `convert_weight "150" "lb" "kg"`

- **convert_temperature**: Converts between temperature units
  - Example: `convert_temperature "32" "f" "c"`

## Creating Custom Tools

You can extend the Agent with your own custom tools. Here's a simple example:

```python
from ailabkit.agent import register_tool

def random_number(min_val=0, max_val=100):
    """Generate a random number in the given range."""
    import random
    return random.randint(min_val, max_val)

# Register the tool with the agent
register_tool(
    "random", 
    "Generate a random number between min and max values",
    random_number
)
```

After registering, your custom tool will be available to the agent.

## Understanding ReAct Prompting

The Agent module uses a technique called ReAct (Reasoning + Acting) to guide the LLM's thought process. This involves a structured format:

1. **Question**: The user's original query
2. **Thought**: The agent's reasoning about the problem
3. **Action**: The tool the agent wants to use
4. **Action Input**: The input to provide to the tool
5. **Observation**: The output from the tool
6. **Final Answer**: The agent's response to the user

By following this chain of thought, the agent can tackle complex problems that require multiple steps of reasoning and tool use.

## Educational Applications

The Agent module is particularly useful for:

- **Teaching programming concepts**: Students can see how tools are used programmatically
- **Problem-solving demonstrations**: Show step-by-step reasoning and tool use
- **Data analysis projects**: Combine reasoning with computational tools
- **Workflow automation**: Demonstrate how AI can connect with various APIs and tools
- **Critical thinking exercises**: Analyze the agent's reasoning process

## Example Use Cases

Here are some examples of what you can do with the Agent module:

- Create a research assistant that can search for information and perform calculations
- Develop a data analyst that can process and interpret data
- Build a planning assistant that breaks down complex tasks
- Design a teaching assistant that explains concepts and checks work

## Next Steps

- Explore the [built-in tools](../reference/agent/tools.md) in more detail
- Try creating your own custom tools
- Experiment with different types of questions in the interactive mode
- Check out our [agent mini-projects](../mini-projects.md) for inspiration