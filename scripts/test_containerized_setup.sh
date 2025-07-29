#!/bin/bash

set -e

# Source shared health check utilities (DRY principle)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/health_checks.sh"

echo "🐳 Testing Containerized TicketChain Setup"
echo "==========================================="

# Test function
test_step() {
    echo -e "${YELLOW}Testing: $1${NC}"
}

# Override error function to exit on failure
error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Check if docker compose is running
test_step "Docker services status"
if docker compose ps | grep -q "Up"; then
    success "Docker services are running"
else
    error "Docker services are not running properly"
fi

# Test API health
test_step "API health endpoint"
if check_api_health >/dev/null; then
    CONTRACT_ADDRESS=$(get_contract_address)
    echo "Contract address: $CONTRACT_ADDRESS"
else
    error "API health check failed"
fi

# Test blockchain connectivity
test_step "Blockchain connectivity"
if ! check_blockchain_connectivity >/dev/null; then
    error "Blockchain RPC connection failed"
fi

# Test ticket minting
test_step "Ticket minting functionality"
MINT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/tickets/sold \
    -H "Content-Type: application/json" \
    -d '{
        "event_id": "container-test-event",
        "ticket_id": "container-test-ticket-'$(date +%s)'",
        "user_id": "container-test-user",
        "price": 1000000000000000000,
        "to_address": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
        "name": "Container Test Ticket",
        "description": "Ticket for testing containerized setup"
    }')

if echo "$MINT_RESPONSE" | grep -q '"status":"valid"'; then
    success "Ticket minting successful"
    TOKEN_ID=$(echo "$MINT_RESPONSE" | jq -r '.token_id')
    echo "Minted token ID: $TOKEN_ID"
else
    error "Ticket minting failed: $MINT_RESPONSE"
fi

# Test ticket check-in
test_step "Ticket check-in functionality"
TICKET_ID=$(echo "$MINT_RESPONSE" | jq -r '.ticket_id')
CHECKIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/tickets/checked-in \
    -H "Content-Type: application/json" \
    -d "{\"ticket_id\": \"$TICKET_ID\"}")

if echo "$CHECKIN_RESPONSE" | grep -q '"status":"checked_in"'; then
    success "Ticket check-in successful"
else
    error "Ticket check-in failed: $CHECKIN_RESPONSE"
fi

echo ""
echo -e "${GREEN}🎉 All containerized setup tests passed!${NC}"
echo "The TicketChain application is working correctly in Docker containers."
