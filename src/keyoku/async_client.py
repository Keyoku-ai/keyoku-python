"""Asynchronous Keyoku client."""

import asyncio
from typing import Any, Optional

import httpx

from keyoku.exceptions import (
    AuthenticationError,
    KeyokuError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from keyoku.models import (
    Job,
    JobStatus,
    MemorySearchResult,
    Stats,
)


DEFAULT_BASE_URL = "https://api.keyoku.dev"
DEFAULT_TIMEOUT = 30.0


class AsyncKeyoku:
    """Asynchronous client for Keyoku API.

    Example:
        ```python
        from keyoku import AsyncKeyoku

        async with AsyncKeyoku(api_key="your-api-key") as client:
            job = await client.remember("User prefers dark mode")
            await job.wait()

            results = await client.search("preferences")
        ```
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        entity_id: Optional[str] = None,
    ):
        """Initialize the async Keyoku client.

        Args:
            api_key: Your Keyoku API key
            base_url: API base URL (default: https://api.keyoku.dev)
            timeout: Request timeout in seconds (default: 30)
            entity_id: Entity ID for multi-tenant isolation
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.entity_id = entity_id

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers=self._default_headers(),
        )

    def _default_headers(self) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "keyoku-python/0.1.0",
        }
        if self.entity_id:
            headers["X-Entity-ID"] = self.entity_id
        return headers

    def _handle_response(self, response: httpx.Response) -> Any:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 200 or response.status_code == 201:
            return response.json() if response.content else None

        try:
            error_data = response.json()
            message = error_data.get("error", {}).get("message", "Unknown error")
        except Exception:
            message = response.text or "Unknown error"

        if response.status_code == 401:
            raise AuthenticationError(message, response.status_code)
        elif response.status_code == 404:
            raise NotFoundError(message, response.status_code)
        elif response.status_code == 400 or response.status_code == 422:
            raise ValidationError(message, response.status_code)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                message,
                retry_after=int(retry_after) if retry_after else None,
                status_code=response.status_code,
            )
        elif response.status_code >= 500:
            raise ServerError(message, response.status_code)
        else:
            raise KeyokuError(message, response.status_code)

    async def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Make an async API request."""
        response = await self._client.request(
            method,
            path,
            json=json,
            params=params,
        )
        return self._handle_response(response)

    async def remember(
        self,
        content: str,
        *,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> "AsyncJobHandle":
        """Store a memory asynchronously.

        Args:
            content: The content to remember
            session_id: Optional session ID for grouping
            agent_id: Optional agent ID for multi-agent systems

        Returns:
            AsyncJobHandle that can be awaited for completion
        """
        data: dict[str, Any] = {"content": content}
        if session_id:
            data["session_id"] = session_id
        if agent_id:
            data["agent_id"] = agent_id

        response = await self.request("POST", "/v1/memories", json=data)
        return AsyncJobHandle(self, response["job_id"])

    async def search(
        self,
        query: str,
        *,
        limit: int = 10,
        mode: str = "hybrid",
        agent_id: Optional[str] = None,
    ) -> list[MemorySearchResult]:
        """Search memories.

        Args:
            query: Search query
            limit: Maximum results to return (default: 10)
            mode: Search mode - "semantic", "keyword", or "hybrid"
            agent_id: Filter by agent ID

        Returns:
            List of matching memories with scores
        """
        data: dict[str, Any] = {
            "query": query,
            "limit": limit,
            "mode": mode,
        }
        if agent_id:
            data["agent_id"] = agent_id

        response = await self.request("POST", "/v1/memories/search", json=data)
        return [MemorySearchResult(**m) for m in response["memories"]]

    async def stats(self) -> Stats:
        """Get memory statistics."""
        response = await self.request("GET", "/v1/stats")
        return Stats(**response)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncKeyoku":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()


class AsyncJobHandle:
    """Async handle for a job that can be awaited."""

    def __init__(self, client: AsyncKeyoku, job_id: str):
        self.client = client
        self.job_id = job_id

    async def get(self) -> Job:
        """Get current job status."""
        response = await self.client.request("GET", f"/v1/jobs/{self.job_id}")
        return Job(**response)

    async def wait(
        self,
        *,
        poll_interval: float = 0.5,
        timeout: Optional[float] = None,
    ) -> Job:
        """Wait for job to complete.

        Args:
            poll_interval: Seconds between status checks
            timeout: Maximum seconds to wait (None = no timeout)

        Returns:
            Completed job

        Raises:
            TimeoutError: If timeout is reached
            KeyokuError: If job fails
        """
        import time

        start = time.time()
        while True:
            job = await self.get()
            if job.status == JobStatus.COMPLETED:
                return job
            if job.status == JobStatus.FAILED:
                raise KeyokuError(job.error or "Job failed")

            if timeout and (time.time() - start) > timeout:
                raise TimeoutError(f"Job {self.job_id} did not complete in {timeout}s")

            await asyncio.sleep(poll_interval)
