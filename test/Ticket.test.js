const { expect } = require('chai');
const { ethers } = require('hardhat');
const { loadFixture } = require('@nomicfoundation/hardhat-toolbox/network-helpers');

describe('Ticket', function () {
  // Deploy the contract before each test
  async function deployTicketFixture() {
    const [owner, addr1, addr2] = await ethers.getSigners();

    const Ticket = await ethers.getContractFactory('Ticket');
    const ticket = await Ticket.deploy();
    await ticket.waitForDeployment();

    return { ticket, owner, addr1, addr2 };
  }

  describe('Deployment', function () {
    it('Should set the right owner', async function () {
      const { ticket, owner } = await loadFixture(deployTicketFixture);
      expect(await ticket.owner()).to.equal(owner.address);
    });

    it('Should have the correct name and symbol', async function () {
      const { ticket } = await loadFixture(deployTicketFixture);
      expect(await ticket.name()).to.equal('TicketChain');
      expect(await ticket.symbol()).to.equal('TCKT');
    });
  });

  describe('Minting', function () {
    it('Should allow owner to mint tickets', async function () {
      const { ticket, owner, addr1 } = await loadFixture(deployTicketFixture);
      const tokenURI = 'https://example.com/metadata/1';

      await expect(ticket.mintTicket(addr1.address, tokenURI))
        .to.emit(ticket, 'TicketMinted')
        .withArgs(0, addr1.address);

      expect(await ticket.ownerOf(0)).to.equal(addr1.address);
      expect(await ticket.tokenURI(0)).to.equal(tokenURI);
      expect(await ticket.ticketStatuses(0)).to.equal(0); // TicketStatus.Valid
    });

    it('Should mint tickets with sequential token IDs', async function () {
      const { ticket, addr1, addr2 } = await loadFixture(deployTicketFixture);

      await ticket.mintTicket(addr1.address, 'uri1');
      await ticket.mintTicket(addr2.address, 'uri2');

      expect(await ticket.ownerOf(0)).to.equal(addr1.address);
      expect(await ticket.ownerOf(1)).to.equal(addr2.address);
    });

    it('Should not allow non-owner to mint tickets', async function () {
      const { ticket, addr1 } = await loadFixture(deployTicketFixture);

      await expect(
        ticket.connect(addr1).mintTicket(addr1.address, 'uri')
      ).to.be.revertedWithCustomError(ticket, 'OwnableUnauthorizedAccount');
    });
  });

  describe('State Changes', function () {
    async function mintTicketFixture() {
      const { ticket, owner, addr1, addr2 } = await loadFixture(deployTicketFixture);
      await ticket.mintTicket(addr1.address, 'https://example.com/1');
      return { ticket, owner, addr1, addr2 };
    }

    describe('Check In', function () {
      it('Should allow owner to check in a valid ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await expect(ticket.checkIn(0)).to.emit(ticket, 'TicketCheckedIn').withArgs(0);

        expect(await ticket.ticketStatuses(0)).to.equal(1); // TicketStatus.CheckedIn
      });

      it('Should not allow check in of non-existent ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await expect(ticket.checkIn(999)).to.be.revertedWith('Ticket does not exist');
      });

      it('Should not allow check in of already checked-in ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await ticket.checkIn(0);
        await expect(ticket.checkIn(0)).to.be.revertedWith('Ticket is not valid');
      });

      it('Should not allow check in of invalidated ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await ticket.invalidate(0);
        await expect(ticket.checkIn(0)).to.be.revertedWith('Ticket is not valid');
      });

      it('Should not allow non-owner to check in tickets', async function () {
        const { ticket, addr1 } = await loadFixture(mintTicketFixture);

        await expect(ticket.connect(addr1).checkIn(0)).to.be.revertedWithCustomError(
          ticket,
          'OwnableUnauthorizedAccount'
        );
      });
    });

    describe('Invalidate', function () {
      it('Should allow owner to invalidate a valid ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await expect(ticket.invalidate(0)).to.emit(ticket, 'TicketInvalidated').withArgs(0);

        expect(await ticket.ticketStatuses(0)).to.equal(2); // TicketStatus.Invalidated
      });

      it('Should not allow invalidation of non-existent ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await expect(ticket.invalidate(999)).to.be.revertedWith('Ticket does not exist');
      });

      it('Should not allow invalidation of already checked-in ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await ticket.checkIn(0);
        await expect(ticket.invalidate(0)).to.be.revertedWith('Ticket is not valid');
      });

      it('Should not allow invalidation of already invalidated ticket', async function () {
        const { ticket } = await loadFixture(mintTicketFixture);

        await ticket.invalidate(0);
        await expect(ticket.invalidate(0)).to.be.revertedWith('Ticket is not valid');
      });

      it('Should not allow non-owner to invalidate tickets', async function () {
        const { ticket, addr1 } = await loadFixture(mintTicketFixture);

        await expect(ticket.connect(addr1).invalidate(0)).to.be.revertedWithCustomError(
          ticket,
          'OwnableUnauthorizedAccount'
        );
      });
    });
  });

  describe('Token URI', function () {
    it('Should return correct token URI', async function () {
      const { ticket, addr1 } = await loadFixture(deployTicketFixture);
      const uri = 'https://example.com/metadata/1';

      await ticket.mintTicket(addr1.address, uri);
      expect(await ticket.tokenURI(0)).to.equal(uri);
    });

    it('Should revert when querying URI for non-existent token', async function () {
      const { ticket } = await loadFixture(deployTicketFixture);

      await expect(ticket.tokenURI(999)).to.be.revertedWith('Ticket does not exist');
    });
  });

  describe('Access Control', function () {
    it('Should allow owner to transfer ownership', async function () {
      const { ticket, owner, addr1 } = await loadFixture(deployTicketFixture);

      await ticket.transferOwnership(addr1.address);
      expect(await ticket.owner()).to.equal(addr1.address);
    });

    it('Should not allow non-owner to transfer ownership', async function () {
      const { ticket, addr1, addr2 } = await loadFixture(deployTicketFixture);

      await expect(
        ticket.connect(addr1).transferOwnership(addr2.address)
      ).to.be.revertedWithCustomError(ticket, 'OwnableUnauthorizedAccount');
    });
  });
});
