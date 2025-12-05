"""Jobs resource for Keyoku API."""

from typing import TYPE_CHECKING

from keyoku.models import Job

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class JobsResource:
    """Resource for job operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def get(self, job_id: str) -> Job:
        """Get a job by ID.

        Args:
            job_id: The job ID

        Returns:
            The job
        """
        response = self._client.request("GET", f"/v1/jobs/{job_id}")
        return Job(**response)
