# notes from _The Bitcoin Lightning Network: Scalable Off-Chain Instant Payments_

- by Joseph Poon and Thaddeus Dryja
- January 2016

## The Bitcoin Blockchain Scalability Problem

- the Bitcoin blockchain excells as a distributed ledger
- as a large scale payment platform it suffers from scaling issues
- the blockchain is a gossip protocol
  - all state modifications to the ledger are broadcasted to all participants
  - consensus of the state is agreed upon through this protocol
  - each node in the Bitcoin network must know about every single transaction
    that occurs in the network
- for Bitcoin to scale to the amount of transactions needed to use it for daily
  transactions for the majority of the population of the world it would require
  huge amounts of data and is not feasible with current technology
- increasing block sizes to handle more transactions per second could result
  in only miners who could handle such large data loads to be able to validate
  the blocks
  - this can result in centralization of the network validators
  - can result in higher fees
- to avoid centralization Bitcoin needs to be able to be validated by a single
  consumer level computer on a home broadband connection
  - full validation must be able to occur cheaply - ensures low transaction fees
- currently in order to greatly increase the amount of transactions per second
  with Bitcoin - transactions must be made off the Bitcoin blockchain
  - on a sidechain

## A Network of Micropayment Channels Can Solve Scalability

- in a blockchain - if only 2 participants care about an everyday recurring
  transaction - it is not necessary for all other nodes in the network to
  kow about that transaction
  - preferable to only have the bare minimum information on the blockchain
  - a net settlement of the relationship between these 2 participants can be
    completed at a later date and added to the blockchain at that time]
    - this allows for many transactions to be completed without bloating the
      main blockchain
    - also removes the need for a trusted centralized counterparty
- a trustless structure can be achieved by using time locks as a component
  to global consensus
- using a network of micropayment channels allows for Bitcoin to scale to
  billions of transactions per day using readily available modern compute power
- many payments can be sent in a single micropayment channel
  - enables one to send large amounts of funds to another party in a
    decentralized manner
- micropayment channels create a relationship between 2 parties to perpetually
  update balances
  - the broadcast to the blockchain is deferred and sent in a single transaction
    which nets out the total balance between the 2 parties
  - allows the financial relationships between 2 parties to be trustlessly
    deferred to a later date without risk of counterparty default
- micropayment channels used real Bitcoin transactions
  - broadcasts to the blockchain are deferred so that both parties can gaurantee
    their current balance on the blockchain
    - real Bitcoin communicated and exchanged off-chain

### Micropayment Channels Do Not Require Trust