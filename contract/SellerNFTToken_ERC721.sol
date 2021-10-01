// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.8.0;

import "./netflix-libs/token/erc721/ERC721.sol";


contract SellerNFTToken_ERC721 is ERC721 {

    struct RECORD {
        address owner;
        string fileId;
        uint256 startTokenId;
        uint256 lastTokenId;
        bool isExpired;
    }

    struct TimeLock {
        address owner;
        uint startDateTime;
        uint endDateTime;
    }

    // mapping start and last token id based on address
    mapping (address => mapping (string => RECORD)) internal recordMap;
    mapping (address => mapping (string => TimeLock)) internal timeLockMap;
    // last token id
    uint256 public last_token_id;


    constructor (string memory _name, string memory _symbol) public
        ERC721(_name, _symbol)
    {}

    // _receiver : Receiver address
    // _RECORD_START_TOKEN_ID : Start token id in NFT token
    // _RECORD_LAST_TOKEN_ID : Last token id in NFT token
    function NETFLIX_NFT_RECORD_ADD (   string _fileId,
                                        address _receiver,
                                        uint256 _RECORD_START_TOKEN_ID,
                                        uint256 _RECORD_LAST_TOKEN_ID) public {
        // map _fileId to RECORD
        recordMap[_receiver][_fileId] = RECORD(_receiver,_fileId, _RECORD_START_TOKEN_ID,_RECORD_LAST_TOKEN_ID);
        // send SellerNFTToken
        last_token_id +=1;
        // Assigns the Token to the Ethereum Address that is specified
        super._mint(_receiver, last_token_id);
        // check _receiver has exipred NFT tokens
        // get TimeLock
        TimeLock timeLock = timeLockMap[_receiver][_fileId];
         // get RECORD
        RECORD record = recordMap[_receiver][_fileId];
        // check diff
        uint diff = (endDate - startDate) / 60 / 60 / 24;
        if (diff == 0 && !record.isExpired){
            // burn token because time is expired
            _burn(_receiver , address(0) ,  1  * (10 ** uint256(decimals())));
            // make as expired
            record.isExpired = true;
        }
    }

    // ADD NETFLIX_NFT_FIXEDTERM
    function NETFLIX_NFT_FIXEDTERM (address ownerOfTokenId, string _fileId, uint _START_DATETIME, uint _LAST_DATETIME)  public {
        // map _fileId to TimeLock
        timeLockMap[ownerOfTokenId][_fileId] = TimeLock(ownerOfTokenId  , _START_DATETIME, _LAST_DATETIME);
    }

    // Get RECORD
    function getRECORD(string _fileId) public virtual returns (RECORD) {
        return recordMap[msg.sender][_fileId];
    }



}
