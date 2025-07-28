# TicketChain - Blockchain Ticketing System

A minimal viable blockchain-based ticketing system that issues event tickets as NFTs, manages their lifecycle, and provides API endpoints compatible with OPEN Ticketing Ecosystem patterns.

## 🎯 Project Vision

TicketChain combines on-chain smart contracts with off-chain orchestration to create a transparent, secure, and composable ticketing system. Event tickets are issued as ERC-721 NFTs, enabling secondary markets, preventing fraud, and offering attendees true ownership of their tickets.

## 🏗️ Architecture

This project implements a dual-stack architecture:

- **On-chain**: Solidity smart contracts for immutable ticket lifecycle management
- **Off-chain**: Python/FastAPI backend for API orchestration, caching, and business logic
- **Standards**: Compatible with OPEN Ticketing Ecosystem APIs and ERC-721 NFT standard

## 📊 Current Status

**✅ Stage 1 Complete**: Foundation & Scaffolding
**✅ Stage 2 Complete**: On-Chain Core (Smart Contracts)
**✅ Stage 3 Complete**: Off-Chain Core & Blockchain Integration - **FULLY FUNCTIONAL**
**🚧 Stage 4 Ready**: Infrastructure & Quality Enhancements

See [Project Status](docs/PROJECT_STATUS.md) for detailed progress tracking.

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.0.0
- Python >= 3.12
- Poetry installed
- Docker & Docker Compose (optional)

### Installation & Setup

```bash
# Clone and setup
git clone <repository-url>
cd ticketchain-mvp-v4
npm install && poetry install
cp .env.example .env
```

### Running the System

#### Local Development (Recommended)
```bash
# Terminal 1: Start Hardhat blockchain
npx hardhat node

# Terminal 2: Deploy contracts
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3: Start API server
poetry run uvicorn src.api.main:app --reload
```

#### Docker Compose (Alternative)
```bash
docker compose up -d                    # Start all services
docker compose logs api                 # View API logs
docker compose logs hardhat             # View blockchain logs
docker compose down                     # Stop all services
```

> **Note**: Use `docker-compose` (legacy) if `docker compose` (V2) is not available.

### Verification

After starting the system, verify everything is working:

```bash
# Check API health
curl http://localhost:8000/api/v1/health

# Check Hardhat node is running
curl -X POST -H "Content-Type: application/json" \
     --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
     http://localhost:8545
```

**Web Interfaces:**
- **API Health**: http://localhost:8000/api/v1/health
- **API Docs**: http://localhost:8000/docs
- **Hardhat Console**: `npx hardhat console --network localhost`

## 🧪 Testing

### Smart Contract Tests
```bash
npx hardhat test                        # Run all Solidity tests
npx hardhat coverage                    # Generate coverage report
npx hardhat test --gas-reporter         # Analyze gas usage
```

### Backend Tests
```bash
poetry run pytest                       # Run all Python tests
poetry run pytest --cov=src            # With coverage report
poetry run pytest -v                   # Verbose output
```

### CI Testing (Local)
```bash
npm run test:ci-local                   # Test CI-like conditions locally
./scripts/test_ci_locally.sh            # Direct script execution
```
Catches most CI issues before pushing: Poetry/npm problems, code quality issues, test failures, Docker configuration.

### Run All Tests
```bash
npm test && poetry run pytest          # Quick test everything
```

## 📁 Project Structure

```
ticketchain-mvp-v4/
├── contracts/              # Solidity smart contracts
│   └── Ticket.sol         # Core ERC-721 ticket contract
├── scripts/               # Deployment scripts
├── test/                  # Solidity tests
├── src/                   # Python/FastAPI backend
│   ├── api/              # API endpoints
│   ├── blockchain_service/ # Web3.py integration (Stage 3)
│   └── datastore/        # Database models (Stage 3)
├── tests/                 # Python tests
├── docs/                  # Documentation
│   ├── stages/           # Stage-specific documentation
│   └── PROJECT_STATUS.md # Current project status
├── infra/                 # Infrastructure
│   └── docker/           # Docker configurations
└── .github/              # CI/CD workflows
```

## 🔧 Technology Stack

For detailed technology versions and descriptions, see **[Technology Stack Reference](docs/TECH_STACK.md)**.

**Quick Overview:**
- **Blockchain**: Hardhat + Solidity 0.8.24 + OpenZeppelin contracts
- **Backend**: Python 3.12 + FastAPI + Web3.py
- **Infrastructure**: Docker + Poetry + GitHub Actions

## 📖 Documentation

### Project Overview
- **[Project Status](docs/PROJECT_STATUS.md)** - Current progress and next steps
- **[Technology Stack](docs/TECH_STACK.md)** - Complete tech stack reference
- **[Development Commands](docs/COMMANDS.md)** - All development commands

### Implementation Stages
- **[Stage 1: Foundation](docs/stages/stage-1/README.md)** - Project scaffolding and setup
- **[Stage 2: Smart Contracts](docs/stages/stage-2/README.md)** - On-chain implementation

### Reference Materials
- **[OPEN Ticketing API Reference](docs/apis_combined.md)** - External API compatibility
- **[High-Level Implementation Plan](docs/high-level-implementation-plan.md)** - Overall strategy

## 🎫 Core Features

### Implemented ✅
- **ERC-721 NFT Tickets**: Each ticket is a unique, transferable NFT
- **Lifecycle Management**: Full ticket lifecycle (Mint → Resell → Check-in → Invalidate)
- **API Gateway**: Complete HTTP endpoints for blockchain interaction
- **Web3 Integration**: Full blockchain service with transaction management
- **Access Control**: Secure administrative functions
- **Ticket Registry**: Off-chain mapping and state management
- **Comprehensive Testing**: 27 tests across all layers with 100% coverage
- **CI/CD Pipeline**: Automated testing and quality checks
- **Live System**: Fully functional API server with blockchain integration

### In Development 🚧
- **Event Management**: Enhanced event lifecycle management
- **User Authentication**: JWT-based user management system
- **Advanced Analytics**: Ticket sales and usage analytics

### Planned 📋
- **Secondary Markets**: Ticket resale functionality
- **Batch Operations**: Efficient bulk ticket operations
- **Mobile Integration**: QR code scanning and mobile wallets

## 🛠️ Development

### Development & Deployment Commands

#### Smart Contract Development
```bash
npx hardhat compile                     # Compile contracts
npx hardhat test                       # Run tests
npx hardhat node                       # Start local blockchain
npx hardhat run scripts/deploy.js      # Deploy contracts
npx hardhat console --network localhost # Interactive console
```

#### Backend Development
```bash
poetry run uvicorn src.api.main:app --reload    # Start dev server
poetry run pytest                               # Run tests
poetry run black src tests                      # Format code
poetry run ruff check src tests                 # Lint code
poetry run mypy src                              # Type checking
```

#### Code Quality & CI Testing
```bash
poetry run pre-commit install          # Setup pre-commit hooks
poetry run pre-commit run --all-files  # Run all quality checks
npm run test:ci-local                   # Test CI-like conditions locally
```

> **💡 Tip:** See [Development Commands Reference](docs/COMMANDS.md) for comprehensive command documentation and advanced usage.

### Adding Features

1. **Smart Contract Changes**: Update `contracts/Ticket.sol` and add tests
2. **API Changes**: Add endpoints in `src/api/` with corresponding tests
3. **Documentation**: Update relevant documentation in `docs/`

## 🌐 Deployment

### Local Networks
- **Hardhat Network**: Built-in local blockchain (default)
- **Hardhat Node**: Persistent local blockchain for development

### Testnets (Planned)
- **Polygon Amoy**: Primary testnet for integration testing
- **Ethereum Sepolia**: Alternative testnet option

### Production (Future)
- **Polygon Mainnet**: Low-cost, fast transactions
- **Ethereum Mainnet**: Maximum security and adoption

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Run quality checks: `npm test && poetry run pytest`
5. Commit with conventional commits: `git commit -m "feat: add amazing feature"`
6. Push and create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Hardhat Documentation](https://hardhat.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OPEN Ticketing Ecosystem](https://docs.onopen.xyz/)

---

*Built with ❤️ for transparent, secure, and composable ticketing*
