"""
Configuration module for TicketChain application.

This module handles all environment variable configuration
using Pydantic Settings for type safety and validation.
"""

from typing import Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Blockchain Configuration
    deployer_private_key: Optional[str] = None
    rpc_url: str = "http://localhost:8545"
    chain_id: int = 31337

    # Contract Configuration
    ticket_contract_address: Optional[str] = None
    ticket_contract_abi_path: str = "artifacts/contracts/Ticket.sol/Ticket.json"

    # Deployment Information
    deployment_network: str = "localhost"
    deployment_contract_address: Optional[str] = None
    deployment_deployer_address: Optional[str] = None
    deployment_timestamp: Optional[str] = None

    # Database Configuration
    database_url: str = "sqlite:///./data/ticketchain.db"

    # Registry Configuration
    ticket_registry_path: Optional[str] = None  # None means in-memory only


# Global settings instance
settings = Settings()