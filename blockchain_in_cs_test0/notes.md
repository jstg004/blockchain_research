# Blockchain

- blockchain is a database of all transactions which have
  occurred since the 1st bitcoin transaction (genesis block)

## miners

- entities who's only goal is to insert a transaction into the
  blockchain
- do not modify the blockchain everytime they revceive a
  trsnaction
- each miner attempts to add up a batch of transactions at the
  same time
  - this batch of transactions is a block
- other nodes on the network confirm that the new block obeys
  the rules set in the bitcoin protocol
- if 2 miners add a block at the same time there is a fork
  - only the branch of the fork with the most work will continue
- if a miner attempts to include an invalid transaction in a
  block - the other nodes will not recognisze the transaction
  - the miner loses the investment (work) spent on creating the
    block
- once a miner submits a valid block - all transactions inside
  the block are considered _confirmed_
  - all miners must discard their current worka nd begin working
    on a new block using new transactions (not in that block)
  - a confirmed block is added to the blockchain as the most
    recent block

## bitcoin

- a bitcoin transaction is a row in a database that cannot be
  deleted or modified
- 2 ways to verify that a specific transaction exists:
  1. check the entire blockchain
  2. request a partial Merkle tree
     - Simple Payment Verification (SPV)