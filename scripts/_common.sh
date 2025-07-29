#!/bin/bash
# Common utilities for TicketChain scripts
# Source this file to access shared functions and constants

# Colors for output
export GREEN='\033[0;32m'
export RED='\033[0;31m'
export YELLOW='\033[1;33m'
export NC='\033[0m' # No Color

# Common function to check if Hardhat node is running
check_hardhat_node() {
    if ! curl -s http://localhost:8545 > /dev/null; then
        echo -e "${RED}❌ Hardhat node is not running!${NC}"
        echo "Please start it with: npx hardhat node"
        return 1
    fi
    echo -e "${GREEN}✅ Hardhat node is running${NC}"
    return 0
}

# Common function to check if API is running
check_api_health() {
    if ! curl -s http://localhost:8000/api/v1/health > /dev/null; then
        return 1
    fi
    return 0
}

# Common function to get API blockchain service type
get_api_service_type() {
    curl -s http://localhost:8000/api/v1/health 2>/dev/null | grep -o '"blockchain_service":"[^"]*"' | cut -d'"' -f4 || echo "unknown"
}

# Common function to check and display API service configuration
check_api_service_config() {
    if check_api_health; then
        SERVICE_TYPE=$(get_api_service_type)
        case "$SERVICE_TYPE" in
            "Web3BlockchainService")
                echo -e "${GREEN}✅ Running API is using Web3BlockchainService${NC}"
                return 0
                ;;
            "MockBlockchainService")
                echo -e "${YELLOW}⚠️  Running API is using MockBlockchainService (restart with contract address)${NC}"
                return 1
                ;;
            *)
                echo -e "ℹ️  API service type: $SERVICE_TYPE"
                return 0
                ;;
        esac
    else
        echo -e "ℹ️  API not running (will be configured properly when started)"
        return 1
    fi
}

# Common function to wait for service to be ready
wait_for_service() {
    local service_name="$1"
    local check_command="$2"
    local max_attempts="${3:-30}"
    local sleep_interval="${4:-2}"

    echo "Waiting for $service_name to be ready..."
    for i in $(seq 1 $max_attempts); do
        if eval "$check_command" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        echo "Waiting for $service_name... ($i/$max_attempts)"
        sleep $sleep_interval
    done

    echo -e "${RED}❌ $service_name failed to start within timeout${NC}"
    return 1
}

# Common function to load environment variables from .env file
load_env_file() {
    if [ -f ".env" ]; then
        source .env
        if [ -n "$TICKET_CONTRACT_ADDRESS" ]; then
            echo -e "${GREEN}✅ Contract address loaded: $TICKET_CONTRACT_ADDRESS${NC}"
            return 0
        fi
    fi
    return 1
}
