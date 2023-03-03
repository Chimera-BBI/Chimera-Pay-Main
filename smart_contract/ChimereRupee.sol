// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./openzeppelin-contracts-4.8.1/contracts/token/ERC20/ERC20.sol";
import "./openzeppelin-contracts-4.8.1/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "./openzeppelin-contracts-4.8.1/contracts/access/Ownable.sol";

contract ChimereRupee is ERC20, ERC20Burnable, Ownable {
    constructor() ERC20("Chimere Rupee", "INRCHMR") {}

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}