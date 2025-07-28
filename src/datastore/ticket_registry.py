"""
Ticket registry for mapping off-chain ticket IDs to on-chain token IDs.

This module provides a simple in-memory storage for development.
In production, this would be replaced with a proper database.
"""

import json
from pathlib import Path
from typing import Optional

from src.config import settings


class TicketRegistry:
    """Simple registry for mapping ticket IDs to blockchain token IDs."""

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the ticket registry.

        Args:
            storage_path: Optional path to persist the registry to disk
        """
        self.storage_path = storage_path
        self._registry: dict[str, int] = {}

        # Load existing data if storage path provided
        if self.storage_path and Path(self.storage_path).exists():
            self._load_from_disk()

    def register_ticket(self, ticket_id: str, token_id: int) -> None:
        """Register a mapping from ticket ID to token ID."""
        self._registry[ticket_id] = token_id
        if self.storage_path:
            self._save_to_disk()

    def get_token_id(self, ticket_id: str) -> Optional[int]:
        """Get the token ID for a given ticket ID."""
        return self._registry.get(ticket_id)

    def exists(self, ticket_id: str) -> bool:
        """Check if a ticket ID is registered."""
        return ticket_id in self._registry

    def clear(self) -> None:
        """Clear all entries from the registry. Used for testing."""
        self._registry.clear()
        if self.storage_path:
            self._save_to_disk()

    def _load_from_disk(self) -> None:
        """Load registry from disk."""
        if self.storage_path is None:
            self._registry = {}
            return

        try:
            with open(self.storage_path) as f:
                self._registry = json.load(f)
        except Exception:
            # If loading fails, start with empty registry
            self._registry = {}

    def _save_to_disk(self) -> None:
        """Save registry to disk."""
        if self.storage_path is None:
            return

        try:
            # Ensure directory exists
            Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)

            with open(self.storage_path, "w") as f:
                json.dump(self._registry, f, indent=2)
        except Exception:
            # Silently fail for now - in production, log this
            pass


# Global registry instance - None for tests, file-based for dev
ticket_registry = TicketRegistry(storage_path=settings.ticket_registry_path)
