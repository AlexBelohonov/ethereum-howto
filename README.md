# ethereum-howto
Trying basics of development for Ethereum blockchain using Solidity + Python.
There are 3 contracts and 3 python scenarious to try them out.

######Simple Open Auction (from Solidity documentation)
The general idea of the following simple auction contract is that everyone can send their bids during a bidding period. The bids already include sending money / ether in order to bind the bidders to their bid. If the highest bid is raised, the previously highest bidder gets her money back. After the end of the bidding period, the contract has to be called manually for the beneficiary to receive their money - contracts cannot activate themselves.

######Publication
PoA implementation - allows to store hash of the publication together with metadata like: title, description, author. Hash must be unique. Allows to get hash by it's internal index and by publication metadata by it's hash. Uses Ownable pattern.

######Book Storage
Allows to save book/publication info like: title, description, year, author. Basic idea is to work with public data types like mapping, arrays. Uses Ownable pattern.
