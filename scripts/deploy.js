const hre = require('hardhat');
const fs = require('fs');
const path = require('path');

// Detect if this is being run in development mode
const isDevelopmentMode =
  process.argv.includes('--dev') ||
  hre.network.name === 'localhost' ||
  hre.network.name === 'hardhat' ||
  hre.network.name === 'hardhat_docker';

async function main() {
  if (isDevelopmentMode) {
    console.log('🚀 Starting development setup...\n');
  } else {
    console.log('Deploying Ticket contract...');
  }

  // Get the deployer's signer
  const [deployer] = await hre.ethers.getSigners();

  if (isDevelopmentMode) {
    console.log('Deploying contracts with account:', deployer.address);
    console.log(
      'Account balance:',
      (await hre.ethers.provider.getBalance(deployer.address)).toString()
    );
    console.log('\n📝 Deploying Ticket contract...');
  } else {
    console.log('Deploying contract with account:', deployer.address);
  }

  // Deploy the Ticket contract
  const Ticket = await hre.ethers.getContractFactory('Ticket');
  const ticket = await Ticket.deploy();

  await ticket.waitForDeployment();

  const contractAddress = await ticket.getAddress();

  if (isDevelopmentMode) {
    console.log('✅ Ticket contract deployed to:', contractAddress);
  } else {
    console.log('Ticket contract deployed to:', contractAddress);
    console.log('Contract owner:', await ticket.owner());
    console.log('Token name:', await ticket.name());
    console.log('Token symbol:', await ticket.symbol());
  }

  // Update .env file with deployment information
  const deploymentInfo = {
    TICKET_CONTRACT_ADDRESS: contractAddress,
    DEPLOYMENT_NETWORK: hre.network.name,
    DEPLOYMENT_CONTRACT_ADDRESS: contractAddress,
    DEPLOYMENT_DEPLOYER_ADDRESS: deployer.address,
  };

  updateEnvFile(deploymentInfo);

  if (isDevelopmentMode) {
    console.log('\n✨ Setup complete!');
    console.log(`📋 Contract deployed at: ${contractAddress}`);
    console.log('📁 Deployment info saved to .env file');
  } else {
    console.log('\n✅ Deployment information saved to .env file');
  }
}

function updateEnvFile(updates) {
  // In containerized deployment, write to data directory which is mounted
  const envPath =
    process.env.NODE_ENV === 'docker' || fs.existsSync('/app/data')
      ? path.join('/app/data', '.env')
      : path.join(__dirname, '..', '.env');
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

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
