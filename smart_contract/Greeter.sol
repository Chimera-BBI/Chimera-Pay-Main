// This contract is written in Solidity version 0.4.21
pragma solidity >=0.4.21;

// Defining the contract
contract Greeter {
  // Declaring the `greeting` variable as a public string
  string public greeting;

  // Constructor function that is called when the contract is deployed
  constructor() public {
    // Setting the initial greeting to "Hello"
    greeting = 'Hello';
  }

  // Function that allows the greeting to be updated
  function setGreeting(string memory _greeting) public {
    // Updating the greeting
    greeting = _greeting;
  }

  // Function that returns the current greeting
  function greet() view public returns (string memory) {
    // Returning the greeting
    return greeting;
  }
}
