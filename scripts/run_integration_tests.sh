#!/bin/bash
# Script to run integration tests with proper setup

set -e

# Source common utilities
source "$(dirname "$0")/_common.sh"

echo "🧪 Running TicketChain Integration Tests"
echo "========================================"

# Check if Hardhat node is running
check_hardhat_node || exit 1

# Check if contract is deployed
if [ -z "$TICKET_CONTRACT_ADDRESS" ] && [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Contract not deployed. Deploying now...${NC}"
    npx hardhat run scripts/deploy.js --network localhost

    # Load the newly created .env file
    load_env_file && echo -e "${GREEN}✅ Contract deployed to: $TICKET_CONTRACT_ADDRESS${NC}"
elif [ -f ".env" ] && [ -z "$TICKET_CONTRACT_ADDRESS" ]; then
    # Load from .env if available
    load_env_file && echo -e "${GREEN}✅ Using existing contract at: $TICKET_CONTRACT_ADDRESS${NC}"
fi

# Check if API is running
if ! check_api_health; then
    echo -e "${YELLOW}⚠️  API server is not running. Starting it...${NC}"

    # Load .env to ensure the API gets the contract address
    load_env_file
    echo -e "${GREEN}📋 Starting API with contract address: $TICKET_CONTRACT_ADDRESS${NC}"

    # Export the variable so it's available to the subprocess
    export TICKET_CONTRACT_ADDRESS
    poetry run uvicorn src.api.main:app --reload &
    API_PID=$!

    # Wait for API to start
    if ! wait_for_service "API server" "check_api_health" 30 1; then
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
