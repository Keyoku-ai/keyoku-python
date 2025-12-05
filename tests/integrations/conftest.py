"""Fixtures for framework integration tests."""

import os
import pytest

# Skip all tests in this directory if running unit tests only
def pytest_collection_modifyitems(config, items):
    """Skip framework tests unless explicitly requested."""
    if config.getoption("-m") and "framework" not in config.getoption("-m"):
        skip_framework = pytest.mark.skip(reason="Framework tests not selected")
        for item in items:
            if "integrations" in str(item.fspath):
                item.add_marker(skip_framework)


@pytest.fixture
def live_api_key() -> str:
    """Get API key for live testing.

    Set KEYOKU_TEST_API_KEY environment variable or this will skip.
    """
    key = os.environ.get("KEYOKU_TEST_API_KEY")
    if not key:
        pytest.skip("KEYOKU_TEST_API_KEY not set")
    return key


@pytest.fixture
def live_base_url() -> str:
    """Get base URL for live testing."""
    return os.environ.get("KEYOKU_TEST_BASE_URL", "http://localhost:8000")


@pytest.fixture
def keyoku_client(live_api_key: str, live_base_url: str):
    """Create a live Keyoku client for testing."""
    from keyoku import Keyoku
    return Keyoku(api_key=live_api_key, base_url=live_base_url)
