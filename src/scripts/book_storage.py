#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

from web3 import Web3, HTTPProvider


# In[2]:


# web3.py instance
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))


# In[8]:


# account/contract data
account_checksum_address = w3.toChecksumAddress("0x0026982384f0a6c6622a01a049f9fcdcab8f0c03")
account_password = "password"
contract_address = w3.toChecksumAddress("0xfbec4e67e22ab0da80c37fc994b169f4632b343a")


# In[15]:


book_data = (
    "The Hobbit",
    "The Hobbit is set within Tolkien's fictional universe and follows the quest of home-loving hobbit" \
    " Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon. Bilbo's journey takes" \
    " him from light-hearted, rural surroundings into more sinister territory.",
    1937,
    "John Ronald Reuel Tolkien",
)


# In[5]:


basic_data = ("Storage", "Main Book Storage")


# In[6]:


# load abi
abi_file = open('../contracts/book_storage/abi.json', 'r')
abi = json.load(abi_file)


# In[9]:


# prepare contract
contract = w3.eth.contract(address=contract_address, abi=abi)


# In[10]:


# check if the contract exists (optional)
w3.eth.getCode(contract.address)


# In[11]:


# prepare account
w3.personal.unlockAccount(account_checksum_address, account_password)


# In[16]:


# prepare contract function and estimate gas
addBook_obj = contract.functions.addBook(*book_data)
gas_limit = addBook_obj.estimateGas(
    {'from': w3.toChecksumAddress(account_checksum_address)}
)
print(gas_limit)


# In[17]:


# add book data to blockchain with calculated gas limit
addBook_tx = addBook_obj.transact({
    "gas": gas_limit,
    "from": account_checksum_address,
})
transaction_hash = addBook_tx.hex()
print(transaction_hash)


# In[19]:


# Wait for transaction to be mined...
print(w3.eth.waitForTransactionReceipt(transaction_hash))


# In[23]:


# get data from array without transaction
books = contract.call().books(0)
print(books)


# In[27]:


# prepare setBasicData contract function and estimate gas
setBasic_obj = contract.functions.setBasicData(*basic_data)
gas_limit = setBasic_obj.estimateGas(
    {'from': w3.toChecksumAddress(account_checksum_address)}
)
print(gas_limit)


# In[28]:


# unlock account for the transaction
w3.personal.unlockAccount(account_checksum_address, account_password)


# In[29]:


# setBasicData to contract with calculated gas limit
setBasic_tx = setBasic_obj.transact({
    "gas": gas_limit,
    "from": account_checksum_address,
})
transaction_hash = setBasic_tx.hex()
print(transaction_hash)


# In[30]:


# Wait for transaction to be mined...
print(w3.eth.waitForTransactionReceipt(transaction_hash))


# In[31]:


# get basic data by key without transaction
basic_data = contract.call().getBasicData(basic_data[0])
print(basic_data)


# In[32]:


# get basic_data_keys_cnt without transaction to understand the range of the basicKeys array
basic_data_keys_cnt = contract.call().getKeysCount()
print(basic_data_keys_cnt)


# In[37]:


# get kyes from basicKeys array without transaction and then use it to get the data
for i in range(0, basic_data_keys_cnt):
    bs_key = contract.call().basicKeys(i)
    bs_value = contract.call().getBasicData(bs_key)
    print(f"{bs_key}: {bs_value}")

