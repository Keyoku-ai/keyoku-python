"""CrewAI integration tests.

Run with:
    pip install keyoku[crewai]
    KEYOKU_TEST_API_KEY=your-key pytest tests/integrations/test_crewai.py -m framework
"""

import pytest

# Mark all tests in this module as framework tests
pytestmark = pytest.mark.framework


class TestKeyokuCrewMemory:
    """Tests for KeyokuCrewMemory."""

    def test_import(self):
        """Test that CrewAI integration can be imported."""
        try:
            from keyoku.integrations.crewai import KeyokuCrewMemory
            assert KeyokuCrewMemory is not None
        except ImportError as e:
            pytest.skip(f"CrewAI not installed: {e}")

    def test_create_memory(self, live_api_key: str, live_base_url: str):
        """Test creating CrewAI memory."""
        try:
            from keyoku.integrations.crewai import KeyokuCrewMemory
        except ImportError:
            pytest.skip("CrewAI not installed")

        memory = KeyokuCrewMemory(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        assert memory is not None

    def test_save_memory(self, live_api_key: str, live_base_url: str):
        """Test saving memory."""
        try:
            from keyoku.integrations.crewai import KeyokuCrewMemory
        except ImportError:
            pytest.skip("CrewAI not installed")

        memory = KeyokuCrewMemory(
            api_key=live_api_key,
            base_url=live_base_url,
            agent_id="test-crew-agent",
        )

        # Save should not raise
        memory.save("The user mentioned they work at a tech company")

    def test_search_memory(self, live_api_key: str, live_base_url: str):
        """Test searching memory."""
        try:
            from keyoku.integrations.crewai import KeyokuCrewMemory
        except ImportError:
            pytest.skip("CrewAI not installed")

        memory = KeyokuCrewMemory(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        results = memory.search("tech company", limit=5)

        assert isinstance(results, list)
        # Results may be empty if nothing matches

    def test_reset_memory(self, live_api_key: str, live_base_url: str):
        """Test resetting memory."""
        try:
            from keyoku.integrations.crewai import KeyokuCrewMemory
        except ImportError:
            pytest.skip("CrewAI not installed")

        memory = KeyokuCrewMemory(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        # Reset should not raise
        # Note: This deletes ALL memories, use with caution in tests
        # memory.reset()
        pass  # Skip actual reset in tests to avoid data loss

    def test_search_returns_correct_format(self, live_api_key: str, live_base_url: str):
        """Test that search returns correctly formatted results."""
        try:
            from keyoku.integrations.crewai import KeyokuCrewMemory
        except ImportError:
            pytest.skip("CrewAI not installed")

        memory = KeyokuCrewMemory(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        # First save something
        memory.save("Test memory for format checking")

        results = memory.search("format checking", limit=1)

        if results:
            # Check result format
            assert "content" in results[0]
            assert "score" in results[0]
            assert "metadata" in results[0]
