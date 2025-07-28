"""Unit tests for ticket registry."""

import pytest

from src.datastore.ticket_registry import TicketRegistry


def test_registry_clear():
    """Test that registry clearing works correctly."""
    # Create a registry without file persistence
    registry = TicketRegistry(storage_path=None)
    
    # Add some entries
    registry.register_ticket("test-1", 1)
    registry.register_ticket("test-2", 2)
    
    assert registry.exists("test-1")
    assert registry.exists("test-2")
    assert registry.get_token_id("test-1") == 1
    assert registry.get_token_id("test-2") == 2
    
    # Clear the registry
    registry.clear()
    
    # Verify it's empty
    assert not registry.exists("test-1")
    assert not registry.exists("test-2")
    assert registry.get_token_id("test-1") is None
    assert registry.get_token_id("test-2") is None


def test_registry_isolation_between_tests(clean_registry):
    """Test that the clean_registry fixture ensures isolation."""
    from src.datastore import ticket_registry
    
    # Registry should be empty at start of test
    assert not ticket_registry.exists("isolation-test")
    
    # Add an entry
    ticket_registry.register_ticket("isolation-test", 100)
    assert ticket_registry.exists("isolation-test")
    
    # The fixture will clear this after the test