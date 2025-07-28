# Development Commands Reference

> **Single Source of Truth**: Common development commands used across the project.

## Quick Start Commands

```bash
# Initial setup
npm install && poetry install
cp .env.example .env

# Start development stack
npx hardhat node                    # Terminal 1: Blockchain
npx hardhat run scripts/deploy.js   # Terminal 2: Deploy contracts
poetry run uvicorn src.api.main:app --reload  # Terminal 3: API server
```

## Blockchain Commands

```bash
# Contract Development
npx hardhat compile                 # Compile contracts
npx hardhat test                   # Run Solidity tests
npx hardhat coverage              # Generate coverage report
npx hardhat console --network localhost  # Interactive console

# Deployment
npx hardhat run scripts/deploy.js --network localhost
npx hardhat verify --network <network> <address>

# Development Node
npx hardhat node                   # Start local blockchain
```

## Backend Commands

```bash
# Development Server
poetry run uvicorn src.api.main:app --reload    # Start API server
poetry run uvicorn src.api.main:app --reload --port 8001  # Custom port

# Testing
poetry run pytest                  # Run Python tests
poetry run pytest --cov=src       # With coverage
poetry run pytest -v              # Verbose output

# Code Quality
poetry run black src tests         # Format code
poetry run ruff check src tests    # Lint code
poetry run mypy src                # Type checking
```

## Docker Commands

```bash
# Container Management
docker-compose up -d               # Start all services
docker-compose down                # Stop all services
docker-compose build               # Build containers
docker-compose logs api            # View API logs
docker-compose logs hardhat        # View blockchain logs
```

## Quality Assurance

```bash
# Pre-commit Setup
poetry run pre-commit install      # Install hooks
poetry run pre-commit run --all-files  # Run all checks

# CI Testing (Local)
npm run test:ci-local              # Test CI-like conditions locally
./scripts/test_ci_locally.sh       # Direct script execution

# Manual Quality Checks
npm test && poetry run pytest      # Run all tests
npx solhint contracts/**/*.sol     # Lint Solidity
npx hardhat test --gas-reporter    # Gas usage analysis
```

## Environment Management

```bash
# Dependencies
npm install                        # Install Node.js deps
poetry install                     # Install Python deps
poetry add <package>               # Add Python package
npm install <package>              # Add Node.js package

# Environment Info
node --version && python --version  # Check versions
poetry env info                    # Poetry environment details
npx hardhat --version              # Hardhat version
```

---

*Referenced by: README.md and stage-specific documentation*
