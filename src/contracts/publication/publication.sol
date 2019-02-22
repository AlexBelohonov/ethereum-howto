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


contract EPublication is Ownable {

    mapping (string => Structures.Book) private _storage;
    string[] private hashes;

    /**
    * Get count of Publication hashes
    */
    function getPublicationCount () public view returns (uint) {
        return hashes.length;
    }

    /**
    * Allows to get a hash by an index
    */
    function getPublicationHash (uint index) public view returns (string memory) {
        return hashes[index];
    }

    /**
    * Allows to return Publication data
    */
    function getPublicationByHash (string memory hash) public view returns (string memory, string memory, string memory) {
        return (_storage[hash].title, _storage[hash].description, _storage[hash].author);
    }

    /**
    * Allows the current owner to add a publication with its metadata
    */
    function addPublication (string memory title, string memory description, string memory author, string memory hash)
    public onlyOwner()
    returns (uint) {
        require(!_storage[hash].exists, "Publication hash should be unique!");
        _storage[hash] = Structures.Book(title, description, author, true);
        hashes.push(hash);
        return hashes.length;
    }

}
