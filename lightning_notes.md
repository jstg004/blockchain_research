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
    -----------------                      ---------------------
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

- Mark Freidenbach has proposed that Sequence Numbers can be enforceable by
  relative block maturity of the parent transaction via a soft-fork
  - this would allow the ability to ensure some form of block confirmation
    time lock on the spending script
  - additional opcode: OP_CHECKSEQUENCEVERIFY (OP_RELATIVECHECKLOCKTIMEVERIFY)
    - permits further abilities like stop-gap solutions before a more
      permanent solution for resolving transaction malleability

#### Enforcing transaction versions off-chain by time commitments

- a Revocable Transaction spends from a unique output where the transaction has
  a unique type of output script
  - this parent's output has 2 redemption paths
    - the 1st can be redeemed immediately
    - the 2nd can only be redeemed if the child has a minimum number of
      confirmations between transactions
      - this is achieved by making the sequence number of the child transaction
        require a minimum number of confirmations from the parent
      - this new sequence number behavior will only permit a spend from this
        output to be valid if the number of blocks between the output and the
        redeeming transaction is above a specified block height
      - a transaction can be revoked with this sequence number behavior by
        creating a restriction with some defined number of blocks defined in
        the sequence number
      - this results in the spend being only valid after the parent has
        entered into the blockchain for some defined number of blocks
      - the parent transaction with this output becomes bonded deposit
        - attests that there is no revocation
      - a time period exists which anyone on the blockchain can refute this
        attestation by broadcasting a spend immediately after the transaction is
        broadcast
- Example: if one wishes to permit revocable transactions with a
  1000-confirmation delay
  - the output transaction construction would remain a 2-of2 multisig:
    - ```2 <Alice1> <Bob1> 2 OP_CHECKMULTISIG```
  - the child spending transaction would contain a nSequence value of 1000
  - this transaction required the signature of both counterparties to be valid
    - both parties include the nSequence number of 1000 as a part of the
      signature
    - both parties may agree to create another transaction which supersedes that
      transaction without any nSequence number
- the pre-signed child transaction can be redeemed after the parent transaction
  has entered into the blockchain with 1000 confirmations due to the child's
  nSequence number on the input spending the parent
- in order to revoke this signed child transaction - both parties agree to
  create another child transaction with the default field of the nSequence
  number of MAX_INT (has special behavior permitting spending at any time)
- the new signed spend supersedes the revocable spend
  - as long as the new signal spend enters into the blockchain within 1000
    confirmations of the parent transaction entering into the blockchain
- anyone can create a transaction without broadcasting it
  - then later create incentives to not ever broadcast the transaction in the
    future via penalties
  - this permits participants on the Bitcoin network to defer many transactions
    from ever hitting the blockchain

##### Revocable Sequence Maturity Contract (RSMC)

- 2 paths are created with very specific contract terms:
  1. all parties pay into a contract with an output enforcing this contract
  2. both parties may agree to send funds to some contract with some waiting period
     - this is the revocable output balance
  3. 1 or both parties may elect to not broadcast (enforce) the payouts until
     some future date
     - either party may redeem the funds after the waiting period at any time
  4. if neither part has broadcasted this transaction (redeemed the funds)
     - they may revoke the above payouts if and only if both parties agree to do
       so by placing in a new payout term in a superseding transaction payout
     - the new transaction payout can be immediately redeemed after the contract
       is disclosed to the world (broadcasted on the blockchain)
  5. in the event that the contract is disclosed and the new payout structure is
     not redeemed
     - the prior revoked payout terms may be redeemed by either party
     - it is the responsibility of either party to enforce the new terms

#### Timestop

- to mitigate a flood of transactions by a malicious attacker requires a
  credible threat that the attack will fail
- timestop proposed by Greg Maxwell:
> The clock can stop when blocks are full; turning the security risk into more
> hold-up delay in the event of a DoS attack.
- a miner can specify whether the current fee paid mempool is presently being
  flooded with transactions
  - miner can enter a '1' value into the last bit in the version number of the
    block header
  - if the last bit in the block header contains a '1'
    - then that block will not count towards the relative height maturity for
      the nSequence value and the block is designated as a congested block
    - the uncongested block height is always lower than the normal block height
    - this block height is used for the nSequence value that only counts block
      maturity confirmations
- a miner can elect to define the block as a congested block or not
  - default code could automatically set the congested block flag as a '1' if
    the mempool is above some size and the average fee for that set size is
    above some value
  - a miner has full discretion to change the rules on what automatically sets as
    a congested block
    - can also select to permanently set the congestion flag to be permanently
      on or off
- if a parent transaction output is spent by a child with nSequence value of 10
  - one must wait 10 confirmations before the transaction ebcomes valid
- if the timestop flag has been set - the counting of confirmations stops
- if 6 confirmations have elapsed - 4 more are necessary for the transaction to
  be held - and timestop block has been set on the 7th block
  - that 7th block does not count towards the nSequence requirement of 10
    confirmations
  - the child is still at 6 blocks for the relative confirmation value
    - stored as an auxiliary timestop block height which is used only for
      tracking the timestop value
  - when the timestop bit is set - all transactions using an nSequence value
    will stop counting until the timestop bit has been unset
  - allows for sufficient time and block-space for transactions at the current
    auxiliary timestop block height to enter into the blockchain
  - this can prevent systemic attackers from successfully attacking the system
  - a flag in the block is required to designate whether it is a timestop block
- for a lightweight client that is fully SPV compatible the block header needs
  to be within the 80-byte block header
  - this flag could be put into either of these sections of the block header:
    1. in the block time
       - may not be safe - the last bits are being used as an entropy source
         for some ASIC miners
       - a bit may need to be consumed for timestop flags
       - the flag could be hardcoded into the timestop activation as a hard
         consensus rule - via block size
         - this may be less flexible
       - if sane defaults are set for timestop rules - they can be changed
         without consensus soft-forks
    2. in the block version
       - the contextual information must match the Chain ID used in some
         merge-mined coins

#### Revocable Commitment Transactions

- the combination of having the ability to ascribe blame and revoke a
  transaction allows for the ability to determine when a party is not abiding
  by the terms of the contract
  - penalties can be enforced without trusting the counter party
- Example:

```None
                    Funding Tx(f)
                         |
         ------------------------------------------------
        |                                                |
Commitment Tx 1a (C1a)                       Commitment Tx 1b (C1b)
Only Alice can broadcast                     Only Bob can broadcast
Outputs:                                     Outputs:
0. RSMC Alice&Bob 0.5BTC                     0. Alice 0.5BTC
1. Bob 0.5BTC                                1. RSMC Alice&Bob 0.5BTC
No LockTime                                  No LockTime
  |                                              |
  Output 0                                       Output 1
  |__ Revocable Delivery 1a(RD1a)                |__ Revocable Delivery 1b(RD1b)
  |   Only Alice can broadcast 1000              |   Only Bob can broadcast 1000
  |   confirmations from C1a's                   |   Confirmations from C1b's
  |   mined block                                |   mined block
  |   Output: Alice 0.5                          |   Output: Bob 0.5
  |   1000-block Relative                        |   1000-block Relative
  |   Confirmations Lock                         |   Confirmations Lock
  |                                              |
  Output 1                                       Output 0
  |__ Delivery 1a (D1a)                          |__ Delivery 1b (D1b)
      Bob can spend from this output                 Alice can spend from this
      immediately when C1a is broadcast              output immediately when
      Output: Bob 0.5                                C1b is broadcast
      No LockTime                                    Output: Alice 0.5
                                                     No LockTime
```

- Funding Transaction F is broadcast on the blockchain after all other
  transactions are signed
- Only the Funding Transaction is broadcast on the blockchain at this time
- creating a new Commitment Transaction allows for invalidation of all old
  Commitment Transactions when the new balance is updated with a new
  Commitment Transaction
- invalidation of old transactions occurs when an output is converted to a
  Revocable Sequence Maturity Contract (RSMC)
- to invalidate a transaction:
  - a superseding transaction is signed and exchanged by both parties
    - this transaction gives all funds to the counterparty is an older
      transaction is incorrectly broadcast
    - the incorrect broadcast is identified by creating 2 different Commitment
      Transactions with the same final balance outputs
      - the payment to oneself is encumbered by an RSMC
- there are 2 Commitment Transactions from a single Funding Transaction 2-of-2
  outputs
  - only 1 of the 2 Commitment Transactions can enter into the blockchain
  - each party within a channel has 1 version of the contract
  - when a party broadcasts a Commitment Transaction pair - they are requesting
    the channel to be closed out
    - the 1st 2 outputs for the Commitment Transaction include the Delivery
      Transaction (the payout) of the present unallocated balance to the channel
      counterparties
    - the Delivery Transaction is immediately redeemable
      - it is not encumbered if the Commitment Transaction is broadcast
- each party's attests that they are broadcasting the most recent Commitment
  Transaction which they own
  - the balance paid to the counterparty is assumed to be true
  - a party has no direct benefit by paying some funds to the counterparty as a
   penalty
- the balance paid to the party who broadcasted the Commitment Transaction
  is unverified
  - therefore there is a penalty if they do not broadcast their most recent
    version
  - the RSMC prevents their funds from being claimed until a set number of
    confirmations is reached after the Commitment Transaction has been included
    in a block
  - if the most recent Commitment Transaction is the one that is broadcasted
    - there is no revocation transaction superseding the revocable transaction
    - then funds are able to be received after the set amount of confirmations
- both parties are able to revoke the Commitment Transaction in the future

#### Redeeming Funds from the Channel: Cooperative Counterparties

- either party may redeem the funds from the channel
- the party that broadcasts the Commitment Transaction must wait for the
  predefined number of confirmations described in the RSMC
  - the counter party that did not broadcast the Commitment Transaction is
    able to redeem the funds immediately

#### Creating a new Commitment Transaction and Revoking Prior Commitments

- either party may close out the most recent Commitment Transaction at any time
  - they may also create a new Commitment Transaction and invalidate the old one
- when the balance is updated a new pair of Commitment Transactions is
  generated only if both parties agree
- 4 possible transactions can exist
  - a pair with the old commitments
  - another pair with the new commitments
- each party inside the channel can only broadcast half of the total commitments
  (2 each)
- when a new pair of Commitment Transactions is agreed upon
  - both parties will sign and exchange signatures for the new Commitment
    Transactions
  - the old is then invalidated
  - the invalidation occurs when both parties sign a Breach Remedy Transaction
    - this supersedes the Revocable Delivery Transaction
  - each party hands a half signed revocations to the other from their
    respective Revocable Delivery
    - this is a spend from the Commitment Transaction
- the Breach Remedy Transaction will send all coins to the counterparty within
  the current balance of the channel
  - by constructing a Breach Remedy Transaction for the counterparty
    - one has attested that one will not be broadcasting any prior commitments
    - this is acceptable to the counterparty on the basis that all the money
      in the channel will be transferred to the counterparty if the agreement
      is violated
- a party should periodically monitor the blockchain to see if one's
  counterparty has broadcasted an invalidated Commitment Transaction
  - a 3rd party can be used for this monitoring service
    - the Breach Remedy Transaction must be delegated to this 3rd party
    - the 3rd party is incentivized by receiving a fee from the output
    - this 3rd party has no power to force close the channel
      - they are only able to take action only if the counterparty acts
        maliciously

#### Process for Creating Revocable Commitment Transactions

- creating revocable Commitment Transactions requires proper construction of the
  channel from the beginning
  - only signing transactions which may be broadcast at any time in the future
  - ensures that one will not lose out due to uncooperative or malicious
    counterparties
  - the public key used for new commitments must be determined
    - using ```SIGHASH_NOINPUT``` requires using unique keys for each Commitment
      Transaction RSMC and HTLC output
      - ```P``` is used to designate pubkeys and ```K``` to designate the
        corresponding private key used to sign
- when the 1st Commitment Transaction is generated both parties agree to create
  a multisig output from a Funding Transaction with a single output
  - this output is a Pay to Script Hash transaction
    - requires both parties to agree to spend from the Funding Transaction
    - the Funding Transaction is not yet spendable
- the Delivery Transaction is either a P2PHK output or a P2SH transaction
  - a P2PHK output is a Bitcoin address beginning with 1
  - P2SH transaction is an address beginning with 3
- output addresses remain the same throughout the channel
  - funds are fully controlled by its designated recipient after the
    Commitment Transaction enters the blockchain
  - pubkeys may be changed for future Commitment Transactions
- both parties exchange pubkeys which they intend to use for the RSMC and HTLC
  for the Commitment Transaction
- each set of Commitment Transactions use their own public keys
  - these are not reused
- both parties know all future pubkeys by using ```BIP0032[17] HD Wallet```
  construction by exchanging Master Public Keys durring channel construction
- after both parties know the output values form the Commitment Transactions
  - both parties create the pair of Commitment Transactions
  - they do not exchange signatures for the Commitment Trnasactions
  - both parties sign the Revocable Delivery Transaction and exchange signatures
  - when both parties have the Revocable Delivery Transaction
    - they exchange signatures for the Commitment Transactions
    - at this point prior Commitment Transactions and the new one can be
      broadcast
- when both Breach Remedy signatures have been exchanged
  - the channel state is now at the current Commitment and the balances are
    committed
  - it is most effective to only disclose the private keys to the counterparty
    - one party can disclose the private keys used in their own Commitment
      Transaction

### Cooperativelty Closing Out a Channel

- both parties are able to send as many payments to their counterparty as they
  wish - as long as they have funds available in the channel
  - in the event of disagreements - the current state can be broadcast to the
    blockchain
- to close out a channel cooperatively both parties contact each other then
  spend from the Funding Transaction with an output of the most current
  Commitment Transaction directly with no script encumbering conditions
  - no further payment is allowed in the channel after this has occurred
- if both parties are cooperative - the balances in the current Commitment
  Transaction are spent from the Funding Transaction using an Exercise
  Settlement Transaction
  - even in the event of the most recent Commitment Transaction being broadcast
    instead - then the payout - less the fees is still the same
- closing out cooperatively reduces the number of transactions that occur on
  the blockchain
  - both parties are able to receive their funds immediately
- channels may remain in perpetuity until they decide to cooperatively close out
  the transaction (or when 1 party does not cooperate)

### Bidirectional Channel Implications and Summary

- by ensuring channels can update only with the consent of both parties:
  - it is possible to construct channels which perpetually exist int eh
    blockchain
- both parties can update the balance inside the channel with whatever output
  balances they wish which are equal or less than the total funds committed
  inside the Funding Transaction
  - balance can move bidirectionally
  - if 1 part acts maliciously - either party may immediately close out the
    channel - broadcasting the most current state to the blockchain
- the Fidelity Bond Construction (Revocable Delivery Transactions):
  a party who violates the terms of the channel will loose their funds to their
  counterparty
  - this occurs only if the proof of validation (Breach Remedy Transaction)
    is entered into the blockchain in a timely manner
  - the channel may remain open indefinitely so long as both parties
    continuously cooperate
- this is all possible because adjudication occurs programmatically over the
  blockchain as part of the Bitcoin consensus
  - neither part need to trust the other
  - one's channel counterparty does not posses full custody or control of
    the funds

## Hashed Timelock Contract (HTLC)

- a bidriectional payment channel only permits secure transfer inside a channel
- HTLC is required in order to construct secure transfers using a network of
  channels across multiple hops to the final destination
- HTLC allows for global state across multiple nodes via hashes
  - the global state is ensured by time commitments and time-based unencumbering
    of resources via disclosure of preimages
  - transaction locking occurs globally via commitments
    - at any point in time a single participant is responsible for disclosing to
      the next participant
    - does not require custodial trust in one's channel counterparty
- HTLC must be able to create certain transactions which are only valid after
  a certain date
  - this is done using ```nLockTime``` and an information disclosure to the
    channel counterparty
  - this data must be revocable - the HTLC must be able to be undone
- HTLC is also a channel contract with one's counterparty
  - enforced by the blockchain
- Example:
  - in a channel the counterparties agree to the following terms for a HTLC:

    ```None
        1. If Bob can produce to Alice an unknown 20-byte random input data R
           a known hash H, within 3 days, then Alice will settle the contract
           by paying Bob 0.1 BTC.
        2. If 3 days have elapsed, then the above clause is null and void and
           the clearing process is invalidated, both parties must not attempt
           to settle and claim payment after 3 days.
        3. Either party may (and should) pay out according to the terms of this
           contract in any method of the participants choosing and close out
           this contract early so long as both participants in this contract
           agree.
        4. Violation of the above terms will incur a maximum penalty of the
           funds locked up in this contract, to be paid to the non-violating
           counterparty as a fidelity bond.
    ```

- if one desires to construct a payment which is contingent upon knowledge
  of ```R``` by the recipient within a certain timeframe
  - after this timeframe - the funds are refunded back to the sender
- the contract terms are programatically enforced on the Bitcoin blockchain
  - they do not require trust in the counterparty in order to adhere to the
    contract terms
  - violations are penalized via unilaterally enforced fidelity bonds
    - these bonds are constructed using penalty transactions spending from
      commitment states
- Example:
    - HTLC is an additional output in a Commitment Transaction with a unique
      output script:

    ```None
        OP_IF
            OP_HASH160 <HASH160(R)> OP_EQUALVERIFY
            2 <Alice2> <Bob2> OP_CHECKMULTISIG
        OP_ELSE
            2 <Alice1> <Bob1> OP_CHECKMULTISIG
        OP_ENDIF
    ```
- the above script has 2 possible paths spending from a single HTLC output:
  1. the 1st path is defined in the ```OP_IF```
     - funds are sent to Bob if Bob can produce ```R```
  2. the 2nd path is redeemed using a 3-day timelocked refund to Alice
     - the 3-day timelock is enforced using ```nLockTime``` from the spending
       transaction

### Non-revocable HTLC Construction

- using the above example:
  - if ```R``` is produced within 3 days, then Bob can redeem the funds by
    broadcasting the Delivery transaction
  - a requirement for the Delivery transaction to be valid requires ```R``` to
    be included with the transaction
  - if ```R``` is not included  - then the Delivery transaction is invalid
  - if 3 days have elapsed - the funds can be sent back to Alice by broadcasting
    transaction Timeout
  - when 3 days have elapsed and ```R``` has been disclosed - either transaction
    may be valid
  - both parties are individually responsible for ensure that they can get their
    transaction into the blockchain in order to ensure the balances are correct
    - in order for Bob to receive funds - he must either broadcast the delivery
      transaction on the Bitcoin blockchain or settle with Alice and
      cancelling the HTLC
    - in order for Alice to receive funds - she must broadcast the Timeout
      in 3 days or cancel the HTLC
  - when an old Commitment Transaction gets broadcast - either party may attempt
    to steal funds
    - if ```R``` gets disclosed 1 year later and an incorrect Commitment
      Transaction gets broadcast - both paths are valid are redeemable by either
      party
      - the contract is not yet enforceable on the blockchain
    - it is necessary to close out the HTLC in order for Alice to get her refund
      - Alice must terminate the contract and receive her refund
    - if Bob discovers ```R``` after 3 days - he may be able to steal the funds
      which are supposed to be going to Alice
  - Uncooperative parties make it impossible to terminate an HTLC without
    broadcasting it to the Bitcoin blockchain
    - the uncooperative party is unwilling to create a new Commitment
      Transaction

### Off-chain Revocable HTLC

- in order to terminate this contract off-chain without a broadcast to the
  Bitcoin blockchain requires embedding RSMCs in the output
  - this is a similar construction to the bidirectional channel
- Example:
  - Alice and Bob wish to update their balance in the channel at Commitment 1
    with a balance of 0.5 BTC to Alice and 0.5 BTC to Bob
  - Alice wishes to send 0.1 to Bob contingent upon knowledge of ```R``` within
    3 days
    - after 3 days Alice wants her money back if Bob does not produce ```R```
  - the new Commitment Transaction will have a full refund of the current
    balance to Alice and Bob (Outputs 0 and 1)
    - output 2 being the HTLC - describes the funds in transit
  - 0.1 BTC will be encumbered in an HTLC
    - Alice's balance is reduced to 0.4 BTC and Bob's remains the same - 0.5 BTC
  - the new Commitment Transaction will have an HTLC output with 2 possible
    spends
    - each spend is different depending on each counterparty's version of the
      Commitment Transaction
  - when 1 party broadcasts their Commitment - payments to the counterparty will
    be assumed to be valid and not invalidated
    - this can occur beacause when a party broadcasts a Commitment Transaction
      - that party attests that it is the most recent Commitment Transaction
    - if it is the most recent - then that party attests that the HTLC exists
      and was not invalidated before
      - potential payments to the counterparty should be valid

#### HTLC when the Sender Broadcasts the Commitment Transaction

- for the sender - the Delivery transaction is sent as an HTLC Execution
  Delivery transaction
  - this is not encumbered in an RSMC
- this assumes that the HTLC has never been terminated off-chain

#### HTLC when the Receiver Broadcasts the Commitment Transaction

- for the potential receiver - the Timeout of the receipt is refunded as an
  HTLC Timeout Delivery transaction
  - this transaction directly refunds the funds to the original sender
  - it is not encumbered in an RSMC
  - this assumes that this HTLC has never been terminated off-chain

### HTLC Off-chain Termination

- after an HTLC is constructed - in order to terminate the HTLC off-chain
  requires both parties to agree on the state of the channel
- if the recipient can prove knowledge of ```R``` to the counterparty
  - the recipient is proving that they are able to immediately close out the
    channel on the Bitcoin blockchain and receive the funds
    - if both parties wish to keep the channel open - they should terminate the
      HTLC off-chain and create a new Commitment Transaction reflecting the new
      balance
- if the recipient is not able to prove knowledge of ```R``` by
  disclosing ```R``` - both parties should agree to terminate the HTLC and
  create a new Commitment Transaction with the balance in the HTLC refunded to
  the sender
- if counterparties cannot come to an agreement or become otherwise unresponsive
  - they should close out the channel by broadcasting the necessary channel
    transaction on the Bitcoin blockchain
  - if they are cooperative - they can do so by:
    - 1st generating a new Commitment Transaction with the new balances
    - then invalidating the prior Commitment by exchanging Breach Remedy
      transactions
  - if they are terminating a particular HTLC they should also exchange some of
    their own private keys used in the HTLC transactions
- both parties are able to prove the current state to each other
  - they can come to agreement on the current balance inside the channel
  - they may broadcast the current state on the blockchain
  - they are able to come to agreement on netting out and terminating the HTLC
    with a new Commitment Transaction

### HTLC Formation and Closing Order

- creating a new HTLC is a similar process to creating a new Commitment
  Transaction
  - the difference is that the signatures for the HTLC are exchanged before the
    new Commitment Transaction's signatures
- when the HTLC has been closed - the funds are updated so that the present
  balance in the channel is what would occur if the HTLC contract is completed
  and broadcast on the blockchain
  - this is instead done in an off-chain novation by both parties who update
    their payments inside the channel
  - it is necessary for both parties to complete off-chain novation within their
    designated time window
- if a counterparty is unwilling to novate or stalls - then a party must
  broadcast the current channel state (including HTLC transactions) onto the
  Bitcoin blockchain

## Key Storage

- keys are generated using BIP 0032 Hierarchical Deterministic Wallets
- keys are pre-generated by both parties
- keys are generated deep within a merkle tree
- Example:
  - Alice pre-generates 1 million keys
    - each key is a child of the previous key
  - Alice allocates which keys are used according to a deterministic manner
  - if Alice starts with the child deepest in the tree to generate many sub-keys
    for day 1
    - this key is used as a master key for all keys generated on day 1
  - Alice gives Bob the address she wishes to use for the next transaction
    - she discloses the private key to Bob when it becomes invalidated
  - when Alice discloses to Bob all private keys derived from the day 1 master
    key and does not wish to continue using that master key
    - Alice can disclose the day 1 master key to Bob
    - Bob does not need to store all the keys derived from the day 1 master key
    - Bob does the same for Alice and gives her his day 1 key
  - when all day 2 private keys have been exchanged by for example day 5
    - Alice then discloses her day 2 key
    - Bob is able to generate the day 1 key from the day 2 key
      - this is possible because the day 1 key is a child of the day 2 key
- if a counterparty broadcasts the incorrect Commitment Transaction
  - the private key to use in a transaction to recover funds can be brute
    forced
  - or the sequence ID number can be used when creating the transaction to
    identify which sets of keys are used (as long as both parties agree)
- participants in a channel can invalidate prior output states (transactions)
  - by disclosing private keys which are pre-arranged in a merkle tree
    - it is possible to invalidate millions of old transactions with only a few
      kB of data per channel
  - core channels in the Lightning Network can conduct billions of transactions
    without a need for significant storage costs

## Blockchain Transaction Fees for Bidirectional Channels

- it is possible for each participant to generate different versions of
  transactions to ascribe blame to the party who broadcasted the transmission
  on the blockchain
- knowledge of the broadcaster allows a 3rd party service the ability to hold
  fees in a 2-of-3 multisig escrow
- if a party chooses to broadcast the transaction chain instead of agreeing
  to do a Funding Close or replacement with a new Commitment Transaction
  - the party needs to communicate with the 3rd party and broadcast thr chain
    to the blockchain
  - if the counterparty refuses the notice from the 3rd party to cooperate
    - then the penalty is rewarded to the non-cooperative party
- trust of the entire network is not required
- fees are typically derived from the time-value of locking up funds for a
  particular route
  - fees should be significantly lower than on-chain transaction fees
- many transactions on a Lightning Network can be settled into 1 single
  blockchain transaction
- on a robust and interconnected network - the fees should asymptotically
  approach negligibility for many types of transactions
- low fees and fast transactions allow for scalable micropayments in a high
  frequency system
  - IoT applications or per-unit micro billing could benefit from this

### Pay to Contract

- it is possible to construct a cryptographically provable Delivery Verses
  Payment contract or oay-to-contract as a proof of payment
  - the proof can be established as knowledge of the input ```R``` from
    ```hash(R)``` as payment of a vertain value
- an embedded clause into the contract between the buyer and seller stating:
  - ```R``` is proof of funds sent
- the recipient of the funds has no incentive to disclose ```R``` unless they
  have certainty that they will receive payment
- when the funds are pulled from teh buyer by their counterparty in their
  micropayment channel - ```R``` is disclosed as part that pull of funds

## The Bitcoin Lightning Network

- a micropayment channel with contracts encumbered by hashlocks and timelocks
- makes it possible to clear transactions over a multi-hop payment network
  using a series of decrementing timelocks without additional central
  clearinghouses
- Bitcoin enables programmatic money
  - possible to create actions without contacting the central clearinghouses
    which traditional banking requires
- transactions can execute off-chain with no 3rd party which collects all funds
  before disbursing
  - only transactions with uncooperative channel counterparts become
    automatically adjudicated on the blockchain
- the chain delegation process allows for obligations to deliver funds to an
  end-recipient
  - each participant along the path assumes the obligation to deliver to a
    particular recipient
  - each participant passes on this obligation to the next participant in the
    path
  - the obligations of each subsequent participant along the path has a shorter
    time to completion compared to the prior participant
    - these obligations are defined by HTLCs
- Bitcoin Transaction Scripting enables systems without trusted custodial
  clearinghouses or escrow
  - makes smart contracts possible

### Decrementing Timelocks

- Example: Payment over the Lightning Network using HTLCs
  - Alice wishes to send 0.001 BTC to Dave
  - Alice locates a route through Bob and Carol
  - the transfer path is Alice to Bob to Carol to Dave

    ```None
         Step 1:         Step 2:           Step 3:
          3 day           2 day             1 day
          lock            lock              lock
    Alice ---------> Bob ---------> Carol ---------> Dave
    ```

- when Alice sends payment to Dave through Bob and Carol - Alice requests
  from Dave ```hash(R)``` to use for this payment
  - Alice then counts the amount of hops until the recipient
    - uses this count as the HTLC expiry
  - in this example the HTLC expiry is set at 3 days
  - Bob then creates an HTLC with Carol with an expiry of 2 days
  - Carol then creates an HTLC with Dave with an expiry  of 1 day
    - Dave is then free to disclose ```R``` to Carol
    - both parties will likely agree to immediate settlement via notation with
      a replacement Commitment Transaction
      - this occurs step by step back to Alice
- all this is conducted off-chain and nothing is broadcast to the blockchain
  when all parties are coorperative

- Example: Settlement of HTLC - Alice's funds get sent to Dave

    ```None
         Step 6:        Step 5:          Step 4:
          Redeem &       Redeem &         Redeem &
          replace        replace          replace
          contract       contract         contract
    Alice ---------> Bob ---------> Carol ---------> Dave
    ```

- decrementing timelocks are used so that all parties along the path know
  the disclosure of ```R``` will allow the disclosing party to pull funds
- if Dave does not produce ```R``` within 1 day to Carol
  - then Carol will be able to close out the HTLC
- if Dave broadcasts ```R``` after 1 day
  - then he will not be able to pull funds from Carol
- Carol's responsibility to Bob occurs on day 2
  - Carol is not responsible for payment to Dave without the ability to pull
    funds from Bob
    - Carol must update her transaction with Dave via transmission to the
      blockchain or via novation
- if ```R``` is disclosed to the participants halfway through expiry along
  the path
  - it is then possible for some parties along the path to be enriched
  - sender is able to know ```R```
    - the payment will have been fulfilled according to Pay to Contract
      even if the receiver did not receive the funds
  - the receiver must never disclose ```R``` before receiving an HTLC from
    their channel counterparty
    - cannot guarantee receipt of payment from a channel counterparty upon
      disclosure of the preimage
- if a party disconnects - the counterparty will be responsible for broadcasting
  the current Commitment Transaction state in teh channel to the blockchain
  - the failed non-responsive channel state gets closed out on the blockchain
  - all other channels shold continue to update their Commitment Transactions
    via novation inside the channel
  - counterparty risk for transaction fees are only exposed to direct channel
    counterparties
  - if a node along the path becomes unresponsive - the participants not
    directly connected to that node suffer only decreased timevalue of their
    funds by not conducting early settlement before the HTLC close

- Example: Only non-responsive channels get broadcast on blockchain
  - all others settled off-chain via novation

    ```None
         Step 6:                                   Step 4:
          Redeem &                                  Redeem &
          replace                                   replace
          contract                                  contract
    Alice ---------> Bob ---> Blockchain ---> Carol ---------> Dave
                           Step 5:
                            Broadcast to
                            blockchain and
                            close channel
                            between Bob
                            & Carol
    ```

### Payment Amount
