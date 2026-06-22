"""
Agent format handlers for different types of model responses.
"""

import re
import json
from typing import Dict, Any
from ..config import log

# JSON prompt template
JSON_SYSTEM_PROMPT = """You are an intelligent agent that can analyze questions and call tools.

AVAILABLE TOOLS:
{tool_list}

To call a tool, respond with VALID JSON in this format:
```json
{{
  "thought": "Your reasoning about what tool to use",
  "tool": "tool_name",
  "input": "parameter for the tool"
}}
```

If you don't need to call a tool, or after you've gathered all necessary information, respond with:
```json
{{
  "thought": "Your reasoning about the answer",
  "answer": "Your final answer to the user's question"
}}
```

IMPORTANT: 
1. Your response MUST be valid JSON wrapped in ```json and ``` markers
2. Use ONLY the exact tool names provided above
3. Only call tools that are relevant to the user's question
4. Think step by step about what information you need to answer the question

EXAMPLE:
User: What's the weather like in Chicago and should I bring an umbrella?

Your response:
```json
{{
  "thought": "I need to check the current weather in Chicago",
  "tool": "weather_data",
  "input": "Chicago"
}}
```

After receiving tool results:
```json
{{
  "thought": "I should check if there's a chance of rain",
  "tool": "rain_chance_graph",
  "input": "Chicago"
}}
```

After receiving all needed information:
```json
{{
  "thought": "Now I have all the information I need",
  "answer": "The weather in Chicago is sunny and 25°C. There's only a 20% chance of rain, but you might want to bring a small umbrella just in case."
}}
```
"""

def parse_json_response(text: str) -> Dict[str, Any]:
    """
    Parse a JSON response from the model.
    
    Args:
        text: Response text from the model
        
    Returns:
        Dict with parsed JSON data or error information
    """
    # Extract JSON from the response (if wrapped in code blocks)
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    
    if json_match:
        json_text = json_match.group(1)
    else:
        # Try to find anything that looks like JSON object (starts with { and ends with })
        json_pattern = r"\s*({.*})\s*"
        object_match = re.search(json_pattern, text, re.DOTALL)
        
        if object_match:
            json_text = object_match.group(1)
        else:
            # Fallback to using the whole text
            json_text = text
    
    try:
        # Parse the JSON response
        parsed: Dict[str, Any] = json.loads(json_text)
        return parsed
    except json.JSONDecodeError as e:
        log.warning(f"Failed to parse JSON from model response: {e}")
        
        # Try to fix common JSON errors
        try:
            # Try to fix missing quotes around keys
            fixed_json = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', json_text)
            parsed = json.loads(fixed_json)
            return parsed
        except json.JSONDecodeError:
            pass
            
        try:
            # Try to fix missing commas between elements
            fixed_json = re.sub(r'(\s*"\w+"\s*:\s*"[^"]*")\s*(")', r'\1,\2', json_text)
            parsed = json.loads(fixed_json)
            return parsed
        except json.JSONDecodeError:
            pass
        
        # If all attempts fail, extract anything useful from the response
        # Look for thought patterns
        thought_match = re.search(r'"?thought"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        answer_match = re.search(r'"?answer"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        tool_match = re.search(r'"?tool"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        input_match = re.search(r'"?input"?\s*:\s*"([^"]*)"', text, re.IGNORECASE)
        
        result = {"error": str(e)}
        
        if thought_match:
            result["thought"] = thought_match.group(1)
        if answer_match:
            result["answer"] = answer_match.group(1)
        if tool_match and input_match:
            result["tool"] = tool_match.group(1)
            result["input"] = input_match.group(1)
        
        # If we've extracted something useful, return it
        if len(result) > 1:
            log.info("Extracted partial JSON data using regex fallbacks")
            return result
            
        # Complete failure, return the error with the text
        return {"error": str(e), "text": text}

def format_tools_for_json_prompt(tools: Dict[str, Dict[str, Any]]) -> str:
    """
    Format tools list for inclusion in JSON prompt.
    
    Args:
        tools: Dictionary of tool information
        
    Returns:
        str: Formatted tool list for the prompt
    """
    if not tools:
        return "No tools are available."
    
    tool_texts = []
    for name, info in tools.items():
        tool_texts.append(f"- {name}: {info['description']}")
    
    return "\n".join(tool_texts)

def run_instructor_agent(
    prompt: str, 
    tools: Dict[str, Dict[str, Any]], 
    model: str | None = None,
    max_iterations: int = 5,
    verbose: bool = False
) -> str:
    """
    Run an agent using Instructor for robust structured outputs.
    
    This replaces the fragile JSON parsing with Pydantic validation
    while maintaining the same educational interface.
    
    Args:
        prompt: User question
        tools: Dictionary of tools
        model: LLM model to use
        max_iterations: Maximum number of tool calls
        verbose: Whether to print intermediate steps
        
    Returns:
        str: Final agent response
    """
    try:
        import instructor
        from openai import OpenAI
        from .schemas import AgentResponse, ToolCall, FinalAnswer
        from ..config import get_server_url, get_api_key
    except ImportError as e:
        # Fallback to old implementation if dependencies not available
        log.warning(f"Instructor not available, falling back to basic JSON: {e}")
        return run_json_agent_fallback(prompt, tools, model, max_iterations, verbose)
    
    # Create instructor client with OpenAI-compatible endpoints
    try:
        server_url = get_server_url()
        # Add /v1 suffix for OpenAI-compatible endpoints
        if not server_url.endswith('/v1'):
            server_url = server_url.rstrip('/') + '/v1'
            
        client = instructor.from_openai(
            OpenAI(
                base_url=server_url,
                api_key=get_api_key() or "ollama"
            ),
            mode=instructor.Mode.JSON_SCHEMA  # Use JSON_SCHEMA for Ollama models
        )
    except Exception as e:
        log.warning(f"Failed to initialize Instructor client: {e}")
        return run_json_agent_fallback(prompt, tools, model, max_iterations, verbose)
    
    # Create more specific system prompt for JSON_SCHEMA mode
    system_prompt = f"""You are an intelligent agent that can analyze questions and call tools.

AVAILABLE TOOLS:
{format_tools_for_json_prompt(tools)}

You must respond with valid JSON in one of these two formats:

TO CALL A TOOL:
{{
  "thought": "Your reasoning about what tool to use",
  "tool": "exact_tool_name",
  "input": "parameter for the tool"
}}

TO PROVIDE FINAL ANSWER:
{{
  "thought": "Your reasoning about the answer", 
  "answer": "Your final answer to the user's question"
}}

IMPORTANT:
- Use exact tool names from the list above
- Provide clear reasoning in the "thought" field
- Only call tools that are relevant to the question
- After using tools, provide a final answer with your conclusion"""
    
    # Initialize conversation state
    conversation_history = [prompt]
    
    # Main agent loop with Instructor validation
    for iteration in range(max_iterations):
        try:
            # Determine what type of response we expect based on conversation state
            if any("Now provide your final answer" in msg for msg in conversation_history[-2:]):
                # After tool execution - expect final answer
                # Either a single model class or a Union of them; instructor
                # accepts both as its response_model, so we keep this dynamic.
                expected_model: Any = FinalAnswer
                if verbose:
                    log.info("Expecting FinalAnswer after tool use")
            else:
                # First iteration or continuing conversation - could be either
                expected_model = AgentResponse
            
            # Use Instructor with JSON_SCHEMA mode
            response = client.chat.completions.create(
                model=model,
                response_model=expected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "\n".join(conversation_history)}
                ]
            )
            
            if verbose:
                log.info(f"Instructor response (iteration {iteration+1}): {response}")
            
            # Handle based on response type (automatic validation!)
            if isinstance(response, FinalAnswer):
                if verbose:
                    log.info(f"Final answer reached: {response.answer}")
                return response.answer
            
            elif isinstance(response, ToolCall):
                # Validate tool exists
                if response.tool not in tools:
                    error_msg = f"Error: Tool '{response.tool}' not found. Available tools: {', '.join(tools.keys())}"
                    if verbose:
                        log.warning(error_msg)
                    conversation_history.append(error_msg)
                    continue
                
                # Execute tool with error handling
                try:
                    tool_result = tools[response.tool]["function"](response.input)
                    if verbose:
                        log.info(f"Tool '{response.tool}' executed successfully: {tool_result}")
                    
                    # Add the tool result to the conversation with instruction for final answer
                    conversation_history.append(f"Tool result: {tool_result}")
                    conversation_history.append("Now provide your final answer based on the tool result.")
                    
                except Exception as e:
                    error_msg = f"Error executing tool '{response.tool}': {str(e)}"
                    if verbose:
                        log.exception(f"Tool execution failed for {response.tool}")
                    conversation_history.append(error_msg)
            
            else:
                # This shouldn't happen with proper Pydantic validation
                if verbose:
                    log.warning(f"Unexpected response type: {type(response)}")
                conversation_history.append(
                    "I need to provide either a tool call or a final answer. Let me try again."
                )
                
        except Exception as e:
            # Instructor handles retries automatically, but if it fails completely
            if verbose:
                log.warning(f"Instructor failed after retries (iteration {iteration+1}): {e}")
            
            # Try to continue with an error message
            conversation_history.append(
                f"I encountered an error: {str(e)}. Let me try a different approach."
            )
            continue
    
    # If we reach max iterations without a final answer
    return "I've reached the maximum number of steps without finding a complete answer."


def run_json_agent_fallback(
    prompt: str, 
    tools: Dict[str, Dict[str, Any]], 
    model: str | None = None,
    max_iterations: int = 5,
    verbose: bool = False
) -> str:
    """
    Fallback to the original JSON agent implementation.
    
    This maintains backward compatibility if Instructor is not available.
    """
    from ..chat import get_response
    
    # Format the system prompt with tools
    system_prompt = JSON_SYSTEM_PROMPT.format(
        tool_list=format_tools_for_json_prompt(tools)
    )
    
    # Initialize conversation state
    conversation_history = [prompt]
    
    # Main agent loop (original implementation)
    for iteration in range(max_iterations):
        # Get the response from the LLM
        llm_response = get_response(
            prompt="\n".join(conversation_history),
            system=system_prompt,
            model=model
        )
        
        if verbose:
            log.info(f"LLM Response (iteration {iteration+1}):\n{llm_response}")
        
        # Parse the JSON response
        response_data = parse_json_response(llm_response)
        
        # Check if parsing failed completely
        if "error" in response_data and len(response_data) == 2 and "text" in response_data:
            # Completely failed to parse anything useful
            error_message = f"Error parsing response: {response_data['error']}"
            if verbose:
                log.warning(error_message)
            
            # Add the error to the conversation and ask for a proper JSON response
            conversation_history.append(
                error_message + "\nPlease provide a valid JSON response following the format in the instructions."
            )
            continue
        
        # Check if we have a final answer
        if "answer" in response_data:
            return str(response_data["answer"])
        
        # Check if we need to call a tool
        if "tool" in response_data and "input" in response_data:
            tool_name = response_data["tool"]
            tool_input = response_data["input"]
            
            # Check if the tool exists
            if tool_name not in tools:
                error_message = f"Error: Tool '{tool_name}' not found. Available tools: {', '.join(tools.keys())}"
                if verbose:
                    log.warning(error_message)
                conversation_history.append(error_message)
                continue
            
            # Call the tool
            try:
                tool_result = tools[tool_name]["function"](tool_input)
                if verbose:
                    log.info(f"Tool result: {tool_result}")
                
                # Add the tool result to the conversation
                conversation_history.append(f"Tool result: {tool_result}")
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {str(e)}"
                if verbose:
                    log.exception(f"Error executing tool {tool_name}")
                conversation_history.append(error_message)
        else:
            # No tool call or answer, see if we can extract something useful
            if "thought" in response_data:
                return f"No clear answer, but here's what I was thinking: {response_data['thought']}"
            else:
                # Try one more time with a clearer instruction
                conversation_history.append(
                    "I need a valid JSON response. Please provide either a tool call or a final answer."
                )
                continue
    
    # If we reach max iterations without a final answer
    return "I've reached the maximum number of steps without finding a complete answer."


# Keep the original function name for backward compatibility
def run_json_agent(
    prompt: str, 
    tools: Dict[str, Dict[str, Any]], 
    model: str | None = None,
    max_iterations: int = 5,
    verbose: bool = False
) -> str:
    """
    Main entry point for JSON-based agent.
    
    Tries Instructor first, falls back to original implementation.
    """
    return run_instructor_agent(prompt, tools, model, max_iterations, verbose)