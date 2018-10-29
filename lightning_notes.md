# notes from _The Bitcoin Lightning Network: Scalable Off-Chain Instant Payments_

- by Joseph Poon and Thaddeus Dryja
- January 2016

## The Bitcoin Blockchain Scalability Problem

- the Bitcoin blockchain excels as a distributed ledger
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
  - broadcasts to the blockchain are deferred so that both parties can guarantee
    their current balance on the blockchain
    - real Bitcoin communicated and exchanged off-chain

### Micropayment Channels Do Not Require Trust

- cryptographic signatures allow a blockchain to prove who owns what
- a blockchain ledger is used as a timestampting system
- it is desireable to create a system which does not actively use this
  timestamping system unless absolutely necessary
  - it is costly to the network to use
  - both parties could commit to signing a transaction and not broadcasting the
    transaction
- with micropayment channels only 2 states are required
  1. current correct balance
  2. any old deprecated balances
- there is only a single correct current balance
  - can be many old balances which are deprecated
- it is possible in Bitcoin to devise a Bitcoin script where all old
  transactions are invalidated
  - only the new transaction is valid
- invalidation is enforced by a Bitcoin output script and dependent transactions
  which force the other party to give all their funds to the channel
  counterparty
  - by taking all funds as a penalty to give to the other - all old transactions
    are thereby invalidated
  - this invalidation process can exist through a process of channel consensus
    where if both parties agree on current ledger states
    - as well as building new states
    - then the real balance gets updated
  - the balance is reflected on the blockchain only when a single party
    disagrees
  - this system is not an independent overlay network
  - this system is a deferral of state on the current system
    - enforcement is still occurring on the blockchain itself
      - deferred to future dates and transactions

### A Network of Channels

- micropayment channels only create a relationship between 2 parties
  - everyone is required to create channels with everyone else
  - this does not solve the scalability problem
- Bitcoin scalability can be achieved using a large network of micropayment
  channels
- it is possible to create a near-infinite amount of transactions in the network
  - in a large network of channels on the Bitcoin blockchain where all users are
    participating on this graph by having at least 1 channel open on the
    Bitcoin blockchain
  - only transactions that are broadcasted on the Bitcoin blockchain prematurely
    are with uncooperative channel counterparties
- the Bitcoin transaction outputs have a hashlock and a timelock
  - the channel counterparty is unable to steal funds
  - Bitcoins can be exchanged without counterparty theft
  - by using staggered timeouts - it is possible to send funds via multiple
    intermediaries in a network without risk of intermediary theft of funds

## Bidirectional Payment Channels

- micropayment channels permit a simple deferral of a transaction state to be
  broadcast at a later time
- contracts are enforced by creating a responsibility for 1 party to
  broadcast transactions before or after certain dates
- in a blockchain with a decentralized timestamping system:
  - possible to used clocks as a component of decentralized consensus to
    determine data validity and present states as a method to order events
- timeframes are created in which certain states can be broadcasted and then
  later invalidated
  - possible to create complex contracts using Bitcoin transaction scripts
  - the Lightning Network's bidirectional microparment channel requires
    the malleability soft-fork to enable near-infinite scalability while
    mitigating risks of intermediate node default
- multiple micropayment channels can be chained together allowing the creation
  of a network of transaction paths
  - paths can be routed using BGP-like systems
  - sender can designate a particular path to the recipient
  - output scripts are encumbered by a hash
    - the hash is generated by the recipient
  - by disclosing the input to the hash - the recipient's counterparty is able
    to pull funds along the route

### The Problem of Blame in Channel Creation

- in order to participate in this payment network - one must create a
  micropayment channel with another participant on this network

#### Creating an Unsigned Funding Transaction

- initial channel Funding Transaction is created
  - 1 or both channel counterparties fund the inputs of the transaction
- both parties create the inputs and outputs for the transaction
  - both do not sign the transaction
- the output for the Funding Transaction is a single 2-of-2 multisignature
  script
- both participants do not exchange signatures for the Funding Transaction
  until they have created spends from this 2-of-2 output refunding the original
  amount back to its respective funders
  - transactions are not signed to allow for one to spend from a transaction
    which does not yet exist
- if 2 parties exchange the signatures from the Funding Transaction without
  being able to broadcast spends from the Funding transaction
  - the funds may be locked up forever if either party does not cooperate
    - or is other coin loss occurs through hostage scenarios
      - where one pays for the cooperation from the counterparty
  - the 2 parties exchange inputs to fund the Funding Transaction and exchange
    1 key to use to sign with at a later point
    - this allows for knowledge of which inputs are used to determine the total
      value of the channel
    - the key is used for the 2-of-2 output for the Funding Transaction
      - both parties must agree to spend from the Funding Transaction

#### SPending from an Unsigned Transaction

- Lightning Network uses a ```SIGHASH_NOINPUT``` transaction to spend from the
  2-of-2 Funding Transaction output
  - necessary to spend from a transaction for which the signatures are not yet
    exchanged
  - ```SIGHASH_NOINPUT``` is implemented into Bitcoin by a soft-fork
    - it ensures transactions can be spent from before being signed by all
      parties
  - without ```SIGHASH_NOINPUT``` it is not possible to generate a spend from
    a transaction without exchanging signatures
    - spending the Funding Transaction (parent) requires a transaction ID as
      part of the signature in the child's input
    - the parent's signature is a component of the transaction ID
    - both parties need to exchange their signatures of the parent transaction
      before the child can be spent
    - one or both parties are able to broadcast the parent before the child
      exists
    - ```SIGHASH_NOINPUT``` is used to get around this restriction by permitting
      the child to spend without signing the input
- ```SIGHASH_NOINPUT``` order of operations:
  1. create the parent Funding Transaction
  2. create the children Commitment Transactions and all spends from the
     Commitment Transactions
  3. sign the children
  4. exchange the signatures for the children
  5. sign the parent
  6. exchange the signatures for the parent
     - if 1 party fails on this step - the parent can either be spent and become
       the parent transaction or the inputs to the parent transaction can be
       double-spent - this entire transaction path is invalidated
  7. broadcast the parent on the blockchain

#### Commitment Transactions: Unenforceable Construction

- when the unsigned/unbroadcasted Funding Transaction has bee created
  - both parties sign and exchange an initial Commitment Transaction
  - Commitment Transaction spends from teh 2-of-2 output of the Funding
    Transaction
    - only the Funding Transaction is broadcasted on the blockchain
- when the Funding Transaction has entered into the blockchain
  - the output is a 2-of-2 multisignature transaction that requires the
    agreement of both parties to spend from
- commitment Transactions are used to express the present balance
- if only 1 2-of-2 signed Commitment Transaction is exchanged between both
  parties
  - then both parties will be sure that they are able to get their coins back
    after the Funding Transaction enters the blockchain
  - both parties do not broadcast the Commitment Transactions onto the
    blockchain until they want to close out the current balance in the channel
    - this is done by broadcasting the present Commitment Transaction
- Commitment Transactions pay out the respective current balances to each party
- a naive (broken) implementation would construct an unbroadcast transaction
  - there would be a 2-of-2 spend from a single transaction that would have 2
    outputs which would return all current balances to both channel
    counterparties
    - this would return all funds to the original party when the initial
      Commitment Transaction is created
- Example of a naive broken funding transaction:
  - the Funding Transaction F is broadcasted on the blockchain after all other
    transactions are signed
  - all other transactions spending from the Funding Transaction are not yet
    broadcast
    - this allows the counterparties to update their balance

```None
                    Funding Tx (F)
                         |
                         |
                  Commitment Transaction
                  Outputs:
                  0. Alice 0.5 BTC
                  1. Bob 0.5 BTC
                  No LockTime
                         |
           -------------------------------
       Output 0                        Output 1
          |                               |
    Alice can redeem               Bob can redeem
    0.05 BTC from the              0.05 BTC from the
    Commitment Transaction         Commitment Transaction

```

- Commitment Transactions are signed 1st and the keys are exchanged
  - allows either party to to be able to broadcast the Commitment Transaction at
    any time
    - contingent upon the Funding Transaction entering into the blockchain
    - at this point the Funding Transaction signatures can safely be exchanged
      - either party is able to redeem their funds by broadcasting the
        Commitment Transaction
  - this construction breaks when 1 party attempts to update the present balance
  - in order to update the balance - they must update their Commitment
    Transaction output values
    - this is because the Funding Transaction has already entered into the
      blockchain and cannot be changed
- when both parties agree to a new Commitment Transaction and exchange
  signatures for the new Commitment Transaction:
  - either Commitment Transaction can be broadcast
- the output can only be redeemed once
  - only 1 of the transactions will be valid

#### Commitment Transactions: Ascribing Blame

- any Commitment Transaction can be broadcast on the blockchain
  - only one broadcast can be successful
  - necessary to prevent old Commitment Transactions from being broadcast
- not possible to revoke many transactions in Bitcoin
  - it is necessary to construct the channel similar to a Fidelity Bond
    - both parties make commitments - violations of these commitments are
      enforced by penalties
    - if 1 party violates their agreement - then they will lose all the coins
      in the channel
  - contract terms:
    - both parties commit to broadcasting only the most recent transaction
    - any broadcast of older transactions will cause a violation of contract
      - if a violation occurs - all funds are given to the other party not in
        violation
  - this contract can only be enforced if one is able to ascribe blame for
    broadcasting an old transaction
    - the party who broadcasted an older transaction must be able to be
      uniquely identified
      - this is accomplished when each counterparty has a uniquely identifiable
        Commitment Transaction
      - both parties must sign the inputs to the Commitment Transaction which
        the other party is responsible for broadcasting
      - each party holds the signed version of the Commitment Transaction from
        the other party - a party may only broadcast their own version of the
        Commitment Transaction
- in the Lightning Network all Commitment Transactions (spends) from the Funding
  Transaction output have 2 half-signed transactions
- Example:

```None
                        Funding Tx (F)
                            |
         -----------------------------------
        |                                   |
    Commitment 1a                       Commitment 1b
    Only Alice can broadcast            Only Bob can broadcast
    Outputs:                            Outputs:
    0. Alice 0.5 BTC                    0. Alice 0.5 BTC
    1. Bob 0.5 BTC                      1. Bob 0.5 BTC
    No LockTime                         No LockTime
         |                                   |
    -----------------                     ----------------------
   |                 |                    |                     |
Alice can redeem    Bob can Redeem     Alice can redeem      Bob can Redeem
0.5 BTC from        0.5 BTC from       0.5 BTC from          0.5 BTC from
Commitment          Commitment         Commitment            Commitment
Transaction         Transaction        Transaction           Transaction
Only Alice          Only Bob           Only Alice            Only Bob
can broadcast       can broadcast      can broadcast         can broadcast
```

- this only allows for allocating blame
- not possible to enforce the contract on the Bitcoin blockchain

### Creating a Channel with Contract Revocation

- in order to enforce the terms of the contract:
  - construct a Commitment Transaction along with its spends where a party is
    able to revoke a transaction
  - revocation is achievable by using data from when the transaction enters a
    blockchain and uses the maturity of the transaction to determine validation
    paths

### Sequence Number Maturity