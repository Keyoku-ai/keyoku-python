"""Cleanup resource for Keyoku API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from keyoku.models import CleanupSuggestionsResponse, CleanupResponse, CleanupStrategy

if TYPE_CHECKING:
    from keyoku.client import Keyoku


class CleanupResource:
    """Resource for memory cleanup operations."""

    def __init__(self, client: "Keyoku"):
        self._client = client

    def suggestions(self) -> CleanupSuggestionsResponse:
        """Get cleanup suggestions for memory management.

        Returns strategies like stale, low_importance, oldest, never_accessed
        with counts of memories that would be affected.

        Returns:
            CleanupSuggestionsResponse with suggestions and current usage info
        """
        response = self._client.request("GET", "/v1/memories/cleanup-suggestions")
        return CleanupSuggestionsResponse(**response)

    def execute(
        self,
        strategy: CleanupStrategy | str,
        *,
        limit: int = 100,
        dry_run: bool = False,
    ) -> CleanupResponse:
        """Execute a cleanup strategy to delete memories.

        Args:
            strategy: Cleanup strategy - stale, low_importance, oldest, never_accessed
            limit: Maximum number of memories to delete (default: 100, max: 1000)
            dry_run: If True, returns what would be deleted without deleting

        Returns:
            CleanupResponse with deleted count and optionally deleted IDs
        """
        # Convert enum to string if needed
        strategy_str = strategy.value if isinstance(strategy, CleanupStrategy) else strategy

        data: dict[str, Any] = {
            "strategy": strategy_str,
            "limit": limit,
            "dry_run": dry_run,
        }

        response = self._client.request("POST", "/v1/memories/cleanup", json=data)
        return CleanupResponse(**response)
