"""
Core response functionality for the chat module.
"""

import random
import time
from collections.abc import Iterator
from typing import Literal, overload
from openai import OpenAI, Stream
from ..config import get_server_url, get_api_key, load_fallbacks, log

# Global model cache
_last_model: str | None = None
# Load fallbacks from the chat module
_fallbacks = load_fallbacks(module="chat")

# When True, chat_completion prints streamed chunks to stdout as they arrive.
# Used by the interactive REPL so personality bots stream token-by-token. Off by
# default so library/notebook use is unaffected.
_print_stream = False


def set_stream_printing(enabled: bool = True):
    """Enable or disable live token printing to stdout (used by the chat REPL)."""
    global _print_stream
    _print_stream = enabled


# Token usage from the most recent completion (or None). Lets the CLI show usage
# even when the call went through a personality bot.
_last_usage = None


def get_last_usage():
    """Return token usage from the most recent get_response/bot call (or None)."""
    return _last_usage


def _build_client() -> OpenAI:
    """Create an OpenAI-compatible client pointed at the configured server."""
    server_url = get_server_url()
    # Add /v1 suffix for OpenAI-compatible endpoints
    if not server_url.endswith("/v1"):
        server_url = server_url.rstrip("/") + "/v1"
    log.debug(f"Using OpenAI-compatible server URL: {server_url}")
    return OpenAI(base_url=server_url, api_key=get_api_key() or "hands-on-ai")


def _usage_dict(response):
    """Extract token usage from a completion response as a plain dict (or None)."""
    usage = getattr(response, "usage", None)
    if not usage:
        return None
    return {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
    }


def _warm_up(model: str):
    """Print a playful warm-up message the first time we use a given model."""
    global _last_model
    if model != _last_model:
        warmups = [
            f"🧠 Loading model '{model}' into RAM... give me a sec...",
            f"💾 Spinning up the AI core for '{model}'...",
            f"⏳ Summoning the knowledge spirits... '{model}' booting...",
            f"🤖 Thinking really hard with '{model}'...",
            f"⚙️ Switching to model: {model} ... (may take a few seconds)",
        ]
        msg = random.choice(warmups)
        print(msg)
        log.debug(f"Model switch: {msg}")
        time.sleep(1.2)
        _last_model = model


def chat_completion(
    messages: list,
    model: str | None = None,
    personality: str = "friendly",
    stream: bool = False,
    retries: int = 2,
) -> tuple[str, dict | None]:
    """
    Send a list of chat messages to the LLM and return ``(content, usage)``.

    This is the low-level, multi-message primitive used by both
    :func:`get_response` (single-turn) and :class:`Conversation` (multi-turn).

    Args:
        messages: OpenAI-style message dicts, e.g.
            ``[{"role": "system", ...}, {"role": "user", ...}]``.
        model: LLM model to use (defaults to config setting).
        personality: Used to pick a fallback message during retries.
        stream: Whether to request streaming output.
        retries: Number of attempts before giving up.

    Returns:
        tuple: ``(content, usage)`` where ``usage`` is a token-count dict, or
        ``None`` when the provider does not report usage (e.g. streaming).
    """
    if model is None:
        from ..config import get_model
        model = get_model()

    _warm_up(model)

    global _last_usage

    # Stream if explicitly requested, or if live REPL printing is enabled.
    do_stream = stream or _print_stream

    for attempt in range(1, retries + 1):
        try:
            client = _build_client()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=do_stream,
                timeout=10,
            )

            if isinstance(response, Stream):
                # Collect all chunks (usage is not available when streaming),
                # printing each one live when REPL streaming is on.
                content = ""
                for chunk in response:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        if _print_stream:
                            print(delta, end="", flush=True)
                        content += delta
                if _print_stream:
                    print()  # final newline after the streamed response
                _last_usage = None
                return (content or "⚠️ No response from model.", None)

            content = response.choices[0].message.content or "⚠️ No response from model."
            usage = _usage_dict(response)
            _last_usage = usage
            return (content, usage)

        except Exception as e:
            log.warning(f"Error during request (attempt {attempt}): {e}")
            if attempt < retries:
                fallback = _fallbacks.get(personality, _fallbacks.get("default", ["Retrying..."]))
                print(random.choice(fallback))
                time.sleep(1.0)
            else:
                return (f"❌ Error: {str(e)}", None)

    # Unreachable when retries >= 1, but keeps the return type honest.
    return ("❌ Error: no attempts made.", None)


@overload
def get_response(
    prompt: str,
    model: str | None = ...,
    system: str = ...,
    personality: str = ...,
    stream: bool = ...,
    retries: int = ...,
    return_usage: Literal[False] = False,
) -> str: ...


@overload
def get_response(
    prompt: str,
    model: str | None = ...,
    system: str = ...,
    personality: str = ...,
    stream: bool = ...,
    retries: int = ...,
    return_usage: Literal[True] = ...,
) -> tuple[str, dict | None]: ...


def get_response(
    prompt: str,
    model: str | None = None,
    system: str = "You are a helpful assistant.",
    personality: str = "friendly",
    stream: bool = False,
    retries: int = 2,
    return_usage: bool = False,
) -> str | tuple[str, dict | None]:
    """
    Send a single prompt to the LLM and retrieve the model's response.

    This is a stateless, single-turn helper: it sends exactly one system
    message and one user message, with no memory of previous calls. For a
    multi-turn chat that remembers history, use :class:`Conversation`.

    Args:
        prompt (str): The text prompt to send to the model
        model (str): LLM model to use (defaults to config setting)
        system (str): System message defining bot behavior
        personality (str): Used for fallback character during retries
        stream (bool): Whether to request streaming output (default False)
        retries (int): Number of times to retry on error
        return_usage (bool): If True, return ``(response, usage)`` where
            ``usage`` is a token-count dict (or None if unavailable)

    Returns:
        str: AI response or error message. If ``return_usage`` is True, a
        ``(response, usage)`` tuple instead.
    """
    # Check for empty prompt
    if not prompt.strip():
        return ("⚠️ Empty prompt.", None) if return_usage else "⚠️ Empty prompt."

    # Resolve the model now so it is part of the cache key.
    if model is None:
        from ..config import get_model
        model = get_model()

    # Opt-in disk cache (HANDS_ON_AI_CACHE). Skip while streaming to the REPL,
    # where the printed output, not the return value, is what the user sees.
    from .. import cache
    use_cache = not stream and not _print_stream
    if use_cache:
        cached = cache.get(model, system, prompt)
        if cached is not None:
            return (cached, None) if return_usage else cached

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]
    content, usage = chat_completion(
        messages,
        model=model,
        personality=personality,
        stream=stream,
        retries=retries,
    )

    # Only cache real responses, not error/empty placeholders.
    if use_cache and not content.startswith(("❌", "⚠️")):
        cache.put(model, system, prompt, content)

    return (content, usage) if return_usage else content


def stream_response(
    prompt: str,
    model: str | None = None,
    system: str = "You are a helpful assistant.",
    personality: str = "friendly",
    retries: int = 2,
) -> Iterator[str]:
    """
    Like :func:`get_response`, but yields the response in chunks as it arrives.

    This lets you show text as the model generates it, instead of waiting for the
    whole answer:

        for chunk in stream_response("Tell me a short story"):
            print(chunk, end="", flush=True)

    Args:
        prompt: The text prompt to send to the model.
        model: LLM model to use (defaults to config setting).
        system: System message defining bot behavior.
        personality: Unused here; kept for signature parity with get_response.
        retries: Unused here; streaming makes a single attempt.

    Yields:
        str: Pieces of the response as they arrive.
    """
    if not prompt.strip():
        yield "⚠️ Empty prompt."
        return

    if model is None:
        from ..config import get_model
        model = get_model()

    _warm_up(model)

    try:
        client = _build_client()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            stream=True,
            timeout=10,
        )
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception as e:
        log.warning(f"Error during streaming request: {e}")
        yield f"❌ Error: {str(e)}"
