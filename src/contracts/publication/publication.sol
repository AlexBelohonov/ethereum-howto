pragma solidity ^0.5.1;

library Structures {
    struct Book {
        string title;
        string description;
        string author;
        bool exists;
    }
}

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
    //event LogCoinsMinted(uint amount);
    string[] public hashes;

    function getPublicationCount () public view returns (uint) {
        return hashes.length;
    }

    function getPublicationHash (uint index) public view returns (string memory) {
        return hashes[index];
    }

    function getPublicationByHash (string memory hash) public view returns (string[3]) {
        return [_storage[hash].title, _storage[hash].description, _storage[hash].author];
    }

    function addPublication (string memory title, string memory description, string memory hash, string memory author) public onlyOwner() {
        require(!_storage[hash].exists, "OMG, stop that!");
        _storage[hash] = Structures.Book(title, description, author, true);
        hashes.push(hash);
    }
}
