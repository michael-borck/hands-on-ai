# Simple Calculator Agent

**Difficulty**: Beginner - A simple introduction to agent functionality
**Learning Focus**: Agents, Tool Use, ReAct Framework
**Module**: agent

This mini-project creates a simple calculator agent that can solve math problems using the ReAct framework. It demonstrates how to create and use tools with an agent.

## Project Overview

In this project, you'll create an agent that can:

1. Parse mathematical expressions
2. Break down complex calculations into steps
3. Use a calculator tool to solve sub-problems
4. Show its reasoning process

This is a great introduction to how agents work and how they can use tools to solve problems.

## Implementation

Start by importing the necessary modules:

```python
import ast
import operator
from hands_on_ai.agent import run_agent, register_tool

# Operators we allow in expressions
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def _eval_node(node):
    """Recursively evaluate a parsed arithmetic expression."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("unsupported expression")

# Define a calculator function
def calculator(expression):
    """Evaluate a mathematical expression safely (no eval)."""
    try:
        tree = ast.parse(expression, mode="eval")
        return f"Result: {_eval_node(tree.body)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Register the calculator tool
register_tool(
    "calculator", 
    "Evaluate a mathematical expression. Example: 2 + 2 * 10", 
    calculator
)
```

> ⚠️ **Why not just use `eval()`?** You may have seen calculators built with
> `eval(expression, {"__builtins__": {}}, {...})`. **Don't do this.** Emptying
> `__builtins__` is *not* a sandbox — a crafted string such as
> `().__class__.__bases__[0].__subclasses__()` can still reach the operating
> system and run arbitrary code. Because an *agent* feeds model-generated text
> straight into your tool, that's a real remote-code-execution risk. Parsing the
> expression with `ast` and walking only the nodes you allow (as above) is the
> safe approach — it's exactly what `hands-on-ai`'s built-in calculator tool does.

```python

# Create a function to run the agent
def solve_math_problem(question):
    """Solve a math problem using the agent."""
    print(f"Question: {question}")
    
    # Run the agent with the question
    response = run_agent(question, verbose=True)
    
    print("\nFinal Answer:")
    print(response)
    
    return response

# Example usage
if __name__ == "__main__":
    questions = [
        "What is 25 * 3?",
        "If I have 125 apples and give away 1/5 of them, how many do I have left?",
        "What is the square root of 144?",
        "What is 15% of 240?",
        "If a triangle has sides of length 3, 4, and 5, what is its area?"
    ]
    
    for q in questions:
        print("\n" + "="*50)
        solve_math_problem(q)
        print("="*50)
```

## How It Works

1. We define a `calculator` function that safely evaluates mathematical expressions.
2. We register this tool with the agent system using `register_tool`.
3. We create a `solve_math_problem` function that runs the agent with a question.
4. The agent breaks the problem down and decides when to call the calculator tool.
5. The agent returns a final answer based on its reasoning and the tool results.

> 💡 **ReAct vs. JSON, and small models.** `run_agent(..., format="auto")` (the
> default) picks a reasoning format based on the model. The *ReAct* style shown
> below (`Thought / Action / Observation`) reads nicely but needs a fairly
> capable model. For the small local models you'll often run on Ollama,
> `hands-on-ai` automatically routes to a more reliable **JSON** format instead —
> so the exact text you see may differ from the sample below. If a small model
> struggles, that's expected: try a larger model, or pass `format="json"`
> explicitly.

## Sample Output

With a capable model (ReAct format), you'll see output like:

```
==================================================
Question: What is 25 * 3?

Thought: I need to multiply 25 by 3. I can use the calculator tool for this.
Action: calculator
Action Input: 25 * 3
Observation: Result: 75

Final Answer: The result of 25 * 3 is 75.
==================================================
```

On a small local model the steps are the same, but the agent exchanges JSON
(`{"thought": ..., "tool": "calculator", "input": "25 * 3"}`) under the hood
rather than the `Thought/Action` text.

## Extensions and Variations

Here are some ways to extend this project:

1. **Add more mathematical functions**: Extend the calculator to handle more complex operations like logarithms, trigonometry, etc.

2. **Create a multi-step calculator**: Modify the agent to show intermediate steps for complex calculations.

3. **Add unit conversion**: Create a unit conversion tool and let the agent solve problems involving different units.

4. **Create a word problem solver**: Enhance the agent to parse word problems and solve them step-by-step.

5. **Add visualization**: Create a web interface that displays the agent's reasoning steps alongside the calculations.

## Educational Applications

This project can be used to:

- Teach how agents break down problems into steps
- Demonstrate the ReAct framework in practice
- Show how tools can extend an AI system's capabilities
- Help students understand mathematical problem-solving strategies

## Assessment Ideas

- Have students modify the calculator tool to handle additional operations
- Ask students to analyze the agent's reasoning for different types of problems
- Challenge students to create a word problem generator that the agent can solve
- Have students compare the agent's approach to their own problem-solving methods