"""
Main FastAPI application for TicketChain backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def root() -> dict:
    """Root endpoint - health check."""
    return {"message": "Hello from TicketChain API", "status": "healthy"}


@app.get("/api/v1/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "ticketchain-api", "version": "0.1.0"}
