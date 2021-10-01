pragma solidity >=0.5.0;

interface INetflixSwapBEP721 {
    event Approval(address indexed owner, address indexed spender, uint256 tokenId);
    event Transfer(address indexed from, address indexed to, uint256 tokenId);

    function name() external pure returns (string memory);

    function symbol() external pure returns (string memory);

    function totalSupply() external view returns (uint256);

    function balanceOf(address owner) external view returns (uint256);

    function allowance(address owner, address spender) external view returns (uint256);

    function approve(address spender, uint256 tokenId) external returns (bool);

    function transfer(address to, uint256 tokenId) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);

    function DOMAIN_SEPARATOR() external view returns (bytes32);

    function PERMIT_TYPEHASH() external pure returns (bytes32);

    function nonces(address owner) external view returns (uint256);

    function permit(
        address owner,
        address spender,
        uint256 value,
        uint256 deadline,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) external;
}