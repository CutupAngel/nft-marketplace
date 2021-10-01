pragma solidity ^0.6.0;

import "../netflix-libs/access/Ownable.sol";
import "../netflix-libs/gsn/Context.sol";
import "../netflix-libs/token/bep20/BEP20.sol";
import "../netflix-libs/token/bep20/IBEP20.sol";
import "../netflix-libs/token/bep20/SafeBep20.sol";
import "../netflix-libs/math/SafeMath.sol";
import "../netflix-libs/token/erc1155/IERC1155.sol";

contract NetflixNFTFarm is Ownable {

    struct UserInfo {
        // current staked LP
        uint256 amount;
        // unix timestamp for last details update (when pointsDebt calculated)
        uint256 lastUpdateAt;
        // total points collected before latest deposit
        uint256 pointsDebt;
    }

    struct NFTInfo {
        address contractAddress;
         // NFT id
        uint256 id;
        // NFTs remaining to farm
        uint256 remaining;
        // points required to claim NFT
        uint256 price;
    }

    // safe math
    using SafeMath for uint256;
    // BEP20 token
    using SafeBEP20 for IBEP20;
    // points generated per LP token per second staked
    uint256 public emissionRate;
    // staked token
    IBEP20 lpToken;
    // list of NFTInfo
    NFTInfo[] public nftInfo;
    // mapping address based on UserInfo
    mapping(address => UserInfo) public userInfo;

    // constructor
    constructor(uint256 _emissionRate, IBEP20 _lpToken) public {
        emissionRate = _emissionRate;
        lpToken = _lpToken;
    }

    // addNFT
    function addNFT(
        address contractAddress, // Only ERC-1155 NFT Supported!
        uint256 id,
        uint256 total,
        uint256 price
    ) external onlyOwner {
        IERC1155(contractAddress).safeTransferFrom(
            msg.sender,
            address(this),
            id,
            total,
            ""
        );
        nftInfo.push(NFTInfo({
        contractAddress : contractAddress,
        id : id,
        remaining : total,
        price : price
        }));
    }

    // deposit
    function deposit(uint256 _amount) external {
        lpToken.safeTransferFrom(
            msg.sender,
            address(this),
            _amount
        );
        // get UserInfo based on address
        UserInfo storage user = userInfo[msg.sender];

        if (user.amount != 0) {
            user.pointsDebt = pointsBalance(msg.sender);
        }
        user.amount = user.amount.add(_amount);
        user.lastUpdateAt = now;
    }

    // get reward nft token
    function getReward(uint256 _nftIndex, uint256 _quantity) public {
        NFTInfo storage nft = nftInfo[_nftIndex];
        require(nft.remaining > 0, "All NFTs farmed");
        require(pointsBalance(msg.sender) >= nft.price.mul(_quantity), "Insufficient Points");
        UserInfo storage user = userInfo[msg.sender];

        // deduct points
        user.pointsDebt = pointsBalance(msg.sender).sub(nft.price.mul(_quantity));
        user.lastUpdateAt = now;

        // transfer NFT token
        IERC1155(nft.contractAddress).safeTransferFrom(
            address(this),
            msg.sender,
            nft.id,
            _quantity,
            ""
        );

        nft.remaining = nft.remaining.sub(_quantity);
    }

    // get multiple reward nft token
    function getMultipleReward(uint256[] calldata _nftIndex, uint256[] calldata _quantity) external {
        require(_nftIndex.length == _quantity.length, "Incorrect array length");
        for (uint64 i = 0; i < _nftIndex.length; i++) {
            claim(_nftIndex[i], _quantity[i]);
        }
    }

    // withdraw
    function withdraw(uint256 _amount) public {
        UserInfo storage user = userInfo[msg.sender];
        require(user.amount >= _amount, "Insufficient staked");

        // update userInfo
        user.pointsDebt = pointsBalance(msg.sender);
        user.amount = user.amount.sub(_amount);
        user.lastUpdateAt = now;

        lpToken.safeTransfer(
            msg.sender,
            _amount
        );
    }

    // withdraw all LP tokens
    function exit() external {
        withdraw(userInfo[msg.sender].amount);
    }

    // get points balance based on address
    function pointsBalance(address userAddress) public view returns (uint256) {
        UserInfo memory user = userInfo[userAddress];
        return user.pointsDebt.add(_unDebitedPoints(user));
    }

    function _unDebitedPoints(UserInfo memory user) internal view returns (uint256) {
        return now.sub(user.lastUpdateAt).mul(emissionRate).mul(user.amount);
    }

    function nftCount() public view returns (uint256) {
        return nftInfo.length;
    }

    // required function to allow receiving ERC-1155
    function onERC1155Received(
        address operator,
        address from,
        uint256 id,
        uint256 value,
        bytes calldata data
    )
    external
    returns (bytes4)
    {
        return bytes4(keccak256("onERC1155Received(address,address,uint256,uint256,bytes)"));
    }
}