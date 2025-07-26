#!/usr/bin/env python3
"""
End-to-end test script for TicketChain integration.

This script demonstrates the complete ticket lifecycle:
1. Minting a ticket NFT
2. Transferring (reselling) the ticket
3. Checking in the ticket
4. Invalidating a ticket

Run this with both Hardhat node and API server running.
"""

import asyncio
import sys
from datetime import datetime

import httpx


async def test_ticket_lifecycle():
    """Test the complete ticket lifecycle with real blockchain integration."""

    # Configuration
    api_base = "http://localhost:8000"

    print("🎫 TicketChain End-to-End Integration Test")
    print("=" * 50)

    async with httpx.AsyncClient(base_url=api_base, timeout=30.0) as client:

        # Test 1: Mint a ticket
        print("\n📝 Step 1: Minting a new ticket...")
        mint_data = {
            "event_id": "blockchain-conference-2024",
            "ticket_id": f"ticket-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "user_id": "alice@example.com",
            "price": 1000000000000000000,  # 1 ETH
            "to_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
            "name": "Blockchain Conference 2024 - VIP Pass",
            "description": "VIP access to all sessions and networking events",
        }

        response = await client.post("/api/v1/tickets/sold", json=mint_data)

        if response.status_code != 201:
            print(f"❌ Minting failed: {response.status_code} - {response.text}")
            return False

        mint_result = response.json()
        token_id = mint_result["token_id"]
        ticket_id = mint_result["ticket_id"]

        print("✅ Ticket minted successfully!")
        print(f"   Token ID: {token_id}")
        print(f"   Transaction: {mint_result['transaction_hash']}")
        print(f"   Owner: {mint_result['owner_address']}")

        # Test 2: Resell the ticket
        print("\n💰 Step 2: Reselling the ticket...")
        resale_data = {
            "ticket_id": ticket_id,
            "user_id": "bob@example.com",
            "price": 1500000000000000000,  # 1.5 ETH
            "to_address": "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC",
        }

        response = await client.post("/api/v1/tickets/resold", json=resale_data)

        if response.status_code != 200:
            print(f"❌ Resale failed: {response.status_code} - {response.text}")
            return False

        resale_result = response.json()
        print("✅ Ticket resold successfully!")
        print(f"   New owner: {resale_result['owner_address']}")
        print(f"   Transaction: {resale_result['transaction_hash']}")

        # Test 3: Check in the ticket
        print("\n🎟️ Step 3: Checking in the ticket...")
        checkin_data = {"ticket_id": ticket_id}

        response = await client.post("/api/v1/tickets/checked-in", json=checkin_data)

        if response.status_code != 200:
            print(f"❌ Check-in failed: {response.status_code} - {response.text}")
            return False

        checkin_result = response.json()
        print("✅ Ticket checked in successfully!")
        print(f"   Status: {checkin_result['status']}")
        print(f"   Transaction: {checkin_result['transaction_hash']}")

        # Test 4: Mint and invalidate another ticket
        print("\n❌ Step 4: Testing ticket invalidation...")
        invalidate_mint_data = {
            "event_id": "canceled-event-2024",
            "ticket_id": f"invalid-ticket-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "user_id": "charlie@example.com",
            "price": 500000000000000000,  # 0.5 ETH
            "to_address": "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65",
            "name": "Canceled Event Ticket",
            "description": "This event was unfortunately canceled",
        }

        response = await client.post("/api/v1/tickets/sold", json=invalidate_mint_data)
        if response.status_code != 201:
            print("❌ Failed to mint ticket for invalidation test")
            return False

        invalid_ticket = response.json()

        # Now invalidate it
        invalidate_data = {"ticket_id": invalid_ticket["ticket_id"]}
        response = await client.post(
            "/api/v1/tickets/invalidated", json=invalidate_data
        )

        if response.status_code != 200:
            print(f"❌ Invalidation failed: {response.status_code} - {response.text}")
            return False

        invalidate_result = response.json()
        print("✅ Ticket invalidated successfully!")
        print(f"   Status: {invalidate_result['status']}")
        print(f"   Transaction: {invalidate_result['transaction_hash']}")

        print(
            "\n🎉 All tests passed! The TicketChain integration is working correctly."
        )
        print("\nSummary:")
        print(f"✅ Minted ticket {token_id}")
        print("✅ Transferred to new owner")
        print("✅ Checked in for event")
        print("✅ Invalidated canceled ticket")

        return True


async def main():
    """Main function to run the test."""
    try:
        success = await test_ticket_lifecycle()
        if success:
            print("\n🚀 Integration test completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Integration test failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
