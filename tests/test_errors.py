"""Tests for error handling."""

import pytest
import respx
from httpx import Response

from keyoku import Keyoku
from keyoku.exceptions import (
    KeyokuError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)


class TestErrorHandling:
    """Tests for SDK error handling."""

    @respx.mock
    def test_authentication_error_401(self, client: Keyoku):
        """Test 401 raises AuthenticationError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                401,
                json={"error": {"code": "unauthorized", "message": "Invalid API key"}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            client.remember("Test")

        assert exc_info.value.status_code == 401
        assert "Invalid API key" in str(exc_info.value)

    @respx.mock
    def test_not_found_error_404(self, client: Keyoku):
        """Test 404 raises NotFoundError."""
        respx.get("https://api.keyoku.dev/v1/memories/nonexistent").mock(
            return_value=Response(
                404,
                json={"error": {"code": "not_found", "message": "Memory not found"}},
            )
        )

        with pytest.raises(NotFoundError) as exc_info:
            client.memories.get("nonexistent")

        assert exc_info.value.status_code == 404

    @respx.mock
    def test_validation_error_400(self, client: Keyoku):
        """Test 400 raises ValidationError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                400,
                json={
                    "error": {"code": "validation_error", "message": "content required"}
                },
            )
        )

        with pytest.raises(ValidationError) as exc_info:
            client.remember("")

        assert exc_info.value.status_code == 400

    @respx.mock
    def test_validation_error_422(self, client: Keyoku):
        """Test 422 raises ValidationError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                422,
                json={"error": {"code": "validation_error", "message": "Invalid data"}},
            )
        )

        with pytest.raises(ValidationError):
            client.remember("Test")

    @respx.mock
    def test_rate_limit_error_429(self, client: Keyoku):
        """Test 429 raises RateLimitError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                429,
                json={
                    "error": {"code": "rate_limit", "message": "Rate limit exceeded"}
                },
                headers={"Retry-After": "60"},
            )
        )

        with pytest.raises(RateLimitError) as exc_info:
            client.remember("Test")

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60

    @respx.mock
    def test_rate_limit_error_without_retry_after(self, client: Keyoku):
        """Test 429 without Retry-After header."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                429,
                json={
                    "error": {"code": "rate_limit", "message": "Rate limit exceeded"}
                },
            )
        )

        with pytest.raises(RateLimitError) as exc_info:
            client.remember("Test")

        assert exc_info.value.retry_after is None

    @respx.mock
    def test_server_error_500(self, client: Keyoku):
        """Test 500 raises ServerError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(
                500,
                json={"error": {"code": "internal_error", "message": "Server error"}},
            )
        )

        with pytest.raises(ServerError) as exc_info:
            client.remember("Test")

        assert exc_info.value.status_code == 500

    @respx.mock
    def test_server_error_502(self, client: Keyoku):
        """Test 502 raises ServerError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(502, text="Bad Gateway")
        )

        with pytest.raises(ServerError):
            client.remember("Test")

    @respx.mock
    def test_server_error_503(self, client: Keyoku):
        """Test 503 raises ServerError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(503, text="Service Unavailable")
        )

        with pytest.raises(ServerError):
            client.remember("Test")

    @respx.mock
    def test_generic_error(self, client: Keyoku):
        """Test unhandled status code raises KeyokuError."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(418, text="I'm a teapot")
        )

        with pytest.raises(KeyokuError) as exc_info:
            client.remember("Test")

        assert exc_info.value.status_code == 418

    @respx.mock
    def test_error_without_json_body(self, client: Keyoku):
        """Test error handling when response isn't JSON."""
        respx.post("https://api.keyoku.dev/v1/memories").mock(
            return_value=Response(500, text="Internal Server Error")
        )

        with pytest.raises(ServerError) as exc_info:
            client.remember("Test")

        assert "Internal Server Error" in str(exc_info.value)


class TestErrorProperties:
    """Tests for error class properties."""

    def test_keyoku_error_properties(self):
        """Test KeyokuError has all properties."""
        error = KeyokuError("Test message", status_code=400, response={"key": "value"})

        assert error.message == "Test message"
        assert error.status_code == 400
        assert error.response == {"key": "value"}
        assert str(error) == "Test message"

    def test_authentication_error_inheritance(self):
        """Test AuthenticationError inherits from KeyokuError."""
        error = AuthenticationError("Invalid key", 401)

        assert isinstance(error, KeyokuError)
        assert isinstance(error, Exception)

    def test_rate_limit_error_retry_after(self):
        """Test RateLimitError retry_after property."""
        error = RateLimitError("Rate limited", retry_after=120, status_code=429)

        assert error.retry_after == 120
        assert error.status_code == 429
