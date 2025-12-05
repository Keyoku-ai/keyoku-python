"""Shared test fixtures for Keyoku SDK tests."""

import pytest
from typing import Generator
from unittest.mock import MagicMock

import respx
from httpx import Response

from keyoku import Keyoku, AsyncKeyoku


# Test constants
TEST_API_KEY = "test_api_key_12345"
TEST_BASE_URL = "https://api.keyoku.dev"
TEST_ENTITY_ID = "test_entity_123"


@pytest.fixture
def api_key() -> str:
    """Test API key."""
    return TEST_API_KEY


@pytest.fixture
def base_url() -> str:
    """Test base URL."""
    return TEST_BASE_URL


@pytest.fixture
def client(api_key: str) -> Keyoku:
    """Create a Keyoku client for testing."""
    return Keyoku(api_key=api_key)


@pytest.fixture
def client_with_entity(api_key: str) -> Keyoku:
    """Create a Keyoku client with entity ID."""
    return Keyoku(api_key=api_key, entity_id=TEST_ENTITY_ID)


@pytest.fixture
def async_client(api_key: str) -> AsyncKeyoku:
    """Create an async Keyoku client for testing."""
    return AsyncKeyoku(api_key=api_key)


@pytest.fixture
def mock_api() -> Generator[respx.MockRouter, None, None]:
    """Context manager for mocking API responses."""
    with respx.mock(base_url=TEST_BASE_URL) as respx_mock:
        yield respx_mock


# Common response fixtures
@pytest.fixture
def memory_response() -> dict:
    """Sample memory response."""
    return {
        "id": "mem_abc123",
        "content": "User prefers dark mode",
        "type": "preference",
        "agent_id": "default",
        "importance": 0.8,
        "created_at": "2024-01-15T10:30:00Z",
    }


@pytest.fixture
def memory_search_response() -> dict:
    """Sample search response."""
    return {
        "memories": [
            {
                "id": "mem_abc123",
                "content": "User prefers dark mode",
                "type": "preference",
                "agent_id": "default",
                "importance": 0.8,
                "score": 0.95,
                "created_at": "2024-01-15T10:30:00Z",
            },
            {
                "id": "mem_def456",
                "content": "User uses VS Code",
                "type": "fact",
                "agent_id": "default",
                "importance": 0.6,
                "score": 0.82,
                "created_at": "2024-01-14T09:00:00Z",
            },
        ],
        "query_time_ms": 42,
    }


@pytest.fixture
def entity_response() -> dict:
    """Sample entity response."""
    return {
        "id": "ent_xyz789",
        "name": "John Doe",
        "type": "person",
        "properties": {"age": 30, "occupation": "developer"},
        "created_at": "2024-01-10T08:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z",
    }


@pytest.fixture
def relationship_response() -> dict:
    """Sample relationship response."""
    return {
        "id": "rel_123456",
        "source_id": "ent_abc",
        "target_id": "ent_def",
        "type": "works_with",
        "properties": {"since": "2020"},
        "created_at": "2024-01-12T14:00:00Z",
    }


@pytest.fixture
def job_response() -> dict:
    """Sample job response."""
    return {
        "id": "job_abc123",
        "status": "completed",
        "result": {"memory_id": "mem_new123"},
        "created_at": "2024-01-15T10:30:00Z",
        "completed_at": "2024-01-15T10:30:05Z",
    }


@pytest.fixture
def job_pending_response() -> dict:
    """Sample pending job response."""
    return {
        "id": "job_abc123",
        "status": "pending",
        "created_at": "2024-01-15T10:30:00Z",
    }


@pytest.fixture
def schema_response() -> dict:
    """Sample schema response."""
    return {
        "id": "schema_123",
        "name": "user_preferences",
        "description": "Extract user preferences",
        "schema": {
            "type": "object",
            "properties": {
                "preference_type": {"type": "string"},
                "value": {"type": "string"},
            },
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-15T00:00:00Z",
    }


@pytest.fixture
def stats_response() -> dict:
    """Sample stats response."""
    return {
        "total_memories": 150,
        "by_type": {
            "fact": 80,
            "preference": 45,
            "event": 25,
        },
    }


@pytest.fixture
def error_response_401() -> dict:
    """Sample 401 error response."""
    return {
        "error": {
            "code": "unauthorized",
            "message": "Invalid API key",
        }
    }


@pytest.fixture
def error_response_404() -> dict:
    """Sample 404 error response."""
    return {
        "error": {
            "code": "not_found",
            "message": "Resource not found",
        }
    }


@pytest.fixture
def error_response_429() -> dict:
    """Sample 429 error response."""
    return {
        "error": {
            "code": "rate_limit",
            "message": "Rate limit exceeded",
        }
    }
