"""
Tests for the agent engine: core.py (ReAct loop) and formats.py (JSON parsing
and the JSON fallback agent).

The LLM is mocked throughout (no network), following the pattern in
test_workflow.py. core.py imports get_response into its own namespace, so we
patch it there; the JSON fallback does `from ..chat import get_response` at call
time, so we patch the attribute on the chat package.
"""

import pytest

import hands_on_ai.chat as chat_pkg
import hands_on_ai.agent.core as core_mod
from hands_on_ai.agent.core import (
    register_tool,
    list_tools,
    _parse_tool_calls,
    _execute_tool_call,
    run_agent,
)
from hands_on_ai.agent.formats import (
    parse_json_response,
    format_tools_for_json_prompt,
    run_json_agent_fallback,
)


@pytest.fixture
def clean_tools():
    """Isolate the global tool registry so tests don't leak into each other."""
    saved = dict(core_mod._tools)
    core_mod._tools.clear()
    yield
    core_mod._tools.clear()
    core_mod._tools.update(saved)


def _fake_responses(responses):
    """A fake get_response that returns each queued reply in turn."""
    it = iter(responses)

    def fake(prompt=None, model=None, system=None, **kwargs):
        return next(it)

    return fake


# --- core.py: registry + parsing helpers ----------------------------------

def test_register_and_list_tools(clean_tools):
    register_tool("echo", "Echo the input", lambda x: x)
    assert {"name": "echo", "description": "Echo the input"} in list_tools()


def test_parse_tool_calls():
    text = "Thought: I should calculate\nAction: calc\nAction Input: 2 + 2"
    assert _parse_tool_calls(text) == [("calc", "2 + 2")]
    assert _parse_tool_calls("Just a thought, no action here.") == []


def test_execute_tool_call(clean_tools):
    register_tool("echo", "Echo", lambda x: f"got {x}")
    assert _execute_tool_call("echo", "hi") == "got hi"
    assert "not found" in _execute_tool_call("missing", "x")
    register_tool("boom", "Boom", lambda x: 1 / 0)
    assert "Error executing tool 'boom'" in _execute_tool_call("boom", "x")


# --- core.py: the ReAct loop ----------------------------------------------

def test_run_agent_returns_final_answer(clean_tools, monkeypatch):
    monkeypatch.setattr(core_mod, "get_response", _fake_responses(["Final Answer: 42"]))
    assert run_agent("What is 6*7?", model="test-model", format="react") == "42"


def test_run_agent_tool_call_then_final_answer(clean_tools, monkeypatch):
    register_tool("echo", "Echo the input back", lambda x: x.upper())
    responses = [
        "Thought: I'll use echo\nAction: echo\nAction Input: hello",
        "Final Answer: done",
    ]
    monkeypatch.setattr(core_mod, "get_response", _fake_responses(responses))
    assert run_agent("say hello", model="test-model", format="react") == "done"


def test_run_agent_direct_response_when_no_tools(clean_tools, monkeypatch):
    # No Action and no "Final Answer:" -> the response is returned as-is.
    monkeypatch.setattr(core_mod, "get_response", _fake_responses(["Here is a plain answer."]))
    assert run_agent("hi", model="test-model", format="react") == "Here is a plain answer."


# --- formats.py: JSON parsing ---------------------------------------------

def test_parse_json_response_code_block():
    data = parse_json_response('```json\n{"thought": "t", "answer": "42"}\n```')
    assert data["answer"] == "42"


def test_parse_json_response_bare_object():
    data = parse_json_response('Sure! {"tool": "calc", "input": "2+2"}')
    assert data["tool"] == "calc"
    assert data["input"] == "2+2"


def test_parse_json_response_recovers_unquoted_keys():
    # Invalid JSON (unquoted keys) should be repaired by the fallback regex.
    data = parse_json_response('{thought: "hi", answer: "yo"}')
    assert data["answer"] == "yo"


def test_parse_json_response_complete_failure():
    data = parse_json_response("there is no json here at all")
    assert "error" in data
    assert "text" in data


def test_format_tools_for_json_prompt():
    assert format_tools_for_json_prompt({}) == "No tools are available."
    out = format_tools_for_json_prompt({"calc": {"description": "do math"}})
    assert "- calc: do math" in out


# --- formats.py: the JSON fallback agent -----------------------------------

def test_json_fallback_returns_answer(monkeypatch):
    def fake(prompt=None, system=None, model=None, **kwargs):
        return '{"thought": "done", "answer": "the answer is 42"}'

    monkeypatch.setattr(chat_pkg, "get_response", fake)
    assert run_json_agent_fallback("q", {}, model="test-model") == "the answer is 42"


def test_json_fallback_tool_call_then_answer(monkeypatch):
    replies = iter([
        '{"thought": "use echo", "tool": "echo", "input": "hi"}',
        '{"thought": "now answer", "answer": "HELLO"}',
    ])

    def fake(prompt=None, system=None, model=None, **kwargs):
        return next(replies)

    monkeypatch.setattr(chat_pkg, "get_response", fake)
    tools = {"echo": {"description": "echo", "function": lambda x: x.upper()}}
    assert run_json_agent_fallback("q", tools, model="test-model") == "HELLO"


def test_json_fallback_unknown_tool_then_answer(monkeypatch):
    replies = iter([
        '{"thought": "try a tool", "tool": "nope", "input": "x"}',
        '{"thought": "answer instead", "answer": "recovered"}',
    ])

    def fake(prompt=None, system=None, model=None, **kwargs):
        return next(replies)

    monkeypatch.setattr(chat_pkg, "get_response", fake)
    # Unknown tool -> error added to history, loop continues, then answers.
    assert run_json_agent_fallback("q", {}, model="test-model") == "recovered"
