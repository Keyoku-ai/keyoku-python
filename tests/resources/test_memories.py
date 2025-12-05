"""Tests for Memories resource."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.models import Memory, ListMemoriesResponse


class TestMemoriesResource:
    """Tests for client.memories operations."""

    @respx.mock
    def test_list_memories(self, client: Keyoku, memory_response: dict):
        """Test listing memories."""
        respx.get("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                200,
                json={
                    "memories": [memory_response],
                    "total": 1,
                    "has_more": False,
                },
            )
        )

        result = client.memories.list()

        assert isinstance(result, ListMemoriesResponse)
        assert len(result.memories) == 1
        assert result.memories[0].id == "mem_abc123"
        assert result.total == 1
        assert result.has_more is False

    @respx.mock
    def test_list_memories_with_pagination(self, client: Keyoku, memory_response: dict):
        """Test listing memories with pagination params."""
        route = respx.get("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                200,
                json={"memories": [], "total": 0, "has_more": False},
            )
        )

        client.memories.list(limit=25, offset=50)

        assert "limit=25" in str(route.calls[0].request.url)
        assert "offset=50" in str(route.calls[0].request.url)

    @respx.mock
    def test_list_memories_with_agent_id(self, client: Keyoku):
        """Test listing memories filtered by agent_id."""
        route = respx.get("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                200,
                json={"memories": [], "total": 0, "has_more": False},
            )
        )

        client.memories.list(agent_id="my-agent")

        assert "agent_id=my-agent" in str(route.calls[0].request.url)

    @respx.mock
    def test_get_memory(self, client: Keyoku, memory_response: dict):
        """Test getting a specific memory."""
        respx.get("https://api.keyoku.dev/v1/memories/mem_abc123").mock(
            return_value=Response(200, json=memory_response)
        )

        result = client.memories.get("mem_abc123")

        assert isinstance(result, Memory)
        assert result.id == "mem_abc123"
        assert result.content == "User prefers dark mode"
        assert result.type == "preference"
        assert result.importance == 0.8

    @respx.mock
    def test_delete_memory(self, client: Keyoku):
        """Test deleting a memory."""
        route = respx.delete("https://api.keyoku.dev/v1/memories/mem_abc123").mock(
            return_value=Response(200)
        )

        client.memories.delete("mem_abc123")

        assert route.called

    @respx.mock
    def test_delete_all_memories(self, client: Keyoku):
        """Test deleting all memories."""
        route = respx.delete("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(200)
        )

        client.memories.delete_all()

        assert route.called

    @respx.mock
    def test_batch_create(self, client: Keyoku):
        """Test batch creating memories."""
        route = respx.post("https://api.keyoku.dev/v1/memories/batch").mock(
            return_value=Response(200, json={"job_id": "batch_job_123"})
        )

        result = client.memories.batch_create(
            ["Memory 1", "Memory 2", "Memory 3"],
            session_id="session_123",
            agent_id="agent_1",
        )

        assert result["job_id"] == "batch_job_123"
        request_body = route.calls[0].request.content
        assert b"Memory 1" in request_body
        assert b"session_123" in request_body

    @respx.mock
    def test_batch_delete(self, client: Keyoku):
        """Test batch deleting memories."""
        route = respx.delete("https://api.keyoku.dev/v1/memories/batch").mock(
            return_value=Response(200)
        )

        client.memories.batch_delete(["mem_1", "mem_2", "mem_3"])

        assert route.called
        request_body = route.calls[0].request.content
        assert b"mem_1" in request_body
        assert b"mem_2" in request_body
