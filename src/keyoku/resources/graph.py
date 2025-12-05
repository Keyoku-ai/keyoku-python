"""Graph resource for Keyoku API."""

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import Entity, Relationship

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class PathResult:
    """Result of a path finding operation."""

    def __init__(self, entities: list[Entity], relationships: list[Relationship]):
        self.entities = entities
        self.relationships = relationships
        self.length = len(relationships)

    def __repr__(self) -> str:
        if not self.entities:
            return "PathResult(no path found)"
        path_str = " -> ".join(e.name for e in self.entities)
        return f"PathResult({path_str})"


class GraphResource:
    """Resource for knowledge graph traversal operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def find_path(
        self,
        from_entity: str,
        to_entity: str,
        *,
        max_depth: int = 5,
        relationship_types: Optional[list[str]] = None,
    ) -> Optional[PathResult]:
        """Find the shortest path between two entities.

        Args:
            from_entity: Source entity ID
            to_entity: Target entity ID
            max_depth: Maximum path length to search
            relationship_types: Only traverse these relationship types

        Returns:
            PathResult if path found, None otherwise
        """
        params: dict[str, Any] = {
            "from": from_entity,
            "to": to_entity,
            "max_depth": max_depth,
        }
        if relationship_types:
            params["relationship_types"] = ",".join(relationship_types)

        response = self._client.request("GET", "/v1/graph/path", params=params)

        if not response.get("path"):
            return None

        entities = [Entity(**e) for e in response.get("entities", [])]
        relationships = [Relationship(**r) for r in response.get("relationships", [])]

        return PathResult(entities, relationships)
