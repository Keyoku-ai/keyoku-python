"""Entities resource for Keyoku API."""

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import Entity, Relationship

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class EntitiesResource:
    """Resource for knowledge graph entity operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def list(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        type: Optional[str] = None,
    ) -> list[Entity]:
        """List all entities.

        Args:
            limit: Maximum number of entities to return
            offset: Number of entities to skip
            type: Filter by entity type

        Returns:
            List of entities
        """
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if type:
            params["type"] = type

        response = self._client.request("GET", "/v1/entities", params=params)
        return [Entity(**e) for e in response.get("entities", [])]

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        type: Optional[str] = None,
    ) -> list[Entity]:
        """Search entities by name.

        Args:
            query: Search query
            limit: Maximum results to return
            type: Filter by entity type

        Returns:
            List of matching entities
        """
        params: dict[str, Any] = {"query": query, "limit": limit}
        if type:
            params["type"] = type

        response = self._client.request("GET", "/v1/entities/search", params=params)
        return [Entity(**e) for e in response.get("entities", [])]

    def get(self, entity_id: str) -> Entity:
        """Get a specific entity by ID.

        Args:
            entity_id: The entity ID

        Returns:
            The entity
        """
        response = self._client.request("GET", f"/v1/entities/{entity_id}")
        return Entity(**response)

    def relationships(
        self,
        entity_id: str,
        *,
        direction: str = "both",
        type: Optional[str] = None,
    ) -> list[Relationship]:
        """Get relationships for an entity.

        Args:
            entity_id: The entity ID
            direction: "incoming", "outgoing", or "both"
            type: Filter by relationship type

        Returns:
            List of relationships
        """
        params: dict[str, Any] = {"direction": direction}
        if type:
            params["type"] = type

        response = self._client.request(
            "GET",
            f"/v1/entities/{entity_id}/relationships",
            params=params,
        )
        return [Relationship(**r) for r in response.get("relationships", [])]
