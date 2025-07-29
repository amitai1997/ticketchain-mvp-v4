#!/bin/bash

# Health Check Utilities - DRY Compliant
# Sources _common.sh to avoid duplication and extends with specific functionality

set -e

# Source common utilities (DRY principle - reuse existing code)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_common.sh"

# Constants (extending common utilities)
API_URL="http://localhost:8000"
RPC_URL="http://localhost:8545"
HEALTH_ENDPOINT="/api/v1/health"

# Enhanced wait function specifically for API (extends wait_for_service from _common.sh)
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

# Export additional functions (common functions already exported by _common.sh)
export -f wait_for_api
