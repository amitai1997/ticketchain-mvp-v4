"""
Web3 implementation of the blockchain service for real blockchain interactions.
"""

from datetime import datetime
from typing import Any, Optional

from eth_account import Account
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

from ..config import get_contract_abi, settings
from .interface import BlockchainServiceInterface


class Web3BlockchainService(BlockchainServiceInterface):
    """Web3.py implementation for interacting with the Ticket smart contract."""

    def __init__(self, contract_address: Optional[str] = None):
        """
        Initialize the Web3 blockchain service.

        Args:
            contract_address: Address of the deployed Ticket contract.
                            If not provided, will use from settings.
        """
        # Validate required settings
        if not settings.rpc_url:
            raise ValueError("RPC_URL environment variable is required but not set")
        if not settings.deployer_private_key:
            raise ValueError(
                "DEPLOYER_PRIVATE_KEY environment variable is required but not set"
            )

        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(settings.rpc_url))

        # Add middleware for PoA networks (like some testnets)
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

        # Check connection
        if not self.w3.is_connected():
            raise ConnectionError(
                f"Failed to connect to blockchain node at {settings.rpc_url}"
            )

        # Set up account from private key
        self.account = Account.from_key(settings.deployer_private_key)

        # Load contract
        self.contract_address = contract_address or settings.ticket_contract_address
        if not self.contract_address:
            raise ValueError("Contract address not provided")

        # Initialize contract instance
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=get_contract_abi(),
        )

        # Cache for gas prices
        self._last_gas_price: Optional[int] = None

    async def _get_gas_price(self) -> int:
        """Get current gas price with caching."""
        # In production, implement proper caching with TTL
        if self._last_gas_price is None:
            self._last_gas_price = int(self.w3.eth.gas_price)
        return self._last_gas_price

    async def _send_transaction(self, func: Any) -> dict[str, Any]:
        """
        Build, sign, and send a transaction.

        Args:
            func: Contract function to call

        Returns:
            Transaction receipt details
        """
        # Get gas price
        gas_price = await self._get_gas_price()

        # Estimate gas and add buffer
        gas_estimate = func.estimate_gas({"from": self.account.address})
        gas_limit = int(gas_estimate * 1.2)  # Add 20% buffer

        # Build transaction
        tx = func.build_transaction(
            {
                "from": self.account.address,
                "gas": gas_limit,
                "gasPrice": gas_price,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "chainId": settings.chain_id,
            }
        )

        # Sign transaction
        signed_tx = self.w3.eth.account.sign_transaction(
            tx, settings.deployer_private_key
        )

        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "transaction_hash": receipt["transactionHash"].hex(),
            "block_number": receipt["blockNumber"],
            "gas_used": receipt["gasUsed"],
        }

    async def mint_ticket(
        self,
        to_address: str,
        token_uri: str,
    ) -> dict[str, Any]:
        """Mint a new ticket NFT on the blockchain."""
        try:
            # Call the mintTicket function
            func = self.contract.functions.mintTicket(
                Web3.to_checksum_address(to_address), token_uri
            )

            # Send transaction
            receipt = await self._send_transaction(func)

            # Get the token ID from the event logs
            logs = self.contract.events.TicketMinted().process_receipt(
                self.w3.eth.get_transaction_receipt(receipt["transaction_hash"])
            )

            if logs:
                token_id = logs[0]["args"]["tokenId"]
            else:
                # Fallback: calculate token ID (assumes sequential minting)
                token_id = self.contract.functions.totalSupply().call() - 1

            block = self.w3.eth.get_block(receipt["block_number"])
            timestamp_iso = datetime.fromtimestamp(block["timestamp"]).isoformat()

            return {
                "token_id": token_id,
                "transaction_hash": receipt["transaction_hash"],
                "block_number": receipt["block_number"],
                "gas_used": receipt["gas_used"],
                "timestamp": timestamp_iso,
            }

        except Exception as e:
            raise Exception(f"Failed to mint ticket: {str(e)}") from e

    async def check_in_ticket(self, token_id: int) -> dict[str, Any]:
        """Check in a ticket by updating its on-chain state."""
        try:
            # Call the checkIn function
            func = self.contract.functions.checkIn(token_id)

            # Send transaction
            receipt = await self._send_transaction(func)

            block = self.w3.eth.get_block(receipt["block_number"])
            timestamp_iso = datetime.fromtimestamp(block["timestamp"]).isoformat()

            return {
                "transaction_hash": receipt["transaction_hash"],
                "block_number": receipt["block_number"],
                "gas_used": receipt["gas_used"],
                "timestamp": timestamp_iso,
                "new_status": "CheckedIn",
            }

        except Exception as e:
            raise Exception(f"Failed to check in ticket: {str(e)}") from e

    async def invalidate_ticket(self, token_id: int) -> dict[str, Any]:
        """Invalidate a ticket by updating its on-chain state."""
        try:
            # Call the invalidate function
            func = self.contract.functions.invalidate(token_id)

            # Send transaction
            receipt = await self._send_transaction(func)

            block = self.w3.eth.get_block(receipt["block_number"])
            timestamp_iso = datetime.fromtimestamp(block["timestamp"]).isoformat()

            return {
                "transaction_hash": receipt["transaction_hash"],
                "block_number": receipt["block_number"],
                "gas_used": receipt["gas_used"],
                "timestamp": timestamp_iso,
                "new_status": "Invalidated",
            }

        except Exception as e:
            raise Exception(f"Failed to invalidate ticket: {str(e)}") from e

    async def transfer_ticket(
        self,
        token_id: int,
        from_address: str,
        to_address: str,
    ) -> dict[str, Any]:
        """Transfer a ticket NFT from one address to another."""
        try:
            # Use owner-controlled transfer function
            func = self.contract.functions.ownerTransfer(
                Web3.to_checksum_address(from_address),
                Web3.to_checksum_address(to_address),
                token_id,
            )

            # Send transaction
            receipt = await self._send_transaction(func)

            block = self.w3.eth.get_block(receipt["block_number"])
            timestamp_iso = datetime.fromtimestamp(block["timestamp"]).isoformat()

            return {
                "transaction_hash": receipt["transaction_hash"],
                "block_number": receipt["block_number"],
                "gas_used": receipt["gas_used"],
                "timestamp": timestamp_iso,
                "from": from_address,
                "to": to_address,
            }

        except Exception as e:
            raise Exception(f"Failed to transfer ticket: {str(e)}") from e

    async def get_ticket_status(self, token_id: int) -> str:
        """Get the current status of a ticket."""
        try:
            # Call the ticketStatuses mapping
            status_code = self.contract.functions.ticketStatuses(token_id).call()

            # Map status code to string
            status_map = {
                0: "Valid",
                1: "CheckedIn",
                2: "Invalidated",
            }

            return str(status_map.get(status_code, "Unknown"))

        except Exception as e:
            raise Exception(f"Failed to get ticket status: {str(e)}") from e

    async def get_ticket_owner(self, token_id: int) -> str:
        """Get the current owner of a ticket."""
        try:
            # Call the ownerOf function
            owner = self.contract.functions.ownerOf(token_id).call()
            return str(owner)

        except Exception as e:
            raise Exception(f"Failed to get ticket owner: {str(e)}") from e
