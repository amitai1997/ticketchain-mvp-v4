"""
Pytest configuration for integration tests.
"""

import asyncio
import sys
from pathlib import Path

import pytest

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as an integration test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Add integration marker to tests in integration directory
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
