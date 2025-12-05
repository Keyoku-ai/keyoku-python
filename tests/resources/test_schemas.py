"""Tests for Schemas resource."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.models import Schema


class TestSchemasResource:
    """Tests for client.schemas operations."""

    @respx.mock
    def test_list_schemas(self, client: Keyoku, schema_response: dict):
        """Test listing schemas."""
        respx.get("https://api.keyoku.dev/v1/schemas").mock(
            return_value=Response(200, json={"schemas": [schema_response]})
        )

        result = client.schemas.list()

        assert len(result) == 1
        assert isinstance(result[0], Schema)
        assert result[0].id == "schema_123"
        assert result[0].name == "user_preferences"

    @respx.mock
    def test_get_schema(self, client: Keyoku, schema_response: dict):
        """Test getting a specific schema."""
        respx.get("https://api.keyoku.dev/v1/schemas/schema_123").mock(
            return_value=Response(200, json=schema_response)
        )

        result = client.schemas.get("schema_123")

        assert isinstance(result, Schema)
        assert result.id == "schema_123"
        assert result.description == "Extract user preferences"

    @respx.mock
    def test_create_schema(self, client: Keyoku, schema_response: dict):
        """Test creating a schema."""
        route = respx.post("https://api.keyoku.dev/v1/schemas").mock(
            return_value=Response(201, json=schema_response)
        )

        test_schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        result = client.schemas.create(
            name="test_schema",
            schema=test_schema,
            description="A test schema",
        )

        assert isinstance(result, Schema)
        assert route.called
        request_body = route.calls[0].request.content
        assert b"test_schema" in request_body
        assert b"A test schema" in request_body

    @respx.mock
    def test_update_schema(self, client: Keyoku, schema_response: dict):
        """Test updating a schema."""
        route = respx.put("https://api.keyoku.dev/v1/schemas/schema_123").mock(
            return_value=Response(200, json=schema_response)
        )

        result = client.schemas.update(
            "schema_123",
            name="updated_name",
            description="Updated description",
        )

        assert isinstance(result, Schema)
        request_body = route.calls[0].request.content
        assert b"updated_name" in request_body

    @respx.mock
    def test_delete_schema(self, client: Keyoku):
        """Test deleting a schema."""
        route = respx.delete("https://api.keyoku.dev/v1/schemas/schema_123").mock(
            return_value=Response(200)
        )

        client.schemas.delete("schema_123")

        assert route.called
