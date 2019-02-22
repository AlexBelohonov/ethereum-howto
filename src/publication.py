import json

from web3 import Web3, HTTPProvider

# web3.py instance
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))

# account/contract data
account_address = "0x0026982384f0a6c6622a01a049f9fcdcab8f0c03"
account_checksum_address = w3.toChecksumAddress(account_address)
account_password = ""
contract_address = "0xC9AC6dd6ea4D3583E0aed9D8d6D4d4380BF4bB88"

publication_data = {
    "title": "Breakthrough of the Year!",
    "description": "Phenomenal description",
    "author": "mr. Very Smart Scientist",
    "hash": "ed8a1bc7221493fe5e6d7bc19f035725e19a379e"
}

# load abi
abi_file = open('contracts/publication/abi.json', 'r')
abi = json.load(abi_file)

# prepare contract
contract = w3.eth.contract(address=account_checksum_address, abi=abi)

# prepare account
w3.personal.unlockAccount(account_checksum_address, account_password)

addPublication = contract.functions.addPublication(**publication_data).transact()


