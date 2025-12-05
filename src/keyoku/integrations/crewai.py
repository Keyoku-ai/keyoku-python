"""CrewAI integration for Keyoku.

Install with: pip install keyoku[crewai]

Example:
    ```python
    from keyoku.integrations.crewai import KeyokuMemory
    from crewai import Crew, Agent, Task

    memory = KeyokuMemory(api_key="your-api-key")

    crew = Crew(
        agents=[...],
        tasks=[...],
        memory=memory,
    )
    ```
"""

from typing import Any, Optional

try:
    from crewai.memory import EntityMemory
except ImportError as e:
    raise ImportError(
        "CrewAI is required for this integration. "
        "Install it with: pip install keyoku[crewai]"
    ) from e

from keyoku import Keyoku


class KeyokuCrewMemory(EntityMemory):
    """CrewAI memory backed by Keyoku.

    Provides long-term memory for CrewAI agents using Keyoku's
    semantic memory infrastructure.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        agent_id: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize Keyoku memory for CrewAI.

        Args:
            api_key: Keyoku API key
            base_url: Optional custom API URL
            agent_id: Optional agent ID for filtering
        """
        super().__init__(**kwargs)

        client_kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self._client = Keyoku(**client_kwargs)
        self._agent_id = agent_id

    def save(self, value: str, metadata: Optional[dict[str, Any]] = None) -> None:
        """Save a memory."""
        self._client.remember(value, agent_id=self._agent_id)

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Search memories."""
        results = self._client.search(query, limit=limit, agent_id=self._agent_id)
        return [
            {
                "content": r.content,
                "score": r.score,
                "metadata": {"type": r.type, "agent_id": r.agent_id},
            }
            for r in results
        ]

    def reset(self) -> None:
        """Clear all memories."""
        self._client.memories.delete_all()
