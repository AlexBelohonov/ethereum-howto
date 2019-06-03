#!/usr/bin/env python
# coding: utf-8

# In[29]:


from web3 import Web3, HTTPProvider


# In[30]:


# load abi and bytecode
with open('../contracts/auction/abi.json', 'r') as abi_file:
    abi = abi_file.read()
with open('../contracts/auction/bytecode', 'r') as bc:
    bytecode = bc.read()


# In[31]:


# web3.py instance
w3 = Web3(HTTPProvider('http://localhost:8545'))


# In[32]:


# account data
owner_account_address = w3.toChecksumAddress('0xdc88f96bcbedbd92539fefe2c91148cb67d272e4')
guest_account_address = w3.toChecksumAddress('0x0635c434ec5f88f7dc8e44e0b878116d71d2a658')
owner_account_password = 'password'
guest_account_password = 'second_password'


# In[33]:


# prepare contract object
auction_deploy = w3.eth.contract(abi=abi, bytecode=bytecode)


# In[34]:


# get address balance before auction
begin_owner_balance = w3.eth.getBalance(owner_account_address)
print(begin_owner_balance, 'wei')
print(Web3.fromWei(begin_owner_balance, 'ether'), 'ether')


# In[35]:


# unlock account before transaction
w3.personal.unlockAccount(owner_account_address, owner_account_password)
# Submit the transaction which deploys the contract with biddingTime 300 seconds (5 minutes)
tx_hash = auction_deploy.constructor(300).transact({
    'from': owner_account_address
})
print(tx_hash.hex())


# In[36]:


# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)


# In[37]:


# Create the contract instance with the newly-deployed address (can't use without address)
contract = w3.eth.contract(
    address = w3.toChecksumAddress(tx_receipt['contractAddress']),
    abi=abi,
)


# In[38]:


# unlock account before transaction
w3.personal.unlockAccount(owner_account_address, owner_account_password)


# In[39]:


# prepare contract function object
bid_obj = contract.functions.bid()
bid_gas_estimated = bid_obj.estimateGas({
    'from': owner_account_address,
    'value': Web3.toWei(0.03, 'ether')
})
print(w3.eth.gasPrice, 'current gas price in Wei, testnet')
print(bid_gas_estimated, 'estimated for the transaction')
transaction_cost = float(Web3.fromWei(w3.eth.gasPrice * bid_gas_estimated, 'ether')) * 132.45
print(transaction_cost, 'payed for the transactions in USD')


# In[40]:


# 1 ether 132,45$ | 3.97$ == 0.03 == 30 000 000 000 000 000 wei
bid_tx = bid_obj.transact({
    'from': owner_account_address,
    'value': Web3.toWei(0.03, 'ether'),
    'gas': bid_gas_estimated,
    'gas_price': w3.eth.gasPrice
})
print(bid_tx.hex())


# In[41]:


# Wait for the transaction to be mined, and get the transaction receipt
print(w3.eth.waitForTransactionReceipt(bid_tx))


# In[42]:


# get highestBidder using call()
print(contract.functions.highestBidder().call(), 'highestBidder')
# get highestBid
print(contract.functions.highestBid().call(), 'highestBid')


# In[43]:


# make another bid with other account, bid is less then previous
w3.personal.unlockAccount(guest_account_address, guest_account_password)


# In[44]:


# 1 ether 132,45$ | 5.30$ == 0.040 == 40 000 000 000 000 000 wei
bid_tx = bid_obj.transact({
    'from': guest_account_address,
    'value': Web3.toWei(0.040, 'ether'),
})
print(w3.eth.waitForTransactionReceipt(bid_tx))


# In[45]:


# get highestBidder using call()
print(contract.functions.highestBidder().call(), 'highestBidder')
# get highestBid
print(contract.functions.highestBid().call(), 'highestBid')


# In[46]:


# get address balance before withdraw
begin_owner_balance = w3.eth.getBalance(owner_account_address)
print(begin_owner_balance, 'wei')
print(Web3.fromWei(begin_owner_balance, 'ether'), 'ether')


# In[47]:


# unlock account before transaction
w3.personal.unlockAccount(owner_account_address, owner_account_password)


# In[48]:


# withdraw bid, owner
withdraw_obj = contract.functions.withdraw()
withdraw_tx = withdraw_obj.transact({
    'from': owner_account_address,
})
print(withdraw_tx.hex())


# In[49]:


# Wait for the transaction to be mined, and get the transaction receipt
print(w3.eth.waitForTransactionReceipt(withdraw_tx))


# In[50]:


# get address balance after withdraw
begin_owner_balance = w3.eth.getBalance(owner_account_address)
print(begin_owner_balance, 'wei')
print(Web3.fromWei(begin_owner_balance, 'ether'), 'ether')


# In[55]:


# get auctionEndTime using call()
auction_end_time = contract.functions.auctionEndTime().call()
print(auction_end_time)
from datetime import datetime
print(datetime.utcfromtimestamp(auction_end_time).strftime('%Y-%m-%d %H:%M:%S'))


# In[56]:


# get beneficiary address
print(contract.functions.beneficiary().call())


# In[57]:


# unlock account to transact
w3.personal.unlockAccount(owner_account_address, owner_account_password)


# In[58]:


# finish auction if now >= auctionEndTime, transfer data of highestBid to auction owner
auction_end_obj = contract.functions.auctionEnd()
auction_end_tx = auction_end_obj.transact({
    'from': owner_account_address,
})
print(w3.eth.waitForTransactionReceipt(auction_end_tx.hex()))


# In[59]:


# get address balance after auction
owner_balance = w3.eth.getBalance(owner_account_address)
print(Web3.fromWei(begin_owner_balance, 'ether'), 'begin balance ether')
print(Web3.fromWei(owner_balance, 'ether'), 'end balance ether')


# In[ ]:




