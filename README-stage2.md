# Stage 2: On-chain Core Implementation

## Overview

Stage 2 successfully implements the core on-chain functionality for the TicketChain system. The primary deliverable is a secure, minimal `Ticket.sol` smart contract that serves as the definitive on-chain registry for NFT tickets.

## Key Achievements

### 1. Smart Contract Implementation (`contracts/Ticket.sol`)
- **ERC-721 Standard**: Implements the ERC-721 NFT standard using OpenZeppelin's battle-tested contracts
- **Lifecycle Management**: Tracks ticket states through three phases:
  - `Valid`: Initial state after minting
  - `CheckedIn`: State after event attendance is validated
  - `Invalidated`: State for cancelled/invalidated tickets
- **Access Control**: Uses OpenZeppelin's `Ownable` pattern for secure administrative functions
- **Off-chain Metadata**: Stores only `tokenURI` on-chain, keeping gas costs minimal

### 2. Comprehensive Testing (`test/Ticket.test.js`)
- **19 Unit Tests**: Cover all critical functionality including:
  - Contract deployment and initialization
  - Ticket minting with sequential IDs
  - State transitions (check-in and invalidation)
  - Access control enforcement
  - Token URI management
- **100% Test Coverage**: Exceeds the 80% target with complete coverage of all functions

### 3. Deployment Infrastructure
- Updated `scripts/deploy.js` for Ticket contract deployment
- Successfully tested on local Hardhat network

## Deployed Contract Details

### Local Network Deployment
- **Contract Address**: `0x5FbDB2315678afecb367f032d93F642f64180aa3`
- **Deployer/Owner**: `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266`
- **Token Name**: TicketChain
- **Token Symbol**: TCKT

## Contract Interface

### Core Functions

#### Administrative Functions (Owner Only)
```solidity
// Mint a new ticket NFT
function mintTicket(address to, string memory tokenURI) external onlyOwner

// Check in a ticket (for event attendance)
function checkIn(uint256 tokenId) external onlyOwner

// Invalidate a ticket (for cancellations)
function invalidate(uint256 tokenId) external onlyOwner
```

#### Public View Functions
```solidity
// Get ticket status (0=Valid, 1=CheckedIn, 2=Invalidated)
function ticketStatuses(uint256 tokenId) public view returns (TicketStatus)

// Get token metadata URI
function tokenURI(uint256 tokenId) public view returns (string memory)

// Standard ERC-721 functions (ownerOf, balanceOf, etc.)
```

### Events
```solidity
event TicketMinted(uint256 indexed tokenId, address indexed to)
event TicketCheckedIn(uint256 indexed tokenId)
event TicketInvalidated(uint256 indexed tokenId)
```

## Usage Instructions

### 1. Start Local Development Network
```bash
npx hardhat node
```

### 2. Deploy the Contract
```bash
npx hardhat run scripts/deploy.js --network localhost
```

### 3. Run Tests
```bash
# Run all tests
npx hardhat test

# Run with coverage report
npx hardhat coverage
```

### 4. Interact with the Contract

Example interaction using Hardhat console:
```javascript
// Start console
npx hardhat console --network localhost

// Get contract instance
const Ticket = await ethers.getContractFactory("Ticket");
const ticket = await Ticket.attach("0x5FbDB2315678afecb367f032d93F642f64180aa3");

// Mint a ticket
const tx = await ticket.mintTicket("0x70997970C51812dc3A010C7d01b50e0d17dc79C8", "https://example.com/metadata/1");
await tx.wait();

// Check ticket status
const status = await ticket.ticketStatuses(0);
console.log("Ticket status:", status); // 0 = Valid

// Check in the ticket
await ticket.checkIn(0);
```

## State Transition Rules

The contract enforces the following state transition rules:
- Tickets can only be checked in or invalidated when in `Valid` state
- Once checked in or invalidated, tickets cannot transition to other states
- Only the contract owner (backend service) can perform state changes

## Security Considerations

1. **Access Control**: All administrative functions are protected with `onlyOwner` modifier
2. **State Validation**: Strict checks prevent invalid state transitions
3. **Existence Checks**: All functions verify token existence before operations
4. **Gas Optimization**: Minimal on-chain storage with off-chain metadata

## Next Steps

With the on-chain core complete, the project is ready for:
- Stage 3: API Gateway development for HTTP → blockchain integration
- Stage 4: Frontend interface for user interactions
- Optional: Deployment to public testnet (e.g., Polygon Amoy)

## Files Modified/Created

- `contracts/Ticket.sol` - Core smart contract implementation
- `test/Ticket.test.js` - Comprehensive unit tests
- `scripts/deploy.js` - Updated deployment script
- Removed: `contracts/Lock.sol` and `test/Lock.test.js` (placeholder files)

## CI Status

All continuous integration checks pass successfully:
- ✅ Unit tests: 19 tests passing
- ✅ Test coverage: 100% (exceeds 80% requirement)
- ✅ Code formatting: Prettier formatting applied
- ✅ Solidity linting: Only non-critical warnings (NatSpec documentation)
- ✅ Contract compilation: Successful with no errors