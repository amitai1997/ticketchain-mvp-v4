# Integration Testing Guide

This guide explains how to run and develop integration tests for TicketChain.

## Overview

Integration tests verify that the API correctly interacts with the blockchain, testing the complete flow from HTTP requests through Web3 transactions to on-chain state changes.

## Prerequisites

1. Node.js and npm installed
2. Python 3.12+ and Poetry installed
3. All dependencies installed:
   ```bash
   npm install
   poetry install
   ```

## Running Integration Tests

### Method 1: Using the Test Script (Recommended)

```bash
./scripts/run_integration_tests.sh
```

This script handles:
- ✅ Checking if Hardhat node is running
- ✅ Deploying contracts if needed
- ✅ Starting the API server
- ✅ Running all integration tests
- ✅ Cleanup after tests

### Method 2: Manual Setup

1. **Start Hardhat Node**:
   ```bash
   npx hardhat node
   ```

2. **Deploy Contracts**:
   ```bash
   npx hardhat run scripts/setup_dev.js --network localhost
   ```

3. **Set Contract Address**:
   Add the deployed address to your `.env`:
   ```
   TICKET_CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
   ```

4. **Start API Server**:
   ```bash
   poetry run uvicorn src.api.main:app --reload
   ```

5. **Run Tests**:
   ```bash
   poetry run pytest tests/integration -v
   ```

### Method 3: Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Wait for contract deployment
sleep 15

# Run tests
docker-compose exec api poetry run pytest tests/integration

# Stop services
docker-compose down
```

## Test Structure

### Test Files

- `test_api_health.py` - Basic health checks
- `test_ticket_lifecycle.py` - Complete ticket lifecycle tests

### Test Coverage

The integration tests cover:

1. **Ticket Minting**
   - API call to mint ticket
   - Verification of NFT creation on-chain
   - Correct owner assignment
   - Initial status verification

2. **Ticket Check-in**
   - State transition via API
   - On-chain status update verification
   - Prevention of double check-in

3. **Ticket Resale**
   - Ownership transfer via API
   - On-chain ownership verification
   - Event emission checks

4. **Ticket Invalidation**
   - Cancellation flow
   - Status update verification
   - Prevention of further operations

## Writing New Integration Tests

### Basic Template

```python
import pytest
import httpx
from web3 import Web3

@pytest.mark.asyncio
async def test_my_feature(api_client, w3, ticket_contract):
    # 1. Make API call
    response = await api_client.post("/api/v1/endpoint", json={...})
    assert response.status_code == 200

    # 2. Verify on-chain state
    on_chain_data = ticket_contract.functions.someMethod().call()
    assert on_chain_data == expected_value
```

### Available Fixtures

- `api_client` - Async HTTP client for API calls
- `w3` - Web3 instance connected to Hardhat
- `ticket_contract` - Deployed Ticket contract instance
- `contract_address` - Address of deployed contract

## Debugging Failed Tests

### Common Issues

1. **Connection Refused**
   - Ensure Hardhat node is running on port 8545
   - Check API is running on port 8000

2. **Contract Not Found**
   - Deploy contracts first
   - Verify TICKET_CONTRACT_ADDRESS in .env

3. **Transaction Failed**
   - Check account has ETH
   - Verify gas settings
   - Check contract state requirements

### Debug Commands

```bash
# Check Hardhat node
curl http://localhost:8545

# Check API health
curl http://localhost:8000/api/v1/health

# View Hardhat logs
# (In the terminal running hardhat node)

# Run single test with verbose output
poetry run pytest tests/integration/test_ticket_lifecycle.py::test_full_ticket_lifecycle -vvs
```

## CI/CD Integration

### GitHub Actions (Automated)

The GitHub Actions workflow runs integration tests automatically with enhanced reliability:

1. **Robust Poetry Installation**: Uses pip with fallback to official installer
2. **Service Health Checks**: Waits for Hardhat node and API server readiness
3. **Starts Hardhat node in Docker**: With proper health validation
4. **Deploys contracts**: Automatically configures environment
5. **Starts API server**: With readiness polling
6. **Runs all integration tests**: Complete test suite execution
7. **Reports results**: With detailed logging

### Local CI Testing

Test CI-like conditions before pushing:

```bash
# Run local CI simulation
npm run test:ci-local

# Or directly
./scripts/test_ci_locally.sh
```

This catches most issues locally including:
- Poetry/npm dependency problems
- Code quality issues (MyPy, Ruff, Black)
- Test failures
- Docker configuration issues

See `.github/workflows/ci.yml` for complete CI configuration details.

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Reset state between tests when needed
3. **Assertions**: Verify both API responses AND on-chain state
4. **Error Cases**: Test both success and failure scenarios
5. **Documentation**: Document what each test verifies

## Performance Tips

- Use session-scoped fixtures for expensive operations
- Batch similar tests together
- Consider parallel test execution for large test suites
- Cache contract ABIs and common data
