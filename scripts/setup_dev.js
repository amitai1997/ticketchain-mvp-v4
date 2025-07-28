/**
 * Development setup script
 * Deploys the Ticket contract and outputs configuration for the .env file
 */

const hre = require('hardhat');
const fs = require('fs');
const path = require('path');

async function main() {
  console.log('🚀 Starting development setup...\n');

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log('Deploying contracts with account:', deployer.address);
  console.log(
    'Account balance:',
    (await hre.ethers.provider.getBalance(deployer.address)).toString()
  );

  // Deploy the Ticket contract
  console.log('\n📝 Deploying Ticket contract...');
  const Ticket = await hre.ethers.getContractFactory('Ticket');
  const ticket = await Ticket.deploy();
  await ticket.waitForDeployment();

  const contractAddress = await ticket.getAddress();
  console.log('✅ Ticket contract deployed to:', contractAddress);

  // Write deployment info to a file
  const deploymentInfo = {
    TICKET_CONTRACT_ADDRESS: contractAddress,
    DEPLOYMENT_NETWORK: hre.network.name,
    DEPLOYMENT_CONTRACT_ADDRESS: contractAddress,
    DEPLOYMENT_DEPLOYER_ADDRESS: deployer.address,
  };

  // Update .env file with deployment information
  updateEnvFile(deploymentInfo);

  console.log('\n✨ Setup complete!');
  console.log(`📋 Contract deployed at: ${contractAddress}`);
  console.log('📁 Deployment info saved to .env file');
}

function updateEnvFile(updates) {
  const envPath = path.join(__dirname, '..', '.env');
  let envContent = '';

  // Read existing .env file if it exists
  if (fs.existsSync(envPath)) {
    envContent = fs.readFileSync(envPath, 'utf8');
  }

  // Update or add each key-value pair
  Object.entries(updates).forEach(([key, value]) => {
    const regex = new RegExp(`^${key}=.*$`, 'm');
    const newLine = `${key}=${value}`;

    if (regex.test(envContent)) {
      // Update existing key
      envContent = envContent.replace(regex, newLine);
    } else {
      // Add new key
      envContent += `\n${newLine}`;
    }
  });

  // Write back to .env file
  fs.writeFileSync(envPath, envContent.trim() + '\n');
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
