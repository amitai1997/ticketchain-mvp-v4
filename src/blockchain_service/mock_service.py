"""
Mock implementation of the blockchain service for development and testing.
"""

from datetime import datetime
from typing import Any, Dict

from .interface import BlockchainServiceInterface


class MockBlockchainService(BlockchainServiceInterface):
    """Mock blockchain service that returns fake data for development."""

    def __init__(self):
        # Track ticket states in memory for the mock
        self._next_token_id = 1
        self._tickets: Dict[int, Dict[str, Any]] = {}

    async def mint_ticket(
        self,
        to_address: str,
        token_uri: str,
    ) -> Dict[str, Any]:
        """Mock ticket minting."""
        token_id = self._next_token_id
        self._next_token_id += 1

        self._tickets[token_id] = {
            "owner": to_address,
            "status": "Valid",
            "token_uri": token_uri,
        }

        return {
            "token_id": token_id,
            "transaction_hash": f"0x{'1234abcd' * 8}",
            "block_number": 12345,
            "gas_used": 150000,
            "timestamp": datetime.now().isoformat(),
        }

    async def check_in_ticket(self, token_id: int) -> Dict[str, Any]:
        """Mock ticket check-in."""
        if token_id in self._tickets:
            self._tickets[token_id]["status"] = "CheckedIn"

        return {
            "transaction_hash": f"0x{'5678efgh' * 8}",
            "block_number": 12346,
            "gas_used": 50000,
            "timestamp": datetime.now().isoformat(),
            "new_status": "CheckedIn",
        }

    async def invalidate_ticket(self, token_id: int) -> Dict[str, Any]:
        """Mock ticket invalidation."""
        if token_id in self._tickets:
            self._tickets[token_id]["status"] = "Invalidated"

        return {
            "transaction_hash": f"0x{'9abcijkl' * 8}",
            "block_number": 12347,
            "gas_used": 50000,
            "timestamp": datetime.now().isoformat(),
            "new_status": "Invalidated",
        }

    async def transfer_ticket(
        self,
        token_id: int,
        from_address: str,
        to_address: str,
    ) -> Dict[str, Any]:
        """Mock ticket transfer."""
        if token_id in self._tickets:
            self._tickets[token_id]["owner"] = to_address

        return {
            "transaction_hash": f"0x{'defmnopq' * 8}",
            "block_number": 12348,
            "gas_used": 60000,
            "timestamp": datetime.now().isoformat(),
            "from": from_address,
            "to": to_address,
        }

    async def get_ticket_status(self, token_id: int) -> str:
        """Mock get ticket status."""
        if token_id in self._tickets:
            return self._tickets[token_id]["status"]
        return "Invalid"

    async def get_ticket_owner(self, token_id: int) -> str:
        """Mock get ticket owner."""
        if token_id in self._tickets:
            return self._tickets[token_id]["owner"]
        return "0x0000000000000000000000000000000000000000"
