"""LangChain integration for Keyoku.

Install with: pip install keyoku[langchain]

Example:
    ```python
    from keyoku.integrations.langchain import KeyokuMemory, KeyokuChatMessageHistory
    from langchain.chains import ConversationChain
    from langchain_openai import ChatOpenAI

    # Use as chat message history
    history = KeyokuChatMessageHistory(
        api_key="your-api-key",
        session_id="conversation-123",
    )

    # Use as memory
    memory = KeyokuMemory(api_key="your-api-key")

    chain = ConversationChain(
        llm=ChatOpenAI(),
        memory=memory,
    )
    ```
"""

from typing import Any, Optional, Sequence

try:
    from langchain_core.chat_history import BaseChatMessageHistory
    from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
    from langchain.memory import ConversationBufferMemory
except ImportError as e:
    raise ImportError(
        "LangChain is required for this integration. "
        "Install it with: pip install keyoku[langchain]"
    ) from e

from keyoku import Keyoku


class KeyokuChatMessageHistory(BaseChatMessageHistory):
    """LangChain chat message history backed by Keyoku.

    This stores conversation messages in Keyoku for long-term memory.
    """

    def __init__(
        self,
        api_key: str,
        session_id: str,
        *,
        base_url: Optional[str] = None,
        agent_id: Optional[str] = None,
    ):
        """Initialize Keyoku chat history.

        Args:
            api_key: Keyoku API key
            session_id: Session ID to group messages
            base_url: Optional custom API URL
            agent_id: Optional agent ID for multi-agent systems
        """
        self.session_id = session_id
        self.agent_id = agent_id

        client_kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self._client = Keyoku(**client_kwargs)
        self._messages: list[BaseMessage] = []

    @property
    def messages(self) -> list[BaseMessage]:
        """Get all messages in the session."""
        return self._messages

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the history."""
        self._messages.append(message)

        # Store in Keyoku
        content = f"[{message.type}]: {message.content}"
        self._client.remember(
            content,
            session_id=self.session_id,
            agent_id=self.agent_id,
        )

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Add multiple messages."""
        for message in messages:
            self.add_message(message)

    def clear(self) -> None:
        """Clear the message history."""
        self._messages = []


class KeyokuMemory(ConversationBufferMemory):
    """LangChain memory backed by Keyoku.

    This provides semantic memory retrieval from Keyoku.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        memory_key: str = "history",
        return_messages: bool = False,
        **kwargs: Any,
    ):
        """Initialize Keyoku memory.

        Args:
            api_key: Keyoku API key
            base_url: Optional custom API URL
            session_id: Optional session ID
            agent_id: Optional agent ID
            memory_key: Key to use in memory dict
            return_messages: Whether to return messages or string
        """
        client_kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self._keyoku = Keyoku(**client_kwargs)
        self._session_id = session_id
        self._agent_id = agent_id

        super().__init__(
            memory_key=memory_key,
            return_messages=return_messages,
            **kwargs,
        )

    def save_context(self, inputs: dict[str, Any], outputs: dict[str, str]) -> None:
        """Save context to Keyoku."""
        super().save_context(inputs, outputs)

        # Store the interaction in Keyoku
        input_str = str(inputs)
        output_str = str(outputs)
        content = f"User: {input_str}\nAssistant: {output_str}"

        self._keyoku.remember(
            content,
            session_id=self._session_id,
            agent_id=self._agent_id,
        )
