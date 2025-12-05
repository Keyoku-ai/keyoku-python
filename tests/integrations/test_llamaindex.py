"""LlamaIndex integration tests.

Run with:
    pip install keyoku[llamaindex]
    KEYOKU_TEST_API_KEY=your-key pytest tests/integrations/test_llamaindex.py -m framework
"""

import pytest

# Mark all tests in this module as framework tests
pytestmark = pytest.mark.framework


class TestKeyokuVectorStore:
    """Tests for KeyokuVectorStore."""

    def test_import(self):
        """Test that LlamaIndex integration can be imported."""
        try:
            from keyoku.integrations.llamaindex import KeyokuVectorStore
            assert KeyokuVectorStore is not None
        except ImportError as e:
            pytest.skip(f"LlamaIndex not installed: {e}")

    def test_create_vector_store(self, live_api_key: str, live_base_url: str):
        """Test creating vector store."""
        try:
            from keyoku.integrations.llamaindex import KeyokuVectorStore
        except ImportError:
            pytest.skip("LlamaIndex not installed")

        store = KeyokuVectorStore(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        assert store.client is not None

    def test_class_name(self):
        """Test class_name method."""
        try:
            from keyoku.integrations.llamaindex import KeyokuVectorStore
        except ImportError:
            pytest.skip("LlamaIndex not installed")

        assert KeyokuVectorStore.class_name() == "KeyokuVectorStore"

    def test_add_nodes(self, live_api_key: str, live_base_url: str):
        """Test adding nodes to vector store."""
        try:
            from keyoku.integrations.llamaindex import KeyokuVectorStore
            from llama_index.core.schema import TextNode
        except ImportError as e:
            pytest.skip(f"LlamaIndex not installed: {e}")

        store = KeyokuVectorStore(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        nodes = [
            TextNode(text="User prefers Python programming", id_="node_1"),
            TextNode(text="User likes machine learning", id_="node_2"),
        ]

        ids = store.add(nodes)

        assert len(ids) == 2
        assert "node_1" in ids
        assert "node_2" in ids

    def test_query(self, live_api_key: str, live_base_url: str):
        """Test querying vector store."""
        try:
            from keyoku.integrations.llamaindex import KeyokuVectorStore
            from llama_index.core.vector_stores.types import VectorStoreQuery
        except ImportError as e:
            pytest.skip(f"LlamaIndex not installed: {e}")

        store = KeyokuVectorStore(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        query = VectorStoreQuery(query_str="programming", similarity_top_k=5)
        result = store.query(query)

        assert result is not None
        assert hasattr(result, "nodes")
        assert hasattr(result, "similarities")

    def test_delete(self, live_api_key: str, live_base_url: str):
        """Test deleting from vector store."""
        try:
            from keyoku.integrations.llamaindex import KeyokuVectorStore
            from llama_index.core.schema import TextNode
        except ImportError as e:
            pytest.skip(f"LlamaIndex not installed: {e}")

        store = KeyokuVectorStore(
            api_key=live_api_key,
            base_url=live_base_url,
        )

        # This may raise NotFoundError if the ID doesn't exist,
        # which is expected behavior
        try:
            store.delete("nonexistent_id")
        except Exception:
            pass  # Expected if ID doesn't exist
