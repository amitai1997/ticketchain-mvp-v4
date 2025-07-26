#!/bin/bash
# Script to run integration tests with proper setup

set -e

echo "🧪 Running TicketChain Integration Tests"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Hardhat node is running
if ! curl -s http://localhost:8545 > /dev/null; then
    echo -e "${RED}❌ Hardhat node is not running!${NC}"
    echo "Please start it with: npx hardhat node"
    exit 1
fi
echo -e "${GREEN}✅ Hardhat node is running${NC}"

# Check if contract is deployed
if [ -z "$TICKET_CONTRACT_ADDRESS" ] && [ ! -f "data/deployment.json" ]; then
    echo -e "${YELLOW}⚠️  Contract not deployed. Deploying now...${NC}"
    npx hardhat run scripts/setup_dev.js --network localhost

    # Extract contract address from deployment.json
    if [ -f "data/deployment.json" ]; then
        export TICKET_CONTRACT_ADDRESS=$(grep -o '"contractAddress":"[^"]*' data/deployment.json | grep -o '[^"]*$')
        echo -e "${GREEN}✅ Contract deployed to: $TICKET_CONTRACT_ADDRESS${NC}"
    fi
fi

# Check if API is running
if ! curl -s http://localhost:8000/api/v1/health > /dev/null; then
    echo -e "${YELLOW}⚠️  API server is not running. Starting it...${NC}"
    poetry run uvicorn src.api.main:app --reload &
    API_PID=$!

    # Wait for API to start
    sleep 5

    if ! curl -s http://localhost:8000/api/v1/health > /dev/null; then
        echo -e "${RED}❌ Failed to start API server${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ API server started (PID: $API_PID)${NC}"
else
    echo -e "${GREEN}✅ API server is running${NC}"
fi

# Run integration tests
echo -e "\n${YELLOW}Running integration tests...${NC}"
poetry run pytest tests/integration -v --tb=short

# Cleanup
if [ ! -z "$API_PID" ]; then
    echo -e "\n${YELLOW}Stopping API server...${NC}"
    kill $API_PID 2>/dev/null || true
fi

echo -e "\n${GREEN}✨ Integration tests complete!${NC}"
