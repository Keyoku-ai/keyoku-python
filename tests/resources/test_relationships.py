"""Tests for Relationships resource."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.models import Relationship


class TestRelationshipsResource:
    """Tests for client.relationships operations."""

    @respx.mock
    def test_list_relationships(self, client: Keyoku, relationship_response: dict):
        """Test listing relationships."""
        respx.get("https://api.keyoku.dev/v1/relationships").mock(
            return_value=Response(
                200, json={"relationships": [relationship_response]}
            )
        )

        result = client.relationships.list()

        assert len(result) == 1
        assert isinstance(result[0], Relationship)
        assert result[0].id == "rel_123456"
        assert result[0].type == "works_with"
        assert result[0].source_id == "ent_abc"
        assert result[0].target_id == "ent_def"

    @respx.mock
    def test_list_relationships_with_params(self, client: Keyoku):
        """Test listing relationships with parameters."""
        route = respx.get("https://api.keyoku.dev/v1/relationships").mock(
            return_value=Response(200, json={"relationships": []})
        )

        client.relationships.list(limit=30, offset=5, type="knows")

        url = str(route.calls[0].request.url)
        assert "limit=30" in url
        assert "offset=5" in url
        assert "type=knows" in url

    @respx.mock
    def test_get_relationship(self, client: Keyoku, relationship_response: dict):
        """Test getting a specific relationship."""
        respx.get("https://api.keyoku.dev/v1/relationships/rel_123456").mock(
            return_value=Response(200, json=relationship_response)
        )

        result = client.relationships.get("rel_123456")

        assert isinstance(result, Relationship)
        assert result.id == "rel_123456"
        assert result.properties["since"] == "2020"
