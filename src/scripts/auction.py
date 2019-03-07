#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json

from web3 import Web3, HTTPProvider


# In[ ]:


# load abi and bytecode
with open('../contracts/auction/abi.json', 'r') as abi_file:
    abi = abi_file.read()
with open('../contracts/auction/bytecode', 'r') as bc:
    bytecode = bc.read()


# In[ ]:


# web3.py instance
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))


# In[ ]:


# account data
owner_account_address = w3.toChecksumAddress("0x0026982384f0a6c6622a01a049f9fcdcab8f0c03")
guest_account_address = w3.toChecksumAddress("0x00221666689B516DF1f74d8E66b4F6747BB9D038")
owner_account_password = "password"
guest_account_password = "second_password"


# In[ ]:


# get address balance before auction
begin_owner_balance = w3.eth.getBalance(owner_account_address)
print(begin_owner_balance, "wei")
print(Web3.fromWei(begin_owner_balance, "ether"), "ether")


# In[ ]:


# prepare contract object
auction_deploy = w3.eth.contract(abi=abi, bytecode=bytecode)


# In[ ]:


# unlock account before transaction
w3.personal.unlockAccount(owner_account_address, owner_account_password)
# Submit the transaction which deploys the contract with biddingTime 120 seconds
tx_hash = auction_deploy.constructor(18).transact({
    "from": owner_account_address
})
print(tx_hash.hex())


# In[ ]:


# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)


# In[ ]:


# Create the contract instance with the newly-deployed address (can't use without address)
contract = w3.eth.contract(
    # address=tx_receipt.contractAddress,
    address = w3.toChecksumAddress("0x61d9b0bbbe187e44493ebd6a32ff440b0b14a6a9"),
    abi=abi,
)


# In[ ]:


# unlock account before transaction
w3.personal.unlockAccount(owner_account_address, owner_account_password)


# In[ ]:


# prepare contract function object
bid_obj = contract.functions.bid()


# In[ ]:


# 1 ether 124,55$ | 5$ == 0.040 == 40 000 000 000 000 000 wei
bid_tx = bid_obj.transact({
    "from": owner_account_address,
    "value": Web3.toWei(0.040, 'ether'),
})
print(bid_tx.hex())


# In[ ]:


# Wait for the transaction to be mined, and get the transaction receipt
print(w3.eth.waitForTransactionReceipt(bid_tx))


# In[ ]:


# get highestBidder using call()
print(contract.functions.highestBidder().call(), "highestBidder")
# get highestBid
print(contract.functions.highestBid().call(), "highestBid")


# In[ ]:


# make another bid with other account, bid is less then previous
w3.personal.unlockAccount(guest_account_address, guest_account_password)


# In[ ]:


# 0.03 == 30 000 000 000 000 000 wei
bid_tx = bid_obj.transact({
    "from": guest_account_address,
    "value": Web3.toWei(0.03, 'ether'),
})
print(w3.eth.waitForTransactionReceipt(bid_tx))


# In[ ]:


# results shoud be the same as above
# get highestBidder using call()
print(contract.functions.highestBidder().call(), "highestBidder")
# get highestBid
print(contract.functions.highestBid().call(), "highestBid")


# In[ ]:


# unlock account before transaction
w3.personal.unlockAccount(owner_account_address, owner_account_password)


# In[ ]:


# withdraw bid, owner
withdraw_obj = contract.functions.withdraw()
withdraw_tx = withdraw_obj.transact({
    "from": owner_account_address,
})
print(withdraw_tx.hex())


# In[ ]:


# Wait for the transaction to be mined, and get the transaction receipt
print(w3.eth.waitForTransactionReceipt(withdraw_tx))


# In[ ]:


# results different - second account shoud be here
# get highestBidder using call()
print(contract.functions.highestBidder().call(), "highestBidder")
# get highestBid
print(contract.functions.highestBid().call(), "highestBid")


# In[ ]:


# get auctionEndTime using call()
auction_end_time = contract.functions.auctionEndTime().call()
print(auction_end_time)
print(datetime.utcfromtimestamp(auction_end_time).strftime('%Y-%m-%d %H:%M:%S'))


# In[ ]:


# get beneficiary address
print(contract.functions.beneficiary().call())


# In[ ]:


# unlock account to transact
w3.personal.unlockAccount(owner_account_address, owner_account_password)


# In[ ]:


# finish auction if now >= auctionEndTime, transfer data of highestBid to auction owner
auction_end_obj = contract.functions.auctionEnd()
auction_end_tx = auction_end_obj.transact({
    "from": owner_account_address,
})
print(w3.eth.waitForTransactionReceipt(auction_end_tx.hex()))


# In[ ]:


# get address balance after auction
owner_balance = w3.eth.getBalance(owner_account_address)
print(Web3.fromWei(begin_owner_balance, "ether"), "begin balance 'ether'")
print(Web3.fromWei(owner_balance, "ether"), "end balance 'ether'")

