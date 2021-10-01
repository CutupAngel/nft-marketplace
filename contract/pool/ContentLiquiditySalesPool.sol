// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.8.0;

import "../netflix-libs/gsn/Context.sol";
import "../netflix-libs/token/erc20/ERC20.sol";
import "../netflix-libs/token/erc721/ERC721.sol";
import "../netflix-libs/math/SafeMath.sol";
import "../netflix-libs/access/Ownable.sol";

contract ContentLiquiditySalesPool is Ownable {

    event Sent(address indexed payee, uint256 amount, uint256 balance);
    event Received(address indexed payer, uint256 tokenId, uint256 amount, uint256 balance);

    // ERC721 nftTokenAddress
    ERC721 public nftTokenAddress;
    // ERC20 erc20TokenAddress
    ERC20 public erc20TokenAddress;
    // tokenId price
    uint256 public tokenIdPrice;
    // mapping tokenId based on address
    mapping(uint256 => address) public tokenSeller;

    /**
    * @dev Contract Constructor
    * @param _nftTokenAddress address for non-fungible token contract
    * @param _currentPrice initial price
    */
    constructor(address _nftTokenAddress, address _erc20TokenAddress, uint256 _tokenIdPrice , uint256 _tokenId) public {
        // check _nftTokenAddress address validation
        require(_nftTokenAddress != address(0) && _nftTokenAddress != address(this));
        // check tokenId price
        require(_tokenIdPrice > 0);
        // init nftTokenAddress
        nftTokenAddress = ERC721(_nftTokenAddress);
        // init erc20TokenAddress
        erc20TokenAddress = ERC20(_erc20TokenAddress);
        // init tokenIdPrice
        tokenIdPrice = _tokenIdPrice;
        // transfer tokenId to contract address
        nftAddress.transferFrom(msg.sender, address(this), _tokenId);
        // mapping tokenId based on address
        tokenSeller[_tokenId] = msg.sender;
    }


    /**
     * Purchase NFT token ID by BNB
    * @dev Purchase _tokenId
    * @param _tokenId uint256 token ID
    */
    function purchaseTokenByBNB(uint256 _tokenId) public payable {
        // check msg.sender address validation
        require(msg.sender != address(0) && msg.sender != address(this),"wrong addresses interaction");
        // check balance enough
        require(msg.value >= tokenIdPrice,"not enough ETH funds");
        // get tokenId owner address
        address temp = tokenSeller[_tokenId];
        // get payable address
        address payable Seller = address(uint160(temp));
        // transfer BNB to owner address
        Seller.transfer(msg.value);
        // tokenId transfer to the msg.sender
        nftTokenAddress.transferFrom(address(this), msg.sender, _tokenId);
        // publish event
        emit Received(msg.sender, _tokenId, msg.value, address(this).balance);
    }

    /**
    * @dev Purchase _tokenId by ERC20 Token
    * @param _tokenId uint256 token ID
    * @param _amount uint256 amount of ERC20 Tooken
    */
    function purchaseTokenByERC20Token(uint256 _tokenId,uint256 _amount) public returns (bool) {
        // check msg.sender address validation
        require(msg.sender != address(0) && msg.sender != address(this),"wrong addresses interaction");
        // check balance enough
        require(_amount >= currentPrice,"not enough ERC20 token funds");
        // approve _tokenId to msg.sender
        nftAddress.approve(msg.sender,_tokenId);
        // get tokenId owner address
        address temp = tokenSeller[_tokenId];
        // transfer ERC20 token to owner of tokenId
        require(erc20TokenAddress.transferFrom(msg.sender, temp, _amount),"Not Enough tokens Transfered");
        // transfer tokenId to msg.sender
        nftTokenAddress.transferFrom(address(this), msg.sender, _tokenId);
        // publish event
        emit Received(msg.sender, _tokenId, _amount, address(this).balance);
        return true;
    }

    /**
    * @dev withdraw BNB _amount
    */
    function withdraw (address payable _payee, uint256 _amount) public onlyOwner {
        // check _payee address validation
        require(_payee != address(0) && _payee != address(this));
        // check balance enough
        require(_amount > 0 && _amount <= address(this).balance);
         // transfer BNB funds
        _payee.transfer(_amount);
        // publish event
        emit Sent(_payee, _amount, address(this).balance);
    }

    /**
    * @dev set _tokenIdPrice
    */
    function setTokenIdPrice(uint256 _tokenIdPrice) public onlyOwner {
        require(_tokenIdPrice >= 0);
        tokenIdPrice = _tokenIdPrice;
    }

     /**
    * @dev get tokenIdPrice
    */
    function getTokenIdPrice() public view returns (uint256) {
        return tokenIdPrice;
    }


}