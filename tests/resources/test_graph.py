"""Tests for Graph resource."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.resources.graph import PathResult


class TestGraphResource:
    """Tests for client.graph operations."""

    @respx.mock
    def test_find_path_success(
        self, client: Keyoku, entity_response: dict, relationship_response: dict
    ):
        """Test finding a path between entities."""
        respx.get("https://api.keyoku.dev/v1/graph/path").mock(
            return_value=Response(
                200,
                json={
                    "path": True,
                    "entities": [entity_response, entity_response],
                    "relationships": [relationship_response],
                },
            )
        )

        result = client.graph.find_path("ent_a", "ent_b")

        assert result is not None
        assert isinstance(result, PathResult)
        assert len(result.entities) == 2
        assert len(result.relationships) == 1
        assert result.length == 1

    @respx.mock
    def test_find_path_no_path(self, client: Keyoku):
        """Test finding a path when none exists."""
        respx.get("https://api.keyoku.dev/v1/graph/path").mock(
            return_value=Response(
                200,
                json={"path": False, "entities": [], "relationships": []},
            )
        )

        result = client.graph.find_path("ent_a", "ent_z")

        assert result is None

    @respx.mock
    def test_find_path_with_params(self, client: Keyoku):
        """Test finding a path with parameters."""
        route = respx.get("https://api.keyoku.dev/v1/graph/path").mock(
            return_value=Response(
                200,
                json={"path": False, "entities": [], "relationships": []},
            )
        )

        client.graph.find_path(
            "ent_a",
            "ent_b",
            max_depth=3,
            relationship_types=["knows", "works_with"],
        )

        url = str(route.calls[0].request.url)
        assert "from=ent_a" in url
        assert "to=ent_b" in url
        assert "max_depth=3" in url
        assert "relationship_types=knows%2Cworks_with" in url or "relationship_types=knows,works_with" in url

    @respx.mock
    def test_path_result_repr(
        self, client: Keyoku, entity_response: dict, relationship_response: dict
    ):
        """Test PathResult string representation."""
        respx.get("https://api.keyoku.dev/v1/graph/path").mock(
            return_value=Response(
                200,
                json={
                    "path": True,
                    "entities": [entity_response],
                    "relationships": [],
                },
            )
        )

        result = client.graph.find_path("ent_a", "ent_b")

        assert "John Doe" in repr(result)
