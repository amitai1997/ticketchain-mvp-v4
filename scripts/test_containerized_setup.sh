#!/bin/bash

set -e

echo "🐳 Testing Containerized TicketChain Setup"
echo "==========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_step() {
    echo -e "${YELLOW}Testing: $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

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
HEALTH_RESPONSE=$(curl -s http://localhost:8000/api/v1/health)
if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    success "API health check passed"
    echo "Contract address: $(echo "$HEALTH_RESPONSE" | jq -r '.contract_address')"
else
    error "API health check failed"
fi

# Test blockchain connectivity
test_step "Blockchain connectivity"
RPC_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"net_version","params":[],"id":1}' \
    http://localhost:8545)
if echo "$RPC_RESPONSE" | grep -q '"result":"31337"'; then
    success "Blockchain RPC connection successful"
else
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
