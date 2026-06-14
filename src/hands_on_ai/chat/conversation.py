"""
Multi-turn conversation memory for the chat module.

An LLM is stateless: each request only sees the messages you send it. To make a
bot that "remembers" earlier turns, you keep the running transcript and resend it
every time. ``Conversation`` does exactly that bookkeeping for you, so you can
focus on the conversation instead of the plumbing.

Example:
    >>> from hands_on_ai.chat import Conversation
    >>> chat = Conversation(system="You are a helpful tutor.")
    >>> chat.ask("My name is Sam.")
    >>> chat.ask("What's my name?")   # remembers "Sam"
    >>> print(chat.total_tokens)      # tokens used across the whole chat
"""

from .get_response import chat_completion


class Conversation:
    """A stateful chat that remembers the conversation history."""

    def __init__(
        self,
        system: str = "You are a helpful assistant.",
        model: str = None,
        personality: str = "friendly",
    ):
        """
        Args:
            system: System message that defines the bot's behavior.
            model: LLM model to use (defaults to config setting).
            personality: Used for fallback character during retries.
        """
        self.system = system
        self.model = model
        self.personality = personality
        # The transcript we resend each turn. The system message stays first.
        self.messages = [{"role": "system", "content": system}]
        # Token accounting (None until the provider reports usage).
        self.last_usage = None
        self.total_tokens = 0

    def ask(self, prompt: str, stream: bool = False) -> str:
        """
        Send ``prompt`` as the next user turn and return the model's reply.

        The user message and the reply are both appended to the history, so the
        next call automatically includes everything said so far.
        """
        self.messages.append({"role": "user", "content": prompt})
        content, usage = chat_completion(
            self.messages,
            model=self.model,
            personality=self.personality,
            stream=stream,
        )
        self.messages.append({"role": "assistant", "content": content})

        self.last_usage = usage
        if usage and usage.get("total_tokens"):
            self.total_tokens += usage["total_tokens"]

        return content

    def reset(self):
        """Clear the conversation history, keeping the original system prompt."""
        self.messages = [{"role": "system", "content": self.system}]
        self.last_usage = None
        self.total_tokens = 0

    def history(self) -> list:
        """Return the user/assistant turns (excluding the system message)."""
        return [m for m in self.messages if m["role"] != "system"]
