#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

from web3 import Web3, HTTPProvider


# In[2]:


# web3.py instance
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))


# In[3]:


# account/contract data
account_address = "0x0026982384f0a6c6622a01a049f9fcdcab8f0c03"
account_checksum_address = w3.toChecksumAddress(account_address)
account_password = "password"
contract_address = "0xC9AC6dd6ea4D3583E0aed9D8d6D4d4380BF4bB88"


# In[4]:


publication_data = {
    "title": "Breakthrough of the Year!",
    "description": "Phenomenal description",
    "author": "mr. Very Smart Scientist",
    "hash": "ed8a1bc7221493fe5e6d7bc19f035725e19a379q"
}


# In[5]:


# load abi
abi_file = open('../contracts/publication/abi.json', 'r')
abi = json.load(abi_file)


# In[6]:


# prepare contract
contract = w3.eth.contract(address=contract_address, abi=abi)


# In[7]:


# check if the contract exists
w3.eth.getCode(contract.address)


# In[8]:


# prepare account
w3.personal.unlockAccount(account_checksum_address, account_password)


# In[9]:


# prepare contract function and estimate gas
add_publication_obj = contract.functions.addPublication(**publication_data)
gas_limit = add_publication_obj.estimateGas(
    {'from': w3.toChecksumAddress(account_checksum_address)}
)


# In[10]:


# transact data to blockchain with calculated gas limit
add_publication_tx = add_publication_obj.transact({
    "gas": gas_limit,
    "from": account_checksum_address,
})
transaction_hash = add_publication_tx.hex()
print(transaction_hash)


# In[11]:


# Wait for transaction to be mined...
print(w3.eth.waitForTransactionReceipt(transaction_hash))


# In[12]:


# try to transact with the same hash
w3.personal.unlockAccount(account_checksum_address, account_password)
add_same_publication = contract.functions.addPublication(**publication_data).transact()
print(w3.eth.waitForTransactionReceipt(add_same_publication.hex()))


# In[13]:


# get publication by known hash
publication = contract.functions.getPublicationByHash(publication_data["hash"]).call()
print(publication)


# In[14]:


# get publication count to access the array of hashes
publication_cnt = contract.functions.getPublicationCount().call()
print(publication_cnt)


# In[15]:


# get publication hash by index
publication_by_idx = contract.functions.getPublicationHash(0).call()
print(publication_by_idx)

