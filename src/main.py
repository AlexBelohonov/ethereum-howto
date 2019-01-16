import json

from web3 import Web3, HTTPProvider

# web3.py instance
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
print(w3.eth.accounts)
w3.toWei
# account data
rp_account_address = "0x427b2dfa3ad25e77a8b514dcdcd96da827bcb636"
rp_contract_address = "0xe94bacbfb253d6328fe1965df549981c0e81b1e1"

# load abi
abi_file = open('contract/abi.json', 'r')
abi = json.load(abi_file)
# ? other way?
w3.personal.unlockAccount(
    w3.toChecksumAddress(rp_account_address),
    "")

contract = w3.eth.contract(address=w3.toChecksumAddress(rp_contract_address),
                           abi=abi)

# prepare contract function object
# basic_data_obj = contract.functions.setBasicData("fullname", "John Ronald Reuel Tolkien")
#
# gas_limit = basic_data_obj.estimateGas(
#     {'from': w3.toChecksumAddress(rp_account_address)}
# )
#
# transaction = basic_data_obj.transact(
#     {'from': w3.toChecksumAddress(rp_account_address), 'gas': gas_limit}
# )
#
# print('gas', gas_limit)
# print(transaction.hex())
# "0x24399a00db1f74e29c2a77d0976dd110314fdbef28a61f4eebc86b1de93ef638"

# response = w3.eth.getTransactionReceipt(transaction.hex())

# {'blockHash': HexBytes('0x4e84f031ff7f56b265006a666cec3958a7d6710d3c87c9f8130096ff6f1d035e'),
#  'blockNumber': 4670420,
#  'contractAddress': None,
#  'cumulativeGasUsed': 702914,
#  'from': None,
#  'gasUsed': None,
#  'logs': [],
#  'root': None,
#  'status': 1,
#  'to': None,
#  'transactionHash': HexBytes('0x24399a00db1f74e29c2a77d0976dd110314fdbef28a61f4eebc86b1de93ef638'),
#  'transactionIndex': 11}


#response = w3.eth.getTransaction("0x24399a00db1f74e29c2a77d0976dd110314fdbef28a61f4eebc86b1de93ef638")

# {'blockHash': HexBytes('0x4e84f031ff7f56b265006a666cec3958a7d6710d3c87c9f8130096ff6f1d035e'),
#  'blockNumber': 4670420, 'chainId': '0x3', 'condition': None, 'creates': None,
#  'from': '0x427B2DfA3aD25e77A8B514DCDcd96DA827Bcb636', 'gas': 146488, 'gasPrice': 1000000000,
#  'hash': HexBytes('0x24399a00db1f74e29c2a77d0976dd110314fdbef28a61f4eebc86b1de93ef638'),
#  'input': '0x206471d800000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000966756c6c5f6e616d65000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000194a6f686e20526f6e616c6420526575656c20546f6c6b69656e00000000000000',
#  'nonce': 1,
#  'publicKey': HexBytes(
#      '0x16dce8636e20dd0e0513c116c9cd4c1eb2560d7b2a6ac0777fa3db576b9376c2991e26a9fe48a8d8c90c1420dba1a3893a93113f6a20269373079547ca70447e'),
#  'r': HexBytes('0x7494ae2576222ef7e4383e8ff3323a90238ed243e5de2ec9a1e9852c77e9e309'),
#  'raw': HexBytes(
#      '0xf9012901843b9aca0083023c3894e94bacbfb253d6328fe1965df549981c0e81b1e180b8c4206471d800000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000966756c6c5f6e616d65000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000194a6f686e20526f6e616c6420526575656c20546f6c6b69656e0000000000000029a07494ae2576222ef7e4383e8ff3323a90238ed243e5de2ec9a1e9852c77e9e309a04c0bedbef0d79b5609256f00c180a701cf9ce81ffd7652f4955a8b250eef03d9'),
#  's': HexBytes('0x4c0bedbef0d79b5609256f00c180a701cf9ce81ffd7652f4955a8b250eef03d9'),
#  'standardV': 0,
#  'to': '0xE94bacBfB253D6328fE1965df549981C0E81b1E1',
#  'transactionIndex': 11,
#  'v': 41,
#  'value': 0}

# get data from the Network
# transaction = contract.functions.getBasicData("fullname").transact(
#     {'from': w3.toChecksumAddress(rp_account_address)}
# )
#
# print(transaction.hex())
book_description = "The Hobbit is set within Tolkien's fictional universe and follows the quest of home-loving hobbit" \
                   " Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon. Bilbo's journey takes" \
                   " him from light-hearted, rural surroundings into more sinister territory."

# transaction = contract.functions.addBook("The Hobbit", book_description, 1937).transact(
#     {'from': w3.toChecksumAddress(rp_account_address)}
# )

# print(transaction.hex())
# 0x8e8715d9eeb37a52fbf1d68a84820bd32ba4bb371838876e61cd6247d9256927

# fullname = contract.functions.getBasicData("fullname").call(
#     {'from': w3.toChecksumAddress(rp_account_address)}
# )
# print(fullname)

books = contract.call().books(0)
print(books)
# ['The Hobbit',
# "The Hobbit is set within Tolkien's fictional universe and follows the quest of home-loving hobbit Bilbo Baggins
# to win a share of the treasure guarded by Smaug the dragon. Bilbo's journey takes him from light-hearted, rural
# surroundings into more sinister territory.",
# 1937]



# send ether to another account
from_addr = "0x427b2dfa3ad25e77a8b514dcdcd96da827bcb636"
to_addr = "0xdC88f96BCBEdbD92539Fefe2c91148Cb67d272E4"

transaction = w3.eth.sendTransaction({'from': w3.toChecksumAddress(from_addr),
                                      'to': w3.toChecksumAddress(to_addr),
                                      'value': w3.toWei(0.01, 'ether'),
                                      'gasPrice': w3.toWei(1, 'shannon')})
print(transaction.hex())

# https://web3py.readthedocs.io/en/stable/web3.eth.account.html#local-vs-hosted
# https://web3py.readthedocs.io/en/stable/examples.html?highlight=token
# https://web3py.readthedocs.io/en/stable/examples.html#currency-conversions
# https://web3py.readthedocs.io/en/stable/filters.html#filter-class
