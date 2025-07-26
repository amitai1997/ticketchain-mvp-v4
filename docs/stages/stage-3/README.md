# Stage 3: Off-Chain Core & Blockchain Integration

## Overview

Stage 3 implements the backend API that serves as the bridge between users and the blockchain. This stage establishes the API structure, defines blockchain interaction patterns, and creates a complete off-chain orchestration layer.

## Phase 1: API Scaffolding & Blockchain Service Interface ✅

### What Was Built

1. **Pydantic Models** (`src/api/models.py`):
   - Request models for all ticket operations (sold, resold, checked-in, invalidated)
   - Response models with blockchain transaction details
   - Enum for ticket status matching smart contract states

2. **Blockchain Service Interface** (`src/blockchain_service/interface.py`):
   - Abstract base class defining the contract for blockchain interactions
   - Methods for minting, transferring, and state management
   - Clear separation between API logic and blockchain implementation

3. **Mock Blockchain Service** (`src/blockchain_service/mock_service.py`):
   - In-memory implementation for development and testing
   - Returns realistic blockchain responses (transaction hashes, gas usage)
   - Maintains ticket state for testing workflows

4. **Ticket API Router** (`src/api/tickets.py`):
   - RESTful endpoints following OPEN Ticketing patterns
   - Dependency injection for blockchain service
   - Comprehensive error handling and HTTP status codes

### API Endpoints

- `POST /api/v1/tickets/sold` - Mint a new ticket NFT
- `POST /api/v1/tickets/resold` - Transfer ticket ownership
- `POST /api/v1/tickets/checked-in` - Mark ticket as used
- `POST /api/v1/tickets/invalidated` - Cancel/refund ticket

### Testing Phase 1

```bash
# Start the API server
poetry run uvicorn src.api.main:app --reload

# Test minting a ticket
curl -X POST http://localhost:8000/api/v1/tickets/sold \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "event-123",
    "ticket_id": "ticket-001",
    "user_id": "user-456",
    "price": 1000000000000000000,
    "to_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f89ed0",
    "name": "VIP Ticket"
  }'

# View API documentation
open http://localhost:8000/docs
```

## Phase 2: Web3 Integration Layer (In Progress)

### What Will Be Built

1. **Concrete Blockchain Service**:
   - Web3.py connection to Hardhat node
   - Contract ABI loading from artifacts
   - Transaction signing and gas estimation
   - Receipt polling and error handling

2. **Environment Configuration**:
   - Private key management via .env
   - RPC endpoint configuration
   - Contract address management

3. **API Integration**:
   - Replace mock service with real implementation
   - Add transaction monitoring
   - Implement retry logic for failed transactions

## Phase 3: Integration Testing & CI (Planned)

### What Will Be Built

1. **End-to-End Tests**:
   - Full workflow from API to blockchain
   - State verification on-chain
   - Error scenario testing

2. **CI Pipeline Updates**:
   - Docker Compose for test environment
   - Parallel test execution
   - Coverage reporting

## Phase 4: Docker Polish & Documentation (Planned)

### What Will Be Built

1. **Docker Improvements**:
   - Service orchestration
   - Health checks
   - Volume management

2. **Documentation**:
   - API usage guide
   - Deployment instructions
   - Architecture diagrams

## Key Design Decisions

### API Structure
- **RESTful Design**: Following standard HTTP verbs and status codes
- **OPEN Compatibility**: Endpoint names match OPEN Ticketing patterns
- **Async First**: All endpoints are async for better performance

### Blockchain Integration
- **Service Pattern**: Abstract interface allows easy testing and future chain switching
- **Dependency Injection**: Clean separation of concerns
- **Error Handling**: Comprehensive error responses for blockchain failures

### Security Considerations
- **Address Validation**: Will be added in Phase 2
- **Transaction Signing**: Backend holds admin key for contract operations
- **Rate Limiting**: To be added in future stages

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  FastAPI    │────▶│ Blockchain  │
│             │     │   Router    │     │  Service    │
└─────────────┘     └─────────────┘     └─────────────┘
                            │                    │
                            ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Pydantic   │     │   Web3.py   │
                    │   Models    │     │             │
                    └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Hardhat    │
                                        │    Node     │
                                        └─────────────┘
```

## Next Steps

1. Complete Phase 2 by implementing the real blockchain service
2. Add comprehensive integration tests
3. Update Docker Compose for full stack development
4. Add API authentication and rate limiting