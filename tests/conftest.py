"""
Pytest configuration for integration tests.
"""

import sys
from pathlib import Path

import pytest

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def clean_registry():
    """Reset the ticket registry before each test to ensure test isolation."""
    from src.datastore.ticket_registry import ticket_registry

    # Ensure tests use in-memory registry
    ticket_registry.storage_path = None

    # Clear the registry before each test
    ticket_registry.clear()
    yield
    # Clear after test as well
    ticket_registry.clear()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as an integration test")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers."""
    for item in items:
        # Add integration marker to tests in integration directory
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
