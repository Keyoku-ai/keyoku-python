"""Tests for Jobs resource."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.models import Job, JobStatus


class TestJobsResource:
    """Tests for client.jobs operations."""

    @respx.mock
    def test_get_job_completed(self, client: Keyoku, job_response: dict):
        """Test getting a completed job."""
        respx.get("https://api.keyoku.dev/v1/jobs/job_abc123").mock(
            return_value=Response(200, json=job_response)
        )

        result = client.jobs.get("job_abc123")

        assert isinstance(result, Job)
        assert result.id == "job_abc123"
        assert result.status == JobStatus.COMPLETED
        assert result.result == {"memory_id": "mem_new123"}
        assert result.completed_at is not None

    @respx.mock
    def test_get_job_pending(self, client: Keyoku, job_pending_response: dict):
        """Test getting a pending job."""
        respx.get("https://api.keyoku.dev/v1/jobs/job_abc123").mock(
            return_value=Response(200, json=job_pending_response)
        )

        result = client.jobs.get("job_abc123")

        assert result.status == JobStatus.PENDING
        assert result.completed_at is None

    @respx.mock
    def test_get_job_failed(self, client: Keyoku):
        """Test getting a failed job."""
        respx.get("https://api.keyoku.dev/v1/jobs/job_abc123").mock(
            return_value=Response(
                200,
                json={
                    "id": "job_abc123",
                    "status": "failed",
                    "error": "Processing failed",
                    "created_at": "2024-01-15T10:30:00Z",
                },
            )
        )

        result = client.jobs.get("job_abc123")

        assert result.status == JobStatus.FAILED
        assert result.error == "Processing failed"
