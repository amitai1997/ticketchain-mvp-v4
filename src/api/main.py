"""
Main FastAPI application for TicketChain backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .tickets import router as tickets_router

# Create FastAPI app instance
app = FastAPI(
    title="TicketChain API",
    description="Blockchain-based ticketing system API",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tickets_router)


@app.get("/")
async def root() -> dict:
    """Root endpoint - health check."""
    return {"message": "Hello from TicketChain API", "status": "healthy"}


@app.get("/api/v1/health")
async def health_check() -> dict:
    """Health check endpoint."""
    from ..config import settings
    from .tickets import get_blockchain_service

    # Get blockchain service info for debugging
    blockchain_service = await get_blockchain_service()
    service_type = type(blockchain_service).__name__

    return {
        "status": "healthy",
        "service": "ticketchain-api",
        "version": "0.1.0",
        "blockchain_service": service_type,
        "contract_address": settings.ticket_contract_address,
    }
