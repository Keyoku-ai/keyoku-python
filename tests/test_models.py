"""Tests for Pydantic models."""

import pytest
from datetime import datetime

from keyoku.models import (
    Memory,
    MemorySearchResult,
    ListMemoriesResponse,
    Entity,
    Relationship,
    Job,
    JobStatus,
    Schema,
    Stats,
)


class TestMemoryModels:
    """Tests for memory-related models."""

    def test_memory_from_dict(self):
        """Test creating Memory from dict."""
        data = {
            "id": "mem_123",
            "content": "User likes Python",
            "type": "preference",
            "agent_id": "default",
            "importance": 0.75,
            "created_at": "2024-01-15T10:30:00Z",
        }

        memory = Memory(**data)

        assert memory.id == "mem_123"
        assert memory.content == "User likes Python"
        assert memory.type == "preference"
        assert memory.importance == 0.75
        assert isinstance(memory.created_at, datetime)

    def test_memory_search_result(self):
        """Test MemorySearchResult includes score."""
        data = {
            "id": "mem_123",
            "content": "User likes Python",
            "type": "preference",
            "agent_id": "default",
            "importance": 0.75,
            "score": 0.92,
            "created_at": "2024-01-15T10:30:00Z",
        }

        result = MemorySearchResult(**data)

        assert result.score == 0.92

    def test_list_memories_response(self):
        """Test ListMemoriesResponse model."""
        data = {
            "memories": [
                {
                    "id": "mem_1",
                    "content": "Memory 1",
                    "type": "fact",
                    "agent_id": "default",
                    "importance": 0.5,
                    "created_at": "2024-01-15T10:30:00Z",
                }
            ],
            "total": 100,
            "has_more": True,
        }

        response = ListMemoriesResponse(**data)

        assert len(response.memories) == 1
        assert response.total == 100
        assert response.has_more is True


class TestEntityModels:
    """Tests for entity-related models."""

    def test_entity_from_dict(self):
        """Test creating Entity from dict."""
        data = {
            "id": "ent_123",
            "name": "John Doe",
            "type": "person",
            "properties": {"age": 30},
            "created_at": "2024-01-10T08:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
        }

        entity = Entity(**data)

        assert entity.id == "ent_123"
        assert entity.name == "John Doe"
        assert entity.properties["age"] == 30

    def test_entity_empty_properties(self):
        """Test Entity with empty properties."""
        data = {
            "id": "ent_123",
            "name": "Test",
            "type": "thing",
            "properties": {},
            "created_at": "2024-01-10T08:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
        }

        entity = Entity(**data)

        assert entity.properties == {}

    def test_relationship_from_dict(self):
        """Test creating Relationship from dict."""
        data = {
            "id": "rel_123",
            "source_id": "ent_a",
            "target_id": "ent_b",
            "type": "knows",
            "properties": {"since": "2020"},
            "created_at": "2024-01-12T14:00:00Z",
        }

        rel = Relationship(**data)

        assert rel.id == "rel_123"
        assert rel.source_id == "ent_a"
        assert rel.target_id == "ent_b"
        assert rel.type == "knows"


class TestJobModels:
    """Tests for job-related models."""

    def test_job_status_enum(self):
        """Test JobStatus enum values."""
        assert JobStatus.PENDING == "pending"
        assert JobStatus.PROCESSING == "processing"
        assert JobStatus.COMPLETED == "completed"
        assert JobStatus.FAILED == "failed"

    def test_job_completed(self):
        """Test completed Job model."""
        data = {
            "id": "job_123",
            "status": "completed",
            "result": {"memory_id": "mem_456"},
            "created_at": "2024-01-15T10:30:00Z",
            "completed_at": "2024-01-15T10:30:05Z",
        }

        job = Job(**data)

        assert job.status == JobStatus.COMPLETED
        assert job.result["memory_id"] == "mem_456"
        assert job.completed_at is not None

    def test_job_failed(self):
        """Test failed Job model."""
        data = {
            "id": "job_123",
            "status": "failed",
            "error": "Processing error",
            "created_at": "2024-01-15T10:30:00Z",
        }

        job = Job(**data)

        assert job.status == JobStatus.FAILED
        assert job.error == "Processing error"
        assert job.result is None


class TestSchemaModel:
    """Tests for Schema model."""

    def test_schema_from_dict(self):
        """Test creating Schema from dict."""
        data = {
            "id": "schema_123",
            "name": "preferences",
            "description": "User preferences",
            "schema": {"type": "object"},
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-15T00:00:00Z",
        }

        schema = Schema(**data)

        assert schema.id == "schema_123"
        assert schema.name == "preferences"
        assert schema.description == "User preferences"


class TestStatsModel:
    """Tests for Stats model."""

    def test_stats_from_dict(self):
        """Test creating Stats from dict."""
        data = {
            "total_memories": 500,
            "by_type": {"fact": 300, "preference": 200},
        }

        stats = Stats(**data)

        assert stats.total_memories == 500
        assert stats.by_type["fact"] == 300
