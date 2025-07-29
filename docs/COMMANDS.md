# Development Commands Reference

> **Single Source of Truth**: Common development commands used across the project.

## 📋 Available npm Scripts

Run `npm run` to see all available scripts. Here are the most commonly used:

```bash
# Testing
npm test                    # Run smart contract tests
npm run test:ci-local       # Test CI-like conditions locally
npm run test:integration    # Run integration tests with setup
npm run test:containerized  # Test complete containerized setup

# Deployment
npm run deploy:local        # Deploy to local Hardhat network
npm run deploy              # Deploy to configured network

# Code Quality
npm run format              # Format all code files
npm run format:check        # Check code formatting
npm run lint:sol            # Lint Solidity contracts
npm run lint:sol:fix        # Fix Solidity linting issues
```

## 🚀 Quick Start Commands

```bash
# Initial setup
npm install && poetry install
cp .env.example .env

# Start development stack
npx hardhat node              # Terminal 1: Blockchain
npm run deploy:local          # Terminal 2: Deploy contracts
poetry run uvicorn src.api.main:app --reload  # Terminal 3: API server
```

## 🔧 Blockchain Commands

### Smart Contract Development
```bash
# Contract compilation and testing
npx hardhat compile                 # Compile contracts
npm test                           # Run Solidity tests (alias: npx hardhat test)
npx hardhat coverage              # Generate coverage report
npx hardhat console --network localhost  # Interactive console

# Contract deployment
npm run deploy:local               # Deploy to localhost (recommended)
npm run deploy                     # Deploy to default network
npx hardhat run scripts/deploy.js --network <network>  # Deploy to specific network
npx hardhat verify --network <network> <address>      # Verify on block explorer
```

### Development Blockchain
```bash
npx hardhat node                   # Start local blockchain
npx hardhat node --hostname 0.0.0.0  # Start with external access
```

## 🐍 Backend Commands

### Development Server
```bash
poetry run uvicorn src.api.main:app --reload    # Start API server
poetry run uvicorn src.api.main:app --reload --port 8001  # Custom port
```

### Testing & Quality
```bash
# Python testing
poetry run pytest                  # Run Python tests
poetry run pytest --cov=src       # With coverage
poetry run pytest -v              # Verbose output
npm run test:integration           # Run integration tests (recommended)

# Code quality
poetry run black src tests         # Format code
poetry run ruff check src tests    # Lint code
poetry run mypy src                # Type checking
```

## 🐳 Docker Commands

```bash
# Container Management (Docker Compose V2)
docker compose up -d               # Start all services
docker compose down                # Stop all services
docker compose build               # Build containers
docker compose logs api            # View API logs
docker compose logs hardhat        # View blockchain logs
docker compose up deployer         # Deploy contracts to containerized network

# Testing containerized setup
npm run test:containerized         # Test complete containerized stack (recommended)
./scripts/test_containerized_setup.sh  # Direct script execution

# Legacy Docker Compose V1 (if V2 not available)
# Replace 'docker compose' with 'docker-compose' in above commands
```

## 🔍 Quality Assurance

```bash
# Automated testing and checks
npm run test:ci-local              # Test CI-like conditions locally (recommended)
./scripts/test_ci_locally.sh       # Direct script execution

# Pre-commit setup
poetry run pre-commit install      # Install hooks
poetry run pre-commit run --all-files  # Run all checks

# Code formatting and linting
npm run format                     # Format all files (recommended)
npm run format:check               # Check formatting
npm run lint:sol                   # Lint Solidity (recommended)
npm run lint:sol:fix               # Fix Solidity issues (recommended)

# Manual quality checks
npm test && poetry run pytest      # Run all tests
npx hardhat test --gas-reporter    # Gas usage analysis
```

## 📦 Environment Management

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
npm run                            # List all available npm scripts
```

## 🛠️ Advanced Usage

### Script Analysis
```bash
# Script-specific commands (when npm scripts aren't sufficient)
npx hardhat run scripts/deploy.js --network mainnet  # Deploy to mainnet
./scripts/run_integration_tests.sh                   # Direct integration test execution
./scripts/test_ci_locally.sh                         # Direct CI test execution

# Note: scripts/_common.sh is a utility and should not be run directly
```

### Development Workflow
```bash
# Typical development cycle
npm run test:ci-local              # 1. Test everything locally
npm run deploy:local               # 2. Deploy contracts
npm run test:integration           # 3. Run integration tests
npm run format && npm run lint:sol # 4. Format and lint code
```

---

## 🎯 Recommended Usage Patterns

| Task | Recommended Command | Alternative |
|------|-------------------|-------------|
| **Deploy locally** | `npm run deploy:local` | `npx hardhat run scripts/deploy.js --network localhost` |
| **Test contracts** | `npm test` | `npx hardhat test` |
| **Integration tests** | `npm run test:integration` | `./scripts/run_integration_tests.sh` |
| **Local CI testing** | `npm run test:ci-local` | `./scripts/test_ci_locally.sh` |
| **Containerized testing** | `npm run test:containerized` | `./scripts/test_containerized_setup.sh` |
| **Format code** | `npm run format` | `npx prettier --write "**/*.{js,json,sol,yml,yaml}"` |
| **Lint Solidity** | `npm run lint:sol` | `npx solhint "contracts/**/*.sol"` |

---

*Referenced by: README.md and stage-specific documentation*
