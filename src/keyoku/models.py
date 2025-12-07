"""Pydantic models for Keyoku API responses."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Status of an async job."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Memory(BaseModel):
    """A memory stored in Keyoku."""
    id: str
    content: str
    type: str
    agent_id: str
    importance: float
    created_at: datetime


class MemorySearchResult(BaseModel):
    """A memory with similarity score from search."""
    id: str
    content: str
    type: str
    agent_id: str
    importance: float
    score: float
    created_at: datetime


class SearchResponse(BaseModel):
    """Response from memory search."""
    memories: list[MemorySearchResult]
    query_time_ms: int


class ListMemoriesResponse(BaseModel):
    """Response from listing memories."""
    memories: list[Memory]
    total: int
    has_more: bool


class Job(BaseModel):
    """An async job."""
    id: str
    status: JobStatus
    result: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class RememberResponse(BaseModel):
    """Response from remember operation."""
    job_id: str
    status: str


class Entity(BaseModel):
    """An entity in the knowledge graph."""
    id: str
    canonical_name: str
    type: str
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: Optional[datetime] = None


class Relationship(BaseModel):
    """A relationship between entities."""
    id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str
    properties: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class EntityWithRelationships(BaseModel):
    """Entity with its relationships."""
    entity: Entity
    relationships: list[Relationship]


class Stats(BaseModel):
    """Memory statistics."""
    total_memories: int
    by_type: dict[str, int]


class Schema(BaseModel):
    """Extraction schema."""
    id: str
    name: str
    description: Optional[str] = None
    schema_def: dict[str, Any] = Field(alias="schema")
    created_at: datetime
    updated_at: datetime


class CleanupStrategy(str, Enum):
    """Memory cleanup strategies."""
    STALE = "stale"
    LOW_IMPORTANCE = "low_importance"
    OLDEST = "oldest"
    NEVER_ACCESSED = "never_accessed"


class CleanupSuggestion(BaseModel):
    """A cleanup suggestion."""
    strategy: str
    description: str
    count: int


class CleanupUsage(BaseModel):
    """Current memory usage info."""
    memories_stored: int
    memories_limit: int
    percentage: int


class CleanupSuggestionsResponse(BaseModel):
    """Response from cleanup suggestions."""
    suggestions: list[CleanupSuggestion]
    usage: CleanupUsage


class CleanupResponse(BaseModel):
    """Response from cleanup execution."""
    deleted_count: int
    deleted_ids: Optional[list[str]] = None


class ExportResponse(BaseModel):
    """Response from export request."""
    job_id: str
    status: str


class AuditLog(BaseModel):
    """An audit log entry."""
    id: str
    operation: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[dict[str, Any]] = None
    created_at: datetime


class AuditLogsResponse(BaseModel):
    """Response from audit logs query."""
    audit_logs: list[AuditLog]
    total: int
    has_more: bool
