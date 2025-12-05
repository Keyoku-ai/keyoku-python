"""Tests for the Keyoku client."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.exceptions import AuthenticationError, NotFoundError, ValidationError


@respx.mock
def test_remember():
    """Test remember creates a job."""
    respx.post("https://api.keyoku.dev/v1/memories").mock(
        return_value=Response(200, json={"job_id": "job_123", "status": "pending"})
    )

    client = Keyoku(api_key="test-key")
    job = client.remember("Test memory content")

    assert job.job_id == "job_123"


@respx.mock
def test_search():
    """Test search returns memories."""
    respx.post("https://api.keyoku.dev/v1/memories/search").mock(
        return_value=Response(
            200,
            json={
                "memories": [
                    {
                        "id": "mem_1",
                        "content": "User likes pizza",
                        "type": "preference",
                        "agent_id": "default",
                        "importance": 0.8,
                        "score": 0.95,
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "query_time_ms": 42,
            },
        )
    )

    client = Keyoku(api_key="test-key")
    results = client.search("food preferences")

    assert len(results) == 1
    assert results[0].content == "User likes pizza"
    assert results[0].score == 0.95


@respx.mock
def test_authentication_error():
    """Test authentication error is raised."""
    respx.post("https://api.keyoku.dev/v1/memories").mock(
        return_value=Response(
            401,
            json={"error": {"code": "unauthorized", "message": "Invalid API key"}},
        )
    )

    client = Keyoku(api_key="invalid-key")

    with pytest.raises(AuthenticationError):
        client.remember("Test content")


@respx.mock
def test_not_found_error():
    """Test not found error is raised."""
    respx.get("https://api.keyoku.dev/v1/memories/invalid").mock(
        return_value=Response(
            404,
            json={"error": {"code": "not_found", "message": "Memory not found"}},
        )
    )

    client = Keyoku(api_key="test-key")

    with pytest.raises(NotFoundError):
        client.memories.get("invalid")


@respx.mock
def test_validation_error():
    """Test validation error is raised."""
    respx.post("https://api.keyoku.dev/v1/memories").mock(
        return_value=Response(
            400,
            json={"error": {"code": "validation_error", "message": "content is required"}},
        )
    )

    client = Keyoku(api_key="test-key")

    with pytest.raises(ValidationError):
        client.remember("")


@respx.mock
def test_entity_id_header():
    """Test entity ID is sent in header."""
    route = respx.post("https://api.keyoku.dev/v1/memories").mock(
        return_value=Response(200, json={"job_id": "job_123", "status": "pending"})
    )

    client = Keyoku(api_key="test-key", entity_id="user-123")
    client.remember("Test content")

    assert route.calls[0].request.headers["X-Entity-ID"] == "user-123"


@respx.mock
def test_memories_list():
    """Test listing memories."""
    respx.get("https://api.keyoku.dev/v1/memories").mock(
        return_value=Response(
            200,
            json={
                "memories": [
                    {
                        "id": "mem_1",
                        "content": "Memory 1",
                        "type": "fact",
                        "agent_id": "default",
                        "importance": 0.5,
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ],
                "total": 1,
                "has_more": False,
            },
        )
    )

    client = Keyoku(api_key="test-key")
    response = client.memories.list()

    assert len(response.memories) == 1
    assert response.total == 1
    assert response.has_more is False


@respx.mock
def test_entities_search():
    """Test searching entities."""
    respx.get("https://api.keyoku.dev/v1/entities/search").mock(
        return_value=Response(
            200,
            json={
                "entities": [
                    {
                        "id": "ent_1",
                        "name": "John",
                        "type": "person",
                        "properties": {},
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                    }
                ]
            },
        )
    )

    client = Keyoku(api_key="test-key")
    entities = client.entities.search("John")

    assert len(entities) == 1
    assert entities[0].name == "John"
