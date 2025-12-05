"""Tests for async Keyoku client."""

import pytest
import respx
from httpx import Response

from keyoku import AsyncKeyoku
from keyoku.models import JobStatus


class TestAsyncKeyoku:
    """Tests for AsyncKeyoku client."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_remember(self, api_key: str):
        """Test async remember operation."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(200, json={"job_id": "job_123", "status": "pending"})
        )

        async with AsyncKeyoku(api_key=api_key) as client:
            job = await client.remember("Test content")

        assert job.job_id == "job_123"

    @pytest.mark.asyncio
    @respx.mock
    async def test_remember_with_options(self, api_key: str):
        """Test async remember with session and agent ID."""
        route = respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(200, json={"job_id": "job_123", "status": "pending"})
        )

        async with AsyncKeyoku(api_key=api_key) as client:
            await client.remember(
                "Test content",
                session_id="session_abc",
                agent_id="agent_xyz",
            )

        request_body = route.calls[0].request.content
        assert b"session_abc" in request_body
        assert b"agent_xyz" in request_body

    @pytest.mark.asyncio
    @respx.mock
    async def test_search(self, api_key: str, memory_search_response: dict):
        """Test async search operation."""
        respx.post("https://api.keyoku.dev/v1/memories/search").mock(
            return_value=Response(200, json=memory_search_response)
        )

        async with AsyncKeyoku(api_key=api_key) as client:
            results = await client.search("preferences")

        assert len(results) == 2
        assert results[0].score == 0.95

    @pytest.mark.asyncio
    @respx.mock
    async def test_stats(self, api_key: str, stats_response: dict):
        """Test async stats operation."""
        respx.get("https://api.keyoku.dev/v1/stats").mock(
            return_value=Response(200, json=stats_response)
        )

        async with AsyncKeyoku(api_key=api_key) as client:
            result = await client.stats()

        assert result.total_memories == 150

    @pytest.mark.asyncio
    @respx.mock
    async def test_job_wait(self, api_key: str):
        """Test async job wait."""
        # First call returns pending, second returns completed
        respx.get("https://api.keyoku.dev/v1/jobs/job_123").mock(
            side_effect=[
                Response(
                    200,
                    json={
                        "id": "job_123",
                        "status": "pending",
                        "created_at": "2024-01-15T10:30:00Z",
                    },
                ),
                Response(
                    200,
                    json={
                        "id": "job_123",
                        "status": "completed",
                        "result": {"memory_id": "mem_123"},
                        "created_at": "2024-01-15T10:30:00Z",
                        "completed_at": "2024-01-15T10:30:05Z",
                    },
                ),
            ]
        )

        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(200, json={"job_id": "job_123", "status": "pending"})
        )

        async with AsyncKeyoku(api_key=api_key) as client:
            job = await client.remember("Test")
            result = await job.wait(poll_interval=0.01)

        assert result.status == JobStatus.COMPLETED

    @pytest.mark.asyncio
    @respx.mock
    async def test_context_manager(self, api_key: str):
        """Test async context manager properly closes client."""
        respx.get("https://api.keyoku.dev/v1/stats").mock(
            return_value=Response(200, json={"total_memories": 0, "by_type": {}})
        )

        async with AsyncKeyoku(api_key=api_key) as client:
            await client.stats()

        # Client should be closed after context manager exits
        # This is implicitly tested - if close fails, the test would fail
