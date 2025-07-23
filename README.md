# TicketChain - Blockchain Ticketing System

A blockchain-based ticketing system implementing NFT tickets with on-chain smart contracts and off-chain API orchestration.

## 🏗️ Architecture

This project implements a dual-stack architecture:
- **On-chain**: Solidity smart contracts for NFT ticket management (ERC-721)
- **Off-chain**: Python/FastAPI backend for API orchestration and caching

## 📁 Project Structure

```
ticketchain-blockchain/
├── contracts/          # Solidity smart contracts
├── scripts/           # Hardhat deployment scripts
├── test/             # Hardhat/Chai unit tests
├── src/              # Python/FastAPI source code
│   ├── api/          # API endpoints
│   ├── blockchain_service/  # Web3.py interactions
│   └── datastore/    # Database models and cache
├── tests/            # Python tests
│   ├── unit/         # Unit tests
│   └── integration/  # Integration tests
├── docs/             # Documentation
└── infra/            # Infrastructure configuration
    └── docker/       # Docker configurations
```

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.0.0
- Python >= 3.12
- Poetry (Python dependency management)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ticketchain-blockchain
```

2. Install Hardhat dependencies:
```bash
npm install
```

3. Install Python dependencies:
```bash
poetry install
```

4. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Project

1. Start Hardhat local node:
```bash
npx hardhat node
```

2. Deploy contracts (in a new terminal):
```bash
npx hardhat run scripts/deploy.js --network localhost
```

3. Start the FastAPI backend:
```bash
poetry run uvicorn src.api.main:app --reload
```

4. Access the API:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🧪 Testing

### Smart Contract Tests
```bash
npx hardhat test
```

### Python Tests
```bash
poetry run pytest
```

### Coverage
```bash
# Solidity coverage
npx hardhat coverage

# Python coverage
poetry run pytest --cov=src
```

## 🛠️ Development

### Code Quality

The project uses:
- **Black** for Python formatting
- **Ruff** for Python linting
- **MyPy** for Python type checking
- **Solhint** for Solidity linting

Run all checks:
```bash
# Python
poetry run black src tests
poetry run ruff check src tests
poetry run mypy src

# Solidity
npx solhint contracts/**/*.sol
```

### Pre-commit Hooks

Install pre-commit hooks:
```bash
poetry run pre-commit install
```

## 📝 License

MIT License
