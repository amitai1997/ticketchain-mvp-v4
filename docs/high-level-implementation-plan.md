You are absolutely right. My previous plan missed the most critical component of a blockchain ticketing system: the on-chain smart contract. A "clone" without this piece would just be a standard web2 API. Thank you for the correction.

Here is the revised, more complete implementation plan, which incorporates the on-chain logic as a new, distinct stage.

---

## **Stage 1: Scaffolding (Revised)**
This stage sets up a dual-stack project for both the Solidity smart contract and the Python backend.

* **AI Agent Tasks:**
    * Initialize a new Git repository.
    * Set up a **Hardhat** project for the Solidity environment (`npx hardhat`).
    * Set up a Python virtual environment and `pyproject.toml` for the FastAPI backend.
    * Integrate the two project structures into a cohesive monorepo layout.

* **Key Files/Directories:**
    * `/contracts/`: For Solidity source code (`.sol`).
    * `/scripts/`: For Hardhat deployment scripts (`.js`).
    * `/test/`: For Hardhat/Chai unit tests (`.js`).
    * `/app/`: For Python/FastAPI source code.
    * `/tests/`: For Pytest backend tests.
    * `hardhat.config.js`: Hardhat project configuration.
    * `pyproject.toml`: Python dependency management.

* **External Libraries:**
    * **Hardhat**: The core of the Solidity development and testing environment.
    * **OpenZeppelin Contracts**: For secure, standard implementations of ERC-721.
    * **FastAPI, Uvicorn**: For the backend API.

* **Acceptance Criteria:**
    * A default Hardhat project is functional.
    * A "hello world" FastAPI endpoint runs successfully.
    * The combined directory structure is clean and logical.

---

## **Stage 2: On-Chain Core (New)**
This stage focuses exclusively on developing, testing, and deploying the core NFT ticket smart contract.

* **AI Agent Tasks:**
    * Create a `Ticket.sol` smart contract inheriting from OpenZeppelin's `ERC721.sol`. [cite_start]The document notes the system adheres to the ERC-721 standard[cite: 30].
    * Implement a minimal set of functions:
        * `mintTicket(address owner, string memory tokenURI)`: Only callable by the contract owner (our backend).
        * `checkIn(uint256 tokenId)`: A simple state-changing function.
        * `invalidate(uint256 tokenId)`: A simple state-changing function.
    * Write unit tests in JavaScript (using Hardhat/Chai) to verify minting, ownership, and state changes.
    * Create a Hardhat script to deploy the contract to a local network.

* **Key Files/Directories:**
    * `contracts/Ticket.sol`: The new smart contract.
    * `test/Ticket.test.js`: Solidity unit tests.
    * `scripts/deploy.js`: The deployment script.

* **External Libraries:**
    * `@openzeppelin/contracts`: For the ERC-721 implementation.
    * `hardhat`, `@nomicfoundation/hardhat-toolbox`: For testing and running a local node.

* **Acceptance Criteria:**
    * The `Ticket.sol` contract compiles without errors.
    * All Solidity unit tests pass.
    * The contract can be successfully deployed to a local Hardhat node.

---

## **Stage 3: Off-Chain Core & Blockchain Interaction**
This stage builds the backend API, now acting as a trusted orchestrator that interacts with the smart contract.

* **AI Agent Tasks:**
    * Implement a `BlockchainService` in Python to handle all `web3.py` interactions (connecting to the node, loading the contract ABI, sending transactions).
    * Implement the FastAPI endpoints. These endpoints will now call the `BlockchainService` instead of a local database:
        * `soldTicket` calls the contract's `mintTicket` function.
        * `resoldTicket` performs a standard `transferFrom` call.
        * `checkedInTicket` calls the contract's `checkIn` function.
    * Use an SQLite database as a **cache and off-chain data store**, not as the primary source of truth for tickets. [cite_start]It will store mappings from internal IDs to on-chain `tokenId`s and user data that shouldn't be on-chain[cite: 36, 1361].

* **Key Files/Directories:**
    * `app/blockchain_service.py`: New file to encapsulate `web3.py` logic.
    * `app/main.py`: (Modify) API endpoints now call `BlockchainService`.
    * `app/datastore.py`: (Modify) Role changed to cache/off-chain storage.
    * `.env`: To securely store the backend wallet's private key and RPC endpoint URL.

* **External Libraries:**
    * **web3.py**: The essential library for interacting with the Ethereum blockchain from Python.

* **Acceptance Criteria:**
    * API endpoints successfully trigger transactions on the local Hardhat node.
    * The `soldTicket` API call results in a new NFT being minted on the local chain.
    * The SQLite database correctly caches necessary information.

---

## **Stage 4: Infrastructure & Quality (Revised)**
This stage now focuses on integrated testing of the full stack, from the API to the smart contract.

* **AI Agent Tasks:**
    * Update `docker-compose.yml` to run three services: the FastAPI backend, a Hardhat node, and the database.
    * Write integration tests that make API calls to the backend and then verify the resulting state changes directly on the local blockchain.
    * Update the GitHub Actions CI pipeline to run the full integration test suite.

* **Key Files/Directories:**
    * `docker-compose.yml`: (Modify) Add a Hardhat service.
    * `tests/test_integration.py`: New integration tests for the full on-chain/off-chain flow.
    * `.github/workflows/ci.yml`: (Modify) Update the test job to use the Docker Compose setup.

* **External Libraries:**
    * **Pytest**: For testing.
    * **HTTPX**: For API calls within tests.

* **Acceptance Criteria:**
    * `docker-compose up` successfully launches the entire local development stack.
    * Integration tests pass, confirming the API correctly manipulates the smart contract's state.
    * The CI pipeline passes.

---

## **Stage 5: Docs & Polish**
This stage remains focused on documentation, but now needs to cover the on-chain components.

* **AI Agent Tasks:**
    * Update `README.md` to explain the full architecture, including the on-chain components and how to run the complete stack with Hardhat and Docker Compose.
    * [cite_start]Update the ADR to clarify why a minimal custom contract was chosen over the feature-rich contracts from the OPEN documentation[cite: 127].

* **Acceptance Criteria:**
    * Documentation is comprehensive and reflects the final two-stack architecture.

---

## **Stage 6: Buffer / Stretch Goals**
The stretch goals remain the same, focusing on enhancing the API's security and robustness.

* **AI Agent Tasks:**
    * Add a JWT authentication stub to the FastAPI backend.

* **Acceptance Criteria:**
    * Protected endpoints require a valid (stubbed) JWT for access.