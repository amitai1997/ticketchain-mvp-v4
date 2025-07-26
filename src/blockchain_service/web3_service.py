"""
Web3 implementation of the blockchain service for real blockchain interactions.
"""

import asyncio
import json
from typing import Dict, Any, Optional
from datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

from .interface import BlockchainServiceInterface
from ..config import settings, get_contract_abi


class Web3BlockchainService(BlockchainServiceInterface):
    """Web3.py implementation for interacting with the Ticket smart contract."""
    
    def __init__(self, contract_address: Optional[str] = None):
        """
        Initialize the Web3 blockchain service.
        
        Args:
            contract_address: Address of the deployed Ticket contract.
                            If not provided, will use from settings.
        """
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(settings.rpc_url))
        
        # Add middleware for PoA networks (like some testnets)
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Check connection
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {settings.rpc_url}")
        
        # Set up account from private key
        self.account = Account.from_key(settings.deployer_private_key)
        
        # Load contract
        self.contract_address = contract_address or settings.ticket_contract_address
        if not self.contract_address:
            raise ValueError("Contract address not provided")
        
        # Initialize contract instance
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=get_contract_abi()
        )
        
        # Cache for gas prices
        self._last_gas_price = None
    
    async def _get_gas_price(self) -> int:
        """Get current gas price with caching."""
        # In production, implement proper caching with TTL
        if self._last_gas_price is None:
            self._last_gas_price = self.w3.eth.gas_price
        return self._last_gas_price
    
    async def _send_transaction(self, func) -> Dict[str, Any]:
        """
        Build, sign, and send a transaction.
        
        Args:
            func: Contract function to call
            
        Returns:
            Transaction receipt details
        """
        # Get gas price
        gas_price = await self._get_gas_price()
        
        # Build transaction
        tx = func.build_transaction({
            'from': self.account.address,
            'gas': 300000,  # Estimate in production
            'gasPrice': gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'chainId': settings.chain_id,
        })
        
        # Sign transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, settings.deployer_private_key)
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            'transaction_hash': receipt['transactionHash'].hex(),
            'block_number': receipt['blockNumber'],
            'gas_used': receipt['gasUsed'],
        }
    
    async def mint_ticket(
        self,
        to_address: str,
        token_uri: str,
    ) -> Dict[str, Any]:
        """Mint a new ticket NFT on the blockchain."""
        try:
            # Call the mintTicket function
            func = self.contract.functions.mintTicket(
                Web3.to_checksum_address(to_address),
                token_uri
            )
            
            # Send transaction
            receipt = await self._send_transaction(func)
            
            # Get the token ID from the event logs
            logs = self.contract.events.TicketMinted().process_receipt(
                self.w3.eth.get_transaction_receipt(receipt['transaction_hash'])
            )
            
            if logs:
                token_id = logs[0]['args']['tokenId']
            else:
                # Fallback: calculate token ID (assumes sequential minting)
                token_id = self.contract.functions.totalSupply().call() - 1
            
            return {
                'token_id': token_id,
                'transaction_hash': receipt['transaction_hash'],
                'block_number': receipt['block_number'],
                'gas_used': receipt['gas_used'],
                'timestamp': self.w3.eth.get_block(receipt['block_number'])['timestamp'],
            }
            
        except Exception as e:
            raise Exception(f"Failed to mint ticket: {str(e)}")
    
    async def check_in_ticket(self, token_id: int) -> Dict[str, Any]:
        """Check in a ticket by updating its on-chain state."""
        try:
            # Call the checkIn function
            func = self.contract.functions.checkIn(token_id)
            
            # Send transaction
            receipt = await self._send_transaction(func)
            
            return {
                'transaction_hash': receipt['transaction_hash'],
                'block_number': receipt['block_number'],
                'gas_used': receipt['gas_used'],
                'timestamp': self.w3.eth.get_block(receipt['block_number'])['timestamp'],
                'new_status': 'CheckedIn',
            }
            
        except Exception as e:
            raise Exception(f"Failed to check in ticket: {str(e)}")
    
    async def invalidate_ticket(self, token_id: int) -> Dict[str, Any]:
        """Invalidate a ticket by updating its on-chain state."""
        try:
            # Call the invalidate function
            func = self.contract.functions.invalidate(token_id)
            
            # Send transaction
            receipt = await self._send_transaction(func)
            
            return {
                'transaction_hash': receipt['transaction_hash'],
                'block_number': receipt['block_number'],
                'gas_used': receipt['gas_used'],
                'timestamp': self.w3.eth.get_block(receipt['block_number'])['timestamp'],
                'new_status': 'Invalidated',
            }
            
        except Exception as e:
            raise Exception(f"Failed to invalidate ticket: {str(e)}")
    
    async def transfer_ticket(
        self,
        token_id: int,
        from_address: str,
        to_address: str,
    ) -> Dict[str, Any]:
        """Transfer a ticket NFT from one address to another."""
        try:
            # For transferFrom, the transaction needs to come from an approved address
            # In production, implement proper approval flow
            func = self.contract.functions.transferFrom(
                Web3.to_checksum_address(from_address),
                Web3.to_checksum_address(to_address),
                token_id
            )
            
            # Send transaction
            receipt = await self._send_transaction(func)
            
            return {
                'transaction_hash': receipt['transaction_hash'],
                'block_number': receipt['block_number'],
                'gas_used': receipt['gas_used'],
                'timestamp': self.w3.eth.get_block(receipt['block_number'])['timestamp'],
                'from': from_address,
                'to': to_address,
            }
            
        except Exception as e:
            raise Exception(f"Failed to transfer ticket: {str(e)}")
    
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
            
            return status_map.get(status_code, "Unknown")
            
        except Exception as e:
            raise Exception(f"Failed to get ticket status: {str(e)}")
    
    async def get_ticket_owner(self, token_id: int) -> str:
        """Get the current owner of a ticket."""
        try:
            # Call the ownerOf function
            owner = self.contract.functions.ownerOf(token_id).call()
            return owner
            
        except Exception as e:
            raise Exception(f"Failed to get ticket owner: {str(e)}")