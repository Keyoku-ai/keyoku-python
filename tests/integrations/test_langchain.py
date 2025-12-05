"""LangChain integration tests.

Run with:
    pip install keyoku[langchain]
    KEYOKU_TEST_API_KEY=your-key pytest tests/integrations/test_langchain.py -m framework
"""

import pytest

# Mark all tests in this module as framework tests
pytestmark = pytest.mark.framework


class TestKeyokuChatMessageHistory:
    """Tests for KeyokuChatMessageHistory."""

    def test_import(self):
        """Test that LangChain integration can be imported."""
        try:
            from keyoku.integrations.langchain import KeyokuChatMessageHistory
            assert KeyokuChatMessageHistory is not None
        except ImportError as e:
            pytest.skip(f"LangChain not installed: {e}")

    def test_create_history(self, live_api_key: str, live_base_url: str):
        """Test creating chat message history."""
        try:
            from keyoku.integrations.langchain import KeyokuChatMessageHistory
        except ImportError:
            pytest.skip("LangChain not installed")

        history = KeyokuChatMessageHistory(
            api_key=live_api_key,
            session_id="test-session-123",
            base_url=live_base_url,
        )

        assert history.session_id == "test-session-123"

    def test_add_messages(self, live_api_key: str, live_base_url: str):
        """Test adding messages to history."""
        try:
            from keyoku.integrations.langchain import KeyokuChatMessageHistory
        except ImportError:
            pytest.skip("LangChain not installed")

        history = KeyokuChatMessageHistory(
            api_key=live_api_key,
            session_id="test-session-456",
            base_url=live_base_url,
        )

        # Add messages
        history.add_user_message("Hello, how are you?")
        history.add_ai_message("I'm doing well, thank you!")

        # Check messages are stored locally
        messages = history.messages
        assert len(messages) == 2

    def test_clear_messages(self, live_api_key: str, live_base_url: str):
        """Test clearing message history."""
        try:
            from keyoku.integrations.langchain import KeyokuChatMessageHistory
        except ImportError:
            pytest.skip("LangChain not installed")

        history = KeyokuChatMessageHistory(
            api_key=live_api_key,
            session_id="test-session-789",
            base_url=live_base_url,
        )

        history.add_user_message("Test message")
        history.clear()

        assert len(history.messages) == 0


class TestKeyokuMemory:
    """Tests for KeyokuMemory."""

    def test_import(self):
        """Test that KeyokuMemory can be imported."""
        try:
            from keyoku.integrations.langchain import KeyokuMemory
            assert KeyokuMemory is not None
        except ImportError as e:
            pytest.skip(f"LangChain not installed: {e}")

    def test_create_memory(self, live_api_key: str, live_base_url: str):
        """Test creating KeyokuMemory."""
        try:
            from keyoku.integrations.langchain import KeyokuMemory
        except ImportError:
            pytest.skip("LangChain not installed")

        memory = KeyokuMemory(
            api_key=live_api_key,
            base_url=live_base_url,
            session_id="test-memory-session",
        )

        assert memory.memory_key == "history"

    def test_save_and_load_context(self, live_api_key: str, live_base_url: str):
        """Test saving and loading context."""
        try:
            from keyoku.integrations.langchain import KeyokuMemory
        except ImportError:
            pytest.skip("LangChain not installed")

        memory = KeyokuMemory(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        # Save context
        memory.save_context(
            {"input": "What's the weather like?"},
            {"output": "It's sunny today!"},
        )

        # Load should work (even if empty initially)
        loaded = memory.load_memory_variables({"input": "weather"})
        assert memory.memory_key in loaded

    def test_memory_variables(self, live_api_key: str, live_base_url: str):
        """Test memory_variables property."""
        try:
            from keyoku.integrations.langchain import KeyokuMemory
        except ImportError:
            pytest.skip("LangChain not installed")

        memory = KeyokuMemory(
            api_key=live_api_key,
            base_url=live_base_url,
            memory_key="custom_key",
        )

        assert "custom_key" in memory.memory_variables
