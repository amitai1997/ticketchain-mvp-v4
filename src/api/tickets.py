"""
Tickets API router for TicketChain.
"""

import json
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..blockchain_service.interface import BlockchainServiceInterface
from ..blockchain_service.mock_service import MockBlockchainService
from ..datastore.ticket_registry import ticket_registry as registry
from .models import (
    CheckedInTicketRequest,
    ErrorResponse,
    InvalidateTicketRequest,
    ResoldTicketRequest,
    SoldTicketRequest,
    TicketResponse,
    TicketStatus,
)

router = APIRouter(
    prefix="/api/v1/tickets",
    tags=["tickets"],
    responses={
        404: {"model": ErrorResponse, "description": "Ticket not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)


# Dependency injection for blockchain service
async def get_blockchain_service() -> BlockchainServiceInterface:
    """
    Dependency injection for blockchain service.
    Returns mock service if no contract address is configured,
    otherwise returns the real Web3 implementation.
    """
    import traceback

    from ..blockchain_service import Web3BlockchainService
    from ..config import settings

    # Use real service if contract address is configured
    if settings.ticket_contract_address:
        try:
            print("🔍 DEBUG: Environment variables:")
            print(f"  - RPC URL: {settings.rpc_url}")
            print(f"  - Contract Address: {settings.ticket_contract_address}")
            print(f"  - Chain ID: {settings.chain_id}")
            print(
                f"  - Deployer key set: {'YES' if settings.deployer_private_key else 'NO'}"
            )

            print(
                f"Attempting to initialize Web3BlockchainService with address: {settings.ticket_contract_address}"
            )
            service = Web3BlockchainService()
            print("✅ Web3BlockchainService initialized successfully")
            return service
        except Exception as e:
            print(f"❌ Failed to initialize Web3 service: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Traceback: {traceback.format_exc()}")
            print("⚠️  Falling back to mock service")
            return MockBlockchainService()
    else:
        print("ℹ️  No contract address configured, using mock service")
        return MockBlockchainService()


@router.post(
    "/sold", response_model=TicketResponse, status_code=status.HTTP_201_CREATED
)
async def sold_ticket(
    request: SoldTicketRequest,
    blockchain_service: Annotated[
        BlockchainServiceInterface, Depends(get_blockchain_service)
    ],
) -> TicketResponse:
    """
    Mint a new ticket NFT when a ticket is sold.

    This endpoint:
    - Creates a new NFT on the blockchain
    - Assigns it to the specified user address
    - Returns the ticket details including the on-chain token ID
    """
    try:
        # Create metadata URI (in production, this would be uploaded to IPFS or similar)
        metadata = {
            "name": request.name or f"Ticket #{request.ticket_id}",
            "description": request.description
            or f"Ticket for event {request.event_id}",
            "image": request.image_url,
            "attributes": request.metadata_attributes or {},
            "event_id": request.event_id,
            "ticket_id": request.ticket_id,
        }
        token_uri = (
            f"data:application/json;base64,{json.dumps(metadata).encode().hex()}"
        )

        # Mint the ticket on-chain
        result = await blockchain_service.mint_ticket(
            to_address=request.to_address,
            token_uri=token_uri,
        )

        # Store mapping for later operations
        registry.register_ticket(request.ticket_id, result["token_id"])

        return TicketResponse(
            ticket_id=request.ticket_id,
            token_id=result["token_id"],
            event_id=request.event_id,
            status=TicketStatus.VALID,
            owner_address=request.to_address,
            transaction_hash=result["transaction_hash"],
            timestamp=datetime.fromisoformat(result["timestamp"]),
            message="Ticket successfully minted",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mint ticket: {str(e)}",
        ) from e


@router.post("/resold", response_model=TicketResponse)
async def resold_ticket(
    request: ResoldTicketRequest,
    blockchain_service: Annotated[
        BlockchainServiceInterface, Depends(get_blockchain_service)
    ],
) -> TicketResponse:
    """
    Handle secondary market ticket resale.

    This endpoint:
    - Transfers the NFT from the current owner to the new owner
    - Records the resale transaction on-chain
    """
    try:
        # Look up token ID
        if not registry.exists(request.ticket_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket {request.ticket_id} not found",
            )

        token_id = registry.get_token_id(request.ticket_id)
        if token_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token ID not found for ticket {request.ticket_id}",
            )

        # Get current owner
        current_owner = await blockchain_service.get_ticket_owner(token_id)

        # Transfer the ticket
        result = await blockchain_service.transfer_ticket(
            token_id=token_id,
            from_address=current_owner,
            to_address=request.to_address,
        )

        # Get current status
        status_str = await blockchain_service.get_ticket_status(token_id)

        return TicketResponse(
            ticket_id=request.ticket_id,
            token_id=token_id,
            event_id="unknown",  # In production, this would be fetched from metadata
            status=TicketStatus(status_str.lower()),
            owner_address=request.to_address,
            transaction_hash=result["transaction_hash"],
            timestamp=datetime.fromisoformat(result["timestamp"]),
            message="Ticket successfully transferred",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resell ticket: {str(e)}",
        ) from e


@router.post("/checked-in", response_model=TicketResponse)
async def checked_in_ticket(
    request: CheckedInTicketRequest,
    blockchain_service: Annotated[
        BlockchainServiceInterface, Depends(get_blockchain_service)
    ],
) -> TicketResponse:
    """
    Check in a ticket at the event.

    This endpoint:
    - Updates the ticket state on-chain to CheckedIn
    - Prevents the ticket from being used again
    """
    try:
        # Look up token ID
        if not registry.exists(request.ticket_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket {request.ticket_id} not found",
            )

        token_id = registry.get_token_id(request.ticket_id)
        if token_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token ID not found for ticket {request.ticket_id}",
            )

        # Check in the ticket
        result = await blockchain_service.check_in_ticket(token_id)

        # Get owner
        owner = await blockchain_service.get_ticket_owner(token_id)

        return TicketResponse(
            ticket_id=request.ticket_id,
            token_id=token_id,
            event_id="unknown",  # In production, this would be fetched from metadata
            status=TicketStatus.CHECKED_IN,
            owner_address=owner,
            transaction_hash=result["transaction_hash"],
            timestamp=datetime.fromisoformat(result["timestamp"]),
            message="Ticket successfully checked in",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check in ticket: {str(e)}",
        ) from e


@router.post("/invalidated", response_model=TicketResponse)
async def invalidate_ticket(
    request: InvalidateTicketRequest,
    blockchain_service: Annotated[
        BlockchainServiceInterface, Depends(get_blockchain_service)
    ],
) -> TicketResponse:
    """
    Invalidate a ticket (e.g., for refunds or cancellations).

    This endpoint:
    - Updates the ticket state on-chain to Invalidated
    - Prevents the ticket from being used or transferred
    """
    try:
        # Look up token ID
        if not registry.exists(request.ticket_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket {request.ticket_id} not found",
            )

        token_id = registry.get_token_id(request.ticket_id)
        if token_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token ID not found for ticket {request.ticket_id}",
            )

        # Invalidate the ticket
        result = await blockchain_service.invalidate_ticket(token_id)

        # Get owner
        owner = await blockchain_service.get_ticket_owner(token_id)

        return TicketResponse(
            ticket_id=request.ticket_id,
            token_id=token_id,
            event_id="unknown",  # In production, this would be fetched from metadata
            status=TicketStatus.INVALIDATED,
            owner_address=owner,
            transaction_hash=result["transaction_hash"],
            timestamp=datetime.fromisoformat(result["timestamp"]),
            message="Ticket successfully invalidated",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invalidate ticket: {str(e)}",
        ) from e
