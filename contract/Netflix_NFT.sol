pragma solidity ^0.8.0;
import "./netflix-libs/token/erc721/ERC721.sol";

contract NETFLIX_NFT is ERC721 {

    mapping (uint256 => string ) public tokenIdFiles;
    uint256 public last_token_id;

    function getLastTokenId() public view returns (uint256){
        return last_token_id;
    }

    constructor (string memory _name, string memory _symbol) public
        ERC721(_name, _symbol)
    {}


    function batchCreate(address _to , uint256[] memory _tokenIds , string[] memory _strs) public {
         FileItem[] memory fileItems;

         for (uint256 i =0; i< _tokenIds.length; i++ ){
             createItem(_strs[i], _to , _tokenIds[i]);
         }

    }



    function createItem(  string memory _str, address _to , uint256 _tokenId) public {
        last_token_id = _tokenId;
        tokenIdFiles[_tokenId] = _str;
        super._mint(_to,_tokenId); // Assigns the Token to the Ethereum Address that is specified
    }

}