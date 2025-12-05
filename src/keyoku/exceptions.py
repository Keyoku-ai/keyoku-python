"""Keyoku SDK exceptions."""

from typing import Any, Optional


class KeyokuError(Exception):
    """Base exception for Keyoku SDK."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(KeyokuError):
    """Raised when API key is invalid or missing."""
    pass


class NotFoundError(KeyokuError):
    """Raised when a resource is not found."""
    pass


class ValidationError(KeyokuError):
    """Raised when request validation fails."""
    pass


class RateLimitError(KeyokuError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        **kwargs: Any,
    ):
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class ServerError(KeyokuError):
    """Raised when server returns 5xx error."""
    pass
