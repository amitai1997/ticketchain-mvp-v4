"""
Pydantic models for TicketChain API requests and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    """Ticket lifecycle states matching the smart contract."""

    VALID = "valid"
    CHECKED_IN = "checked_in"
    INVALIDATED = "invalidated"


class SoldTicketRequest(BaseModel):
    """Request model for minting/selling a new ticket."""

    event_id: str = Field(..., description="Unique identifier for the event")
    ticket_id: str = Field(..., description="Unique identifier for the ticket")
    user_id: str = Field(..., description="User ID who is purchasing the ticket")
    price: int = Field(..., ge=0, description="Ticket price in wei")
    to_address: str = Field(..., description="Ethereum address to mint the ticket to")
    name: Optional[str] = Field(None, description="Ticket name/type")
    description: Optional[str] = Field(None, description="Ticket description")
    image_url: Optional[str] = Field(None, description="URL to ticket image")
    metadata_attributes: Optional[dict] = Field(None, description="Additional metadata")


class ResoldTicketRequest(BaseModel):
    """Request model for reselling a ticket."""

    ticket_id: str = Field(..., description="Unique identifier for the ticket")
    user_id: str = Field(..., description="User ID of the new owner")
    price: int = Field(..., ge=0, description="Resale price in wei")
    to_address: str = Field(..., description="Ethereum address of new owner")


class CheckedInTicketRequest(BaseModel):
    """Request model for checking in a ticket."""

    ticket_id: str = Field(..., description="Unique identifier for the ticket")


class InvalidateTicketRequest(BaseModel):
    """Request model for invalidating a ticket."""

    ticket_id: str = Field(..., description="Unique identifier for the ticket")


class TicketResponse(BaseModel):
    """Response model for ticket operations."""

    ticket_id: str
    token_id: int = Field(..., description="On-chain NFT token ID")
    event_id: str
    status: TicketStatus
    owner_address: str
    transaction_hash: str
    timestamp: datetime
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    detail: Optional[str] = None
    status_code: int
