"""Schemas resource for Keyoku API."""

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import Schema

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class SchemasResource:
    """Resource for extraction schema operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def list(self) -> list[Schema]:
        """List all schemas.

        Returns:
            List of schemas
        """
        response = self._client.request("GET", "/v1/schemas")
        return [Schema(**s) for s in response.get("schemas", [])]

    def get(self, schema_id: str) -> Schema:
        """Get a specific schema by ID.

        Args:
            schema_id: The schema ID

        Returns:
            The schema
        """
        response = self._client.request("GET", f"/v1/schemas/{schema_id}")
        return Schema(**response)

    def create(
        self,
        name: str,
        schema: dict[str, Any],
        *,
        description: Optional[str] = None,
    ) -> Schema:
        """Create a new extraction schema.

        Args:
            name: Schema name
            schema: JSON Schema definition
            description: Optional description

        Returns:
            The created schema
        """
        data: dict[str, Any] = {"name": name, "schema": schema}
        if description:
            data["description"] = description

        response = self._client.request("POST", "/v1/schemas", json=data)
        return Schema(**response)

    def update(
        self,
        schema_id: str,
        *,
        name: Optional[str] = None,
        schema: Optional[dict[str, Any]] = None,
        description: Optional[str] = None,
    ) -> Schema:
        """Update an existing schema.

        Args:
            schema_id: The schema ID to update
            name: New name (optional)
            schema: New schema definition (optional)
            description: New description (optional)

        Returns:
            The updated schema
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if schema is not None:
            data["schema"] = schema
        if description is not None:
            data["description"] = description

        response = self._client.request("PUT", f"/v1/schemas/{schema_id}", json=data)
        return Schema(**response)

    def delete(self, schema_id: str) -> None:
        """Delete a schema.

        Args:
            schema_id: The schema ID to delete
        """
        self._client.request("DELETE", f"/v1/schemas/{schema_id}")
