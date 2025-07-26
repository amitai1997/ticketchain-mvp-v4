const hre = require('hardhat');

async function main() {
  console.log('Deploying Ticket contract...');

  // Get the deployer's signer
  const [deployer] = await hre.ethers.getSigners();
  console.log('Deploying contract with account:', deployer.address);

  // Deploy the Ticket contract
  const Ticket = await hre.ethers.getContractFactory('Ticket');
  const ticket = await Ticket.deploy();

  await ticket.waitForDeployment();

  console.log('Ticket contract deployed to:', await ticket.getAddress());
  console.log('Contract owner:', await ticket.owner());
  console.log('Token name:', await ticket.name());
  console.log('Token symbol:', await ticket.symbol());
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
