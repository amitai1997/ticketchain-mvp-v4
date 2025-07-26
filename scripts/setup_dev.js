/**
 * Development setup script
 * Deploys the Ticket contract and outputs configuration for the .env file
 */

const hre = require("hardhat");
const fs = require("fs");

async function main() {
  console.log("🚀 Starting development setup...\n");

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  // Deploy the Ticket contract
  console.log("\n📝 Deploying Ticket contract...");
  const Ticket = await hre.ethers.getContractFactory("Ticket");
  const ticket = await Ticket.deploy();
  await ticket.deployed();

  console.log("✅ Ticket contract deployed to:", ticket.address);

  // Write deployment info to a file
  const deploymentInfo = {
    network: hre.network.name,
    contractAddress: ticket.address,
    deployerAddress: deployer.address,
    timestamp: new Date().toISOString(),
  };

  fs.writeFileSync(
    "data/deployment.json",
    JSON.stringify(deploymentInfo, null, 2)
  );

  // Output .env configuration
  console.log("\n📋 Add the following to your .env file:");
  console.log("=====================================");
  console.log(`TICKET_CONTRACT_ADDRESS=${ticket.address}`);
  console.log("=====================================");

  console.log("\n✨ Setup complete!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });