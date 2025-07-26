"""
Configuration management for TicketChain backend.
"""

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Blockchain Configuration
    deployer_private_key: str = (
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    )
    rpc_url: str = "http://localhost:8545"
    chain_id: int = 31337

    # Contract Configuration
    ticket_contract_address: str = ""
    ticket_contract_abi_path: str = "artifacts/contracts/Ticket.sol/Ticket.json"

    # Database Configuration
    database_url: str = "sqlite:///./data/ticketchain.db"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


# Global settings instance
settings = Settings()


def get_contract_abi() -> list:
    """Load the Ticket contract ABI from the artifacts."""
    import json

    abi_path = Path(settings.ticket_contract_abi_path)
    if not abi_path.exists():
        raise FileNotFoundError(f"Contract ABI not found at {abi_path}")

    with open(abi_path) as f:
        contract_json = json.load(f)

    abi = contract_json.get("abi", [])
    if not isinstance(abi, list):
        raise ValueError(f"Invalid ABI format in {abi_path}")
    return abi
