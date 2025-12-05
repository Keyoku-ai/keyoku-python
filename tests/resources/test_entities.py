"""Tests for Entities resource."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.models import Entity, Relationship


class TestEntitiesResource:
    """Tests for client.entities operations."""

    @respx.mock
    def test_list_entities(self, client: Keyoku, entity_response: dict):
        """Test listing entities."""
        respx.get("https://api.keyoku.dev/v1/entities").mock(
            return_value=Response(200, json={"entities": [entity_response]})
        )

        result = client.entities.list()

        assert len(result) == 1
        assert isinstance(result[0], Entity)
        assert result[0].id == "ent_xyz789"
        assert result[0].name == "John Doe"
        assert result[0].type == "person"

    @respx.mock
    def test_list_entities_with_params(self, client: Keyoku):
        """Test listing entities with parameters."""
        route = respx.get("https://api.keyoku.dev/v1/entities").mock(
            return_value=Response(200, json={"entities": []})
        )

        client.entities.list(limit=20, offset=10, type="person")

        url = str(route.calls[0].request.url)
        assert "limit=20" in url
        assert "offset=10" in url
        assert "type=person" in url

    @respx.mock
    def test_search_entities(self, client: Keyoku, entity_response: dict):
        """Test searching entities."""
        respx.get("https://api.keyoku.dev/v1/entities/search").mock(
            return_value=Response(200, json={"entities": [entity_response]})
        )

        result = client.entities.search("John")

        assert len(result) == 1
        assert result[0].name == "John Doe"

    @respx.mock
    def test_search_entities_with_params(self, client: Keyoku):
        """Test searching entities with parameters."""
        route = respx.get("https://api.keyoku.dev/v1/entities/search").mock(
            return_value=Response(200, json={"entities": []})
        )

        client.entities.search("John", limit=5, type="person")

        url = str(route.calls[0].request.url)
        assert "query=John" in url
        assert "limit=5" in url
        assert "type=person" in url

    @respx.mock
    def test_get_entity(self, client: Keyoku, entity_response: dict):
        """Test getting a specific entity."""
        respx.get("https://api.keyoku.dev/v1/entities/ent_xyz789").mock(
            return_value=Response(200, json=entity_response)
        )

        result = client.entities.get("ent_xyz789")

        assert isinstance(result, Entity)
        assert result.id == "ent_xyz789"
        assert result.properties["age"] == 30

    @respx.mock
    def test_get_entity_relationships(
        self, client: Keyoku, relationship_response: dict
    ):
        """Test getting entity relationships."""
        respx.get("https://api.keyoku.dev/v1/entities/ent_xyz789/relationships").mock(
            return_value=Response(200, json={"relationships": [relationship_response]})
        )

        result = client.entities.relationships("ent_xyz789")

        assert len(result) == 1
        assert isinstance(result[0], Relationship)
        assert result[0].type == "works_with"

    @respx.mock
    def test_get_entity_relationships_with_params(self, client: Keyoku):
        """Test getting entity relationships with parameters."""
        route = respx.get(
            "https://api.keyoku.dev/v1/entities/ent_xyz789/relationships"
        ).mock(return_value=Response(200, json={"relationships": []}))

        client.entities.relationships("ent_xyz789", direction="outgoing", type="knows")

        url = str(route.calls[0].request.url)
        assert "direction=outgoing" in url
        assert "type=knows" in url
