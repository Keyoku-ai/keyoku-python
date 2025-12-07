"""Data resource for Keyoku API (GDPR export)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from keyoku.models import ExportResponse

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class DataResource:
    """Resource for GDPR data export operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def export(self) -> ExportResponse:
        """Start a GDPR data export job.

        Returns a job_id that can be polled for completion using jobs.get().
        Once complete, use download() to retrieve the export file.

        Returns:
            ExportResponse with job_id and status
        """
        response = self._client.request("GET", "/v1/data/export")
        return ExportResponse(**response)

    def download(self, job_id: str) -> bytes:
        """Download an export file after the export job completes.

        Args:
            job_id: The job ID from the export() call

        Returns:
            The export file contents as bytes (JSONL format)
        """
        # Use the underlying httpx client directly for raw response
        response = self._client._client.get(f"/v1/data/export/{job_id}/download")
        if response.status_code != 200:
            self._client._handle_response(response)
        return response.content
