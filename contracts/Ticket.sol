// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title Ticket
 * @dev NFT contract for blockchain-based ticketing with lifecycle state management
 */
contract Ticket is ERC721, Ownable {
    // Ticket lifecycle states
    enum TicketStatus {
        Valid,
        CheckedIn,
        Invalidated
    }

    // Mapping from token ID to ticket status
    mapping(uint256 => TicketStatus) public ticketStatuses;

    // Mapping from token ID to token URI
    mapping(uint256 => string) private _tokenURIs;

    // Counter for token IDs
    uint256 private _nextTokenId;

    // Events
    event TicketMinted(uint256 indexed tokenId, address indexed to);
    event TicketCheckedIn(uint256 indexed tokenId);
    event TicketInvalidated(uint256 indexed tokenId);

    /**
     * @dev Constructor
     */
    constructor() ERC721("TicketChain", "TCKT") Ownable(msg.sender) {}

    /**
     * @dev Mint a new ticket NFT
     * @param to Address to mint the ticket to
     * @param tokenURI_ URI for the ticket metadata
     */
    function mintTicket(address to, string memory tokenURI_) external onlyOwner {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI_);
        ticketStatuses[tokenId] = TicketStatus.Valid;

        emit TicketMinted(tokenId, to);
    }

    /**
     * @dev Check in a ticket
     * @param tokenId ID of the ticket to check in
     */
    function checkIn(uint256 tokenId) external onlyOwner {
        require(_ownerOf(tokenId) != address(0), "Ticket does not exist");
        require(ticketStatuses[tokenId] == TicketStatus.Valid, "Ticket is not valid");

        ticketStatuses[tokenId] = TicketStatus.CheckedIn;
        emit TicketCheckedIn(tokenId);
    }

    /**
     * @dev Invalidate a ticket
     * @param tokenId ID of the ticket to invalidate
     */
    function invalidate(uint256 tokenId) external onlyOwner {
        require(_ownerOf(tokenId) != address(0), "Ticket does not exist");
        require(ticketStatuses[tokenId] == TicketStatus.Valid, "Ticket is not valid");

        ticketStatuses[tokenId] = TicketStatus.Invalidated;
        emit TicketInvalidated(tokenId);
    }

    /**
     * @dev Get the token URI
     * @param tokenId ID of the ticket
     */
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_ownerOf(tokenId) != address(0), "Ticket does not exist");
        return _tokenURIs[tokenId];
    }

    /**
     * @dev Set the token URI
     * @param tokenId ID of the ticket
     * @param tokenURI_ New URI for the ticket
     */
    function _setTokenURI(uint256 tokenId, string memory tokenURI_) internal {
        _tokenURIs[tokenId] = tokenURI_;
    }
}
