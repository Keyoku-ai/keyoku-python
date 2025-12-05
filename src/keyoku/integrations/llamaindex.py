"""LlamaIndex integration for Keyoku.

Install with: pip install keyoku[llamaindex]

Example:
    ```python
    from keyoku.integrations.llamaindex import KeyokuVectorStore

    vector_store = KeyokuVectorStore(api_key="your-api-key")
    retriever = vector_store.as_retriever(similarity_top_k=5)
    ```
"""

from typing import Any, List, Optional

try:
    from llama_index.core.schema import NodeWithScore, TextNode
    from llama_index.core.vector_stores.types import (
        BasePydanticVectorStore,
        VectorStoreQuery,
        VectorStoreQueryResult,
    )
except ImportError as e:
    raise ImportError(
        "LlamaIndex is required for this integration. "
        "Install it with: pip install keyoku[llamaindex]"
    ) from e

from keyoku import Keyoku


class KeyokuVectorStore(BasePydanticVectorStore):
    """LlamaIndex vector store backed by Keyoku."""

    stores_text: bool = True
    flat_metadata: bool = True

    _client: Keyoku

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
        agent_id: Optional[str] = None,
        **kwargs: Any,
    ):
        """Initialize Keyoku vector store.

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

    @classmethod
    def class_name(cls) -> str:
        return "KeyokuVectorStore"

    @property
    def client(self) -> Keyoku:
        return self._client

    def add(self, nodes: List[TextNode], **kwargs: Any) -> List[str]:
        """Add nodes to the vector store."""
        ids = []
        for node in nodes:
            job = self._client.remember(
                node.get_content(),
                agent_id=self._agent_id,
            )
            job.wait()
            ids.append(node.node_id)
        return ids

    def delete(self, ref_doc_id: str, **kwargs: Any) -> None:
        """Delete a document by ID."""
        self._client.memories.delete(ref_doc_id)

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        """Query the vector store."""
        results = self._client.search(
            query.query_str or "",
            limit=query.similarity_top_k or 10,
            agent_id=self._agent_id,
        )

        nodes = []
        similarities = []
        ids = []

        for result in results:
            node = TextNode(
                text=result.content,
                id_=result.id,
                metadata={"type": result.type, "agent_id": result.agent_id},
            )
            nodes.append(node)
            similarities.append(result.score)
            ids.append(result.id)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities,
            ids=ids,
        )
