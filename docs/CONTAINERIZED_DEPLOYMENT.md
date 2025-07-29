# Containerized Deployment Reference

> **Single Source of Truth**: All containerized deployment information is centralized here.

## 🐳 **Quick Start**

```bash
# 1. Start services
docker compose up -d

# 2. Deploy contracts
docker compose up deployer

# 3. Validate everything works
npm run test:containerized
```

## 📋 **Available Commands**

| Command | Purpose | Environment |
|---------|---------|-------------|
| `docker compose up -d` | Start API and Hardhat services | Container |
| `docker compose up deployer` | Deploy contracts to containerized network | Container |
| `docker compose logs <service>` | View service logs | Container |
| `docker compose down` | Stop all services | Container |
| `npm run test:containerized` | Complete E2E validation | Local → Container |

## 🔍 **Health Checks**

```bash
# API Health
curl -s http://localhost:8000/api/v1/health | jq .

# Blockchain RPC
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"net_version","params":[],"id":1}' \
  http://localhost:8545
```

## 🧪 **Testing Workflows**

### Complete E2E Testing
```bash
docker compose up -d && docker compose up deployer && npm run test:containerized
```

### Development Workflow
```bash
# Start containers
docker compose up -d

# Deploy contracts
docker compose up deployer

# Run tests
npm run test:containerized

# View logs
docker compose logs api
docker compose logs hardhat

# Stop when done
docker compose down
```

## 🔧 **Configuration**

- **Contract Address**: Auto-configured via deployer service → `data/.env`
- **RPC URL**: `http://hardhat:8545` (internal), `http://localhost:8545` (external)
- **API URL**: `http://localhost:8000`

## 📊 **Service Status**

```bash
# Check all services
docker compose ps

# Expected output:
# api     - Up (port 8000)
# hardhat - Up (port 8545)
```

---

*This is the authoritative reference for containerized deployment. Other docs reference this file.*
