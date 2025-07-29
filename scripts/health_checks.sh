#!/bin/bash

# Health Check Utilities - Single Source of Truth
# Following DRY principles - centralized health check functions

set -e

# Constants
API_URL="http://localhost:8000"
RPC_URL="http://localhost:8545"
HEALTH_ENDPOINT="/api/v1/health"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Utility functions
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Health check functions
check_api_health() {
    local response
    response=$(curl -s "${API_URL}${HEALTH_ENDPOINT}" 2>/dev/null || echo "")

    if echo "$response" | grep -q '"status":"healthy"'; then
        success "API health check passed"
        echo "$response"
        return 0
    else
        error "API health check failed"
        return 1
    fi
}

check_blockchain_connectivity() {
    local response
    response=$(curl -s -X POST -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"net_version","params":[],"id":1}' \
        "${RPC_URL}" 2>/dev/null || echo "")

    if echo "$response" | grep -q '"result":"31337"'; then
        success "Blockchain RPC connection successful"
        return 0
    else
        error "Blockchain RPC connection failed"
        return 1
    fi
}

get_contract_address() {
    local response
    response=$(curl -s "${API_URL}${HEALTH_ENDPOINT}" 2>/dev/null || echo "")
    echo "$response" | jq -r '.contract_address' 2>/dev/null || echo ""
}

wait_for_api() {
    local max_attempts=30
    local attempt=1

    info "Waiting for API to be ready..."

    while [ $attempt -le $max_attempts ]; do
        if check_api_health >/dev/null 2>&1; then
            success "API is ready"
            return 0
        fi

        sleep 2
        attempt=$((attempt + 1))
    done

    error "API failed to start within timeout"
    return 1
}

# Export functions for use in other scripts
export -f check_api_health
export -f check_blockchain_connectivity
export -f get_contract_address
export -f wait_for_api
export -f success
export -f error
export -f info
