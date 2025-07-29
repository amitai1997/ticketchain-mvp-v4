"""
Integration tests for the complete ticket lifecycle.

These tests verify that the API correctly interacts with the blockchain,
testing the full flow from ticket minting to check-in.
"""

import os

import httpx
import pytest
from eth_account import Account
from web3 import Web3

# Test configuration
API_BASE_URL = "http://localhost:8000"
TEST_PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
TEST_ACCOUNT = Account.from_key(TEST_PRIVATE_KEY)


@pytest.fixture(scope="session")
def w3():
    """Web3 instance connected to local Hardhat node."""
    web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    assert web3.is_connected(), "Hardhat node not running"
    return web3


@pytest.fixture(scope="session")
def contract_address():
    """Get the deployed contract address from environment."""
    address = os.getenv("TICKET_CONTRACT_ADDRESS")
    if not address:
        pytest.skip("TICKET_CONTRACT_ADDRESS not set - run deploy.js first")
    return address


@pytest.fixture(scope="session")
def ticket_contract(w3, contract_address):
    """Load the Ticket contract instance."""
    from src.config import get_contract_abi

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(contract_address), abi=get_contract_abi()
    )
    return contract


@pytest.fixture
async def api_client():
    """Async HTTP client for API testing."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        yield client


@pytest.mark.asyncio
class TestTicketLifecycle:
    """Test the complete ticket lifecycle from minting to check-in."""

    async def test_full_ticket_lifecycle(self, api_client, w3, ticket_contract):
        """Test minting, checking status, and checking in a ticket."""

        # Test data
        ticket_data = {
            "event_id": "test-event-001",
            "ticket_id": "test-ticket-001",
            "user_id": "test-user-001",
            "price": 1000000000000000000,  # 1 ETH in wei
            "to_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",  # Hardhat account #1
            "name": "Integration Test Ticket",
            "description": "Ticket for integration testing",
        }

        # Step 1: Mint a ticket via API
        response = await api_client.post("/api/v1/tickets/sold", json=ticket_data)
        assert response.status_code == 201
        mint_result = response.json()

        # Verify response structure
        assert "token_id" in mint_result
        assert "transaction_hash" in mint_result
        assert mint_result["ticket_id"] == ticket_data["ticket_id"]
        assert mint_result["status"] == "valid"

        token_id = mint_result["token_id"]

        # Step 2: Verify on-chain state
        # Check owner
        on_chain_owner = ticket_contract.functions.ownerOf(token_id).call()
        assert on_chain_owner.lower() == ticket_data["to_address"].lower()

        # Check status
        on_chain_status = ticket_contract.functions.ticketStatuses(token_id).call()
        assert on_chain_status == 0  # Valid = 0

        # Step 3: Check in the ticket via API
        checkin_data = {"ticket_id": ticket_data["ticket_id"]}

        response = await api_client.post(
            "/api/v1/tickets/checked-in", json=checkin_data
        )
        assert response.status_code == 200
        checkin_result = response.json()

        assert checkin_result["status"] == "checked_in"
        assert checkin_result["token_id"] == token_id

        # Step 4: Verify on-chain state changed
        on_chain_status = ticket_contract.functions.ticketStatuses(token_id).call()
        assert on_chain_status == 1  # CheckedIn = 1

    async def test_ticket_resale(self, api_client, w3, ticket_contract):
        """Test ticket resale functionality."""

        # First, mint a ticket
        mint_data = {
            "event_id": "test-event-002",
            "ticket_id": "test-ticket-resale-001",
            "user_id": "original-owner",
            "price": 2000000000000000000,  # 2 ETH
            "to_address": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",  # Hardhat account #2
            "name": "Resale Test Ticket",
        }

        response = await api_client.post("/api/v1/tickets/sold", json=mint_data)
        assert response.status_code == 201
        token_id = response.json()["token_id"]

        # Resell the ticket
        resale_data = {
            "ticket_id": mint_data["ticket_id"],
            "user_id": "new-owner",
            "price": 3000000000000000000,  # 3 ETH
            "to_address": "0x90F79bf6EB2c4f870365E785982E1f101E93b906",  # Hardhat account #3
        }

        response = await api_client.post("/api/v1/tickets/resold", json=resale_data)
        assert response.status_code == 200
        resale_result = response.json()

        assert (
            resale_result["owner_address"].lower() == resale_data["to_address"].lower()
        )

        # Verify on-chain ownership change
        on_chain_owner = ticket_contract.functions.ownerOf(token_id).call()
        assert on_chain_owner.lower() == resale_data["to_address"].lower()

    async def test_ticket_invalidation(self, api_client, w3, ticket_contract):
        """Test ticket invalidation."""

        # Mint a ticket
        mint_data = {
            "event_id": "test-event-003",
            "ticket_id": "test-ticket-invalid-001",
            "user_id": "test-user",
            "price": 500000000000000000,  # 0.5 ETH
            "to_address": "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65",  # Hardhat account #4
            "name": "Invalidation Test Ticket",
        }

        response = await api_client.post("/api/v1/tickets/sold", json=mint_data)
        assert response.status_code == 201
        token_id = response.json()["token_id"]

        # Invalidate the ticket
        invalidate_data = {"ticket_id": mint_data["ticket_id"]}

        response = await api_client.post(
            "/api/v1/tickets/invalidated", json=invalidate_data
        )
        assert response.status_code == 200
        result = response.json()

        assert result["status"] == "invalidated"

        # Verify on-chain status
        on_chain_status = ticket_contract.functions.ticketStatuses(token_id).call()
        assert on_chain_status == 2  # Invalidated = 2

    async def test_error_handling(self, api_client):
        """Test API error handling for invalid operations."""

        # Try to check in a non-existent ticket
        response = await api_client.post(
            "/api/v1/tickets/checked-in", json={"ticket_id": "non-existent-ticket"}
        )
        assert response.status_code == 404

        # Try to resell a non-existent ticket
        response = await api_client.post(
            "/api/v1/tickets/resold",
            json={
                "ticket_id": "non-existent-ticket",
                "user_id": "user",
                "price": 1000000000000000000,
                "to_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
            },
        )
        assert response.status_code == 404
