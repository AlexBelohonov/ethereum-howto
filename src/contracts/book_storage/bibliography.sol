pragma solidity ^0.5.1;

import "./structures.sol";

/**
 * @title Ownable
 * The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {

  address public owner;

  /**
   * The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  constructor() internal {
    owner = msg.sender;
  }

  /**
   * Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(msg.sender == owner);
    // Do not forget the "_;"! It will
    // be replaced by the actual function
    // body when the modifier is used.
    _;
  }

  /**
   * Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) internal onlyOwner {
    require(newOwner != address(0));
    owner = newOwner;
  }
}


contract EBookStorage is Ownable {

    mapping (string => string) basicData;
    string[] public basicKeys;
    Structures.Book[] public books;

    /**
    * Allows to compare strings, calls within the current contract
    */
    function compareStrings(string memory s1, string memory s2) private pure returns(bool){
        return keccak256(abi.encode(s1)) == keccak256(abi.encode(s2));
    }

    /**
    * Allows to get length of basicKeys array
    */
    function getKeysCount () public view returns (uint) {
        return basicKeys.length;
    }

    /**
    * Allows the current owner to set any key/value data
    */
    function setBasicData (string memory key, string memory value) public onlyOwner() {
        basicKeys.push(key);
        basicData[key] = value;
    }

    /**
    * Allows to get any key/value data
    */
    function getBasicData (string memory key) public view returns (string memory) {
        return basicData[key];
    }

    /**
    * Allows the current owner to add a book with its metadata
    */
    function addBook (string memory name, string memory description, uint year, string memory author)
    public
    onlyOwner()
    returns(uint) {
        require(!compareStrings(name, ""), "Name is required argument!");
        require(!compareStrings(description, ""), "Description is required argument!");
        require(!compareStrings(author, ""), "Author is required argument!");
        books.push(Structures.Book(name, description, year, author));
        return books.length;
    }
}
