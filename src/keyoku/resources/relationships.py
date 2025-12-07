"""Relationships resource for Keyoku API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import Relationship

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class RelationshipsResource:
    """Resource for knowledge graph relationship operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        type: Optional[str] = None,
    ) -> list[Relationship]:
        """List all relationships.

        Args:
            limit: Maximum number of relationships to return
            offset: Number of relationships to skip
            type: Filter by relationship type

        Returns:
            List of relationships
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if type:
            params["type"] = type

        response = self._client.request("GET", "/v1/relationships", params=params)
        return [Relationship(**r) for r in response.get("relationships", [])]

    def get(self, relationship_id: str) -> Relationship:
        """Get a specific relationship by ID.

        Args:
            relationship_id: The relationship ID

        Returns:
            The relationship
        """
        response = self._client.request("GET", f"/v1/relationships/{relationship_id}")
        return Relationship(**response)
