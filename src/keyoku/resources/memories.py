"""Memories resource for Keyoku API."""

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import ListMemoriesResponse, Memory

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class MemoriesResource:
    """Resource for memory operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        agent_id: Optional[str] = None,
    ) -> ListMemoriesResponse:
        """List all memories.

        Args:
            limit: Maximum number of memories to return
            offset: Number of memories to skip
            agent_id: Filter by agent ID

        Returns:
            ListMemoriesResponse with memories and pagination info
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if agent_id:
            params["agent_id"] = agent_id

        response = self._client.request("GET", "/v1/memories", params=params)
        return ListMemoriesResponse(**response)

    def get(self, memory_id: str) -> Memory:
        """Get a specific memory by ID.

        Args:
            memory_id: The memory ID

        Returns:
            The memory
        """
        response = self._client.request("GET", f"/v1/memories/{memory_id}")
        return Memory(**response)

    def delete(self, memory_id: str) -> None:
        """Delete a specific memory.

        Args:
            memory_id: The memory ID to delete
        """
        self._client.request("DELETE", f"/v1/memories/{memory_id}")

    def delete_all(self) -> None:
        """Delete all memories for the current entity."""
        self._client.request("DELETE", "/v1/memories")

    def batch_create(
        self,
        contents: list[str],
        *,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create multiple memories in batch.

        Args:
            contents: List of content strings to remember
            session_id: Optional session ID for all memories
            agent_id: Optional agent ID for all memories

        Returns:
            Batch job response
        """
        data: dict[str, Any] = {
            "memories": [{"content": c} for c in contents],
        }
        if session_id:
            data["session_id"] = session_id
        if agent_id:
            data["agent_id"] = agent_id

        return self._client.request("POST", "/v1/memories/batch", json=data)

    def batch_delete(self, memory_ids: list[str]) -> None:
        """Delete multiple memories in batch.

        Args:
            memory_ids: List of memory IDs to delete
        """
        self._client.request(
            "DELETE",
            "/v1/memories/batch",
            json={"ids": memory_ids},
        )
