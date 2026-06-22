"""
Core agent functionality for ReAct-style reasoning and tool use.
"""

import re
from typing import Dict, List, Callable, Any, Optional, Tuple
from ..config import get_model, log
from ..chat.get_response import get_response
from ..models import detect_best_format
from .prompts import SYSTEM_PROMPT, TOOL_DESCRIPTION_FORMAT, TOOL_RESULT_FORMAT
from .formats import run_json_agent

# Global tool registry
_tools: Dict[str, Dict[str, Any]] = {}


def register_tool(name: str, description: str, function: Callable) -> None:
    """
    Register a tool with the agent.
    
    Args:
        name: Tool name
        description: Tool description
        function: Tool function
    """
    _tools[name] = {
        "name": name,
        "description": description,
        "function": function
    }
    log.debug(f"Registered tool: {name}")


def list_tools() -> list[dict[str, str]]:
    """
    List all registered tools.
    
    Returns:
        list: List of tool information dictionaries
    """
    return [
        {"name": info["name"], "description": info["description"]}
        for info in _tools.values()
    ]


def _format_tools_for_prompt():
    """Format tools list for inclusion in prompt."""
    if not _tools:
        return "No tools are available."
    
    tool_texts = []
    for name, info in _tools.items():
        tool_texts.append(f"- {name}: {info['description']}")
    
    return TOOL_DESCRIPTION_FORMAT.format(tool_list="\n".join(tool_texts))


def _parse_tool_calls(text: str) -> List[Tuple[str, str]]:
    """
    Parse tool calls from text using ReAct format.
    
    Args:
        text: The model's response text
        
    Returns:
        List of tuples with (tool_name, tool_input)
    """
    # Match action and action input patterns from ReAct format
    action_pattern = r"Action: *(.*?)$"
    action_input_pattern = r"Action Input: *(.*?)$"
    
    # Find all instances
    actions = re.findall(action_pattern, text, re.MULTILINE)
    inputs = re.findall(action_input_pattern, text, re.MULTILINE)
    
    # Ensure we have matching pairs
    tool_calls = []
    for i in range(min(len(actions), len(inputs))):
        tool_name = actions[i].strip()
        tool_input = inputs[i].strip()
        if tool_name and tool_input:
            tool_calls.append((tool_name, tool_input))
    
    return tool_calls


def _execute_tool_call(tool_name: str, tool_input: str) -> str:
    """
    Execute a parsed tool call with proper error handling.
    
    Args:
        tool_name: Name of the tool to execute
        tool_input: String input for the tool
        
    Returns:
        str: Result of tool execution or error message
    """
    if tool_name not in _tools:
        return f"Error: Tool '{tool_name}' not found."
    
    try:
        # For simple tools, we can just pass the input string directly
        result = _tools[tool_name]["function"](tool_input)
        return str(result)
    except Exception as e:
        log.exception(f"Error executing tool {tool_name}")
        return f"Error executing tool '{tool_name}': {str(e)}"


def run_agent(
    prompt: str, 
    model: Optional[str] = None, 
    format: str = "auto",
    max_iterations: int = 5, 
    verbose: bool = False
) -> str:
    """
    Run the agent with the given prompt.
    
    Args:
        prompt: User question or instruction
        model: LLM model to use, defaults to configured model
        format: Format to use ("react", "json", or "auto")
        max_iterations: Maximum number of tool use iterations
        verbose: Whether to print intermediate steps
        
    Returns:
        str: Final agent response
    """
    # Get model from config if not specified
    if model is None:
        model = get_model()
    
    # Determine which format to use if set to auto
    if format == "auto":
        format = detect_best_format(model)
        
    if verbose:
        log.info(f"Using {format} format for model {model}")
    
    # Use JSON format for smaller models
    if format == "json":
        return run_json_agent(prompt, _tools, model, max_iterations, verbose)
    
    # Otherwise use the original ReAct format
    return _run_react_agent(prompt, model, max_iterations, verbose)


def _run_react_agent(
    prompt: str, 
    model: Optional[str] = None,
    max_iterations: int = 5, 
    verbose: bool = False
) -> str:
    """
    Run the agent with the given prompt using ReAct format.
    
    Args:
        prompt: User question or instruction
        model: LLM model to use, defaults to configured model
        max_iterations: Maximum number of tool use iterations
        verbose: Whether to print intermediate steps
        
    Returns:
        str: Final agent response
    """
    # Prepare system prompt with tools
    system_prompt = SYSTEM_PROMPT.format(
        tool_descriptions=_format_tools_for_prompt()
    )
    
    # Initialize conversation with the user query
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {prompt}"}
    ]
    
    # To store the full response with reasoning and tool usage
    full_trace = [f"Question: {prompt}"]
    
    for i in range(max_iterations):
        # Get model response
        # Convert messages to a single prompt for get_response
        system_message = messages[0]["content"]
        full_prompt = "\n\n".join([msg["content"] for msg in messages[1:]])
        response = get_response(
            prompt=full_prompt,
            model=model,
            system=system_message
        )
        
        if verbose:
            log.info(f"Model response: {response}")
        full_trace.append(response)
        
        # Check for tool calls
        tool_calls = _parse_tool_calls(response)
        
        # Check if we've reached a final answer
        if "Final Answer:" in response:
            # Extract the final answer
            final_answer = re.search(r"Final Answer: *(.*?)($|Thought:)", response + "Thought:", re.DOTALL)
            if final_answer:
                return final_answer.group(1).strip()
            # Fallback to returning the whole response if pattern doesn't match
            return response
        
        if not tool_calls:
            # No tools used but also no final answer - interpret as direct response
            return response
        
        # Execute tools and add results to the conversation
        for tool_name, tool_input in tool_calls:
            tool_result = _execute_tool_call(tool_name, tool_input)
            
            # Format tool result in the observation format
            observation = TOOL_RESULT_FORMAT.format(result=tool_result)
            full_trace.append(observation)
            
            # Add the observation to the conversation
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": observation})
    
    # If we reach max iterations without a final answer
    if verbose:
        log.warning(f"Reached maximum iterations ({max_iterations}) without finding a final answer")
    
    # Try to extract any partial answer
    final_thoughts = re.search(r"Thought: *(.*?)($|Action:|Final Answer:)", response, re.DOTALL)
    if final_thoughts:
        return f"I've been working on this but haven't reached a final answer. Here's what I know so far: {final_thoughts.group(1).strip()}"
    
    # Fallback to a generic message
    return "I've reached the maximum number of tool calls without finding a complete answer."