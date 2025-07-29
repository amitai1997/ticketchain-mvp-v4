"""
Abstract blockchain service interface for interacting with the Ticket smart contract.
"""

from abc import ABC, abstractmethod
from typing import Any


class BlockchainServiceInterface(ABC):
    """Abstract interface for blockchain interactions."""

    @abstractmethod
    async def mint_ticket(
        self,
        to_address: str,
        token_uri: str,
    ) -> dict[str, Any]:
        """
        Mint a new ticket NFT.

        Args:
            to_address: Ethereum address to mint the ticket to
            token_uri: URI containing ticket metadata

        Returns:
            Dict containing token_id, transaction_hash, and other details
        """
        pass

    @abstractmethod
    async def check_in_ticket(self, token_id: int) -> dict[str, Any]:
        """
        Check in a ticket by updating its on-chain state.

        Args:
            token_id: The NFT token ID to check in

        Returns:
            Dict containing transaction_hash and updated state
        """
        pass

    @abstractmethod
    async def invalidate_ticket(self, token_id: int) -> dict[str, Any]:
        """
        Invalidate a ticket by updating its on-chain state.

        Args:
            token_id: The NFT token ID to invalidate

        Returns:
            Dict containing transaction_hash and updated state
        """
        pass

    @abstractmethod
    async def transfer_ticket(
        self,
        token_id: int,
        from_address: str,
        to_address: str,
    ) -> dict[str, Any]:
        """
        Transfer a ticket NFT from one address to another.

        Args:
            token_id: The NFT token ID to transfer
            from_address: Current owner address
            to_address: New owner address

        Returns:
            Dict containing transaction_hash and transfer details
        """
        pass

    @abstractmethod
    async def get_ticket_status(self, token_id: int) -> str:
        """
        Get the current status of a ticket.

        Args:
            token_id: The NFT token ID

        Returns:
            Current ticket status (Valid, CheckedIn, Invalidated)
        """
        pass

    @abstractmethod
    async def get_ticket_owner(self, token_id: int) -> str:
        """
        Get the current owner of a ticket.

        Args:
            token_id: The NFT token ID

        Returns:
            Ethereum address of the current owner
        """
        pass
