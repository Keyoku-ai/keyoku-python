"""Audit resource for Keyoku API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import AuditLogsResponse

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class AuditResource:
    """Resource for audit log operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def list(
        self,
        *,
        operation: Optional[str] = None,
        resource_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> AuditLogsResponse:
        """List audit logs with optional filtering.

        Args:
            operation: Filter by operation type (e.g., "memory.create")
            resource_type: Filter by resource type (e.g., "memory")
            start_date: Filter by start date (RFC3339 format)
            end_date: Filter by end date (RFC3339 format)
            limit: Number of logs to return (default: 50, max: 100)
            offset: Pagination offset

        Returns:
            AuditLogsResponse with logs, total count, and pagination info
        """
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }
        if operation:
            params["operation"] = operation
        if resource_type:
            params["resource_type"] = resource_type
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        response = self._client.request("GET", "/v1/audit-logs", params=params)
        return AuditLogsResponse(**response)
