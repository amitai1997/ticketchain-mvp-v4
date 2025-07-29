# Stage 3 Quick Start Guide

This guide will help you run the complete TicketChain system with blockchain integration.

## Prerequisites

- Node.js >= 18.0.0
- Python >= 3.12
- Poetry installed
- npm/yarn installed

## Step 1: Install Dependencies

```bash
# Install Node dependencies
npm install

# Install Python dependencies
poetry install
```

## Step 2: Start Hardhat Node

Open a terminal and start the local blockchain:

```bash
npx hardhat node
```

Keep this terminal open. You should see:
```
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/
```

## Step 3: Deploy Contracts

In a new terminal, deploy the Ticket contract:

```bash
  npm run deploy:local
```

This will output a contract address. Copy it and add to your `.env` file:
```
TICKET_CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
```

## Step 4: Start the API Server

Start the FastAPI backend:

```bash
poetry run uvicorn src.api.main:app --reload
```

The API will be available at http://localhost:8000

## Step 5: Test the System

### Using the Mock Service (Default)

If no contract address is set, the API uses a mock blockchain service:

```bash
# Mint a ticket
curl -X POST http://localhost:8000/api/v1/tickets/sold \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "event-123",
    "ticket_id": "ticket-001",
    "user_id": "user-456",
    "price": 1000000000000000000,
    "to_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
    "name": "VIP Ticket"
  }'
```

### Using the Real Blockchain

After setting `TICKET_CONTRACT_ADDRESS` in your `.env`, restart the API server. Now it will use the real blockchain:

```bash
# The same curl command now creates a real NFT on the blockchain!
```

## Step 6: Check API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Available Endpoints

- `POST /api/v1/tickets/sold` - Mint a new ticket
- `POST /api/v1/tickets/resold` - Transfer ticket ownership
- `POST /api/v1/tickets/checked-in` - Check in a ticket
- `POST /api/v1/tickets/invalidated` - Invalidate a ticket

## Troubleshooting

### Connection Refused
If you get connection errors, make sure:
1. Hardhat node is running on port 8545
2. Contract is deployed and address is in `.env`
3. API server was restarted after updating `.env`

### Transaction Failed
Check that:
1. The deployer account has sufficient ETH
2. The contract address is correct
3. Token IDs exist before trying to transfer/check-in

## Next Steps

- Run integration tests: `poetry run pytest tests/integration`
- Use Docker Compose: `docker-compose up`
- Deploy to testnet: Update `RPC_URL` and `CHAIN_ID` in `.env`
