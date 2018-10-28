# notes from _Enabling Blockchain Innovations with Pegged Sidechains_

- by Adam Back, Matt Corallo, Luke Dashjr, Mark Friedenbach, Gregory Maxwell,
  Andrew Miller, Andrew Poelstra, Jorge Timón, and Pieter Wuille
- October 2014

## Introduction

- Bitcoin's blockheaders can be regarded as an example of a Dynamic Membership
  Multiparty Signature (DMMS)
  - a new type of group signature
  - a digital signature formed by a set of signers which has no fixed size
  - Bitcoin's blockheaders are DMMS
    - Proof-of-Work (PoW) has the property that anyone can contribute without
      enrolling
    - contribution is weighed by computational power
      - allows for anonymous membership without risk of Sybil attack
        - Sybil attack is when 1 party joins many times - has a disproportionate
          input into the signature
  - DMMS could be a solution to the Byzantine Generals Problem
  - Bitcoin's DMMS is cumulative - blocks are chained together
    - the 1st block in a chain or a chain fragment of a blockheader is a DMMS
    - computational strength of a chain = sum of strengths of the DMMS
    - the strength of Bitcoin's cumulative DMMS is directly proportional to the
      total computational power contributed by all miners

### Trade-offs between scalability and decentralization

- a larger block size allows the network to support a higher transaction rate
  - the cost of placing more work on validators
    - this is a centralization risk

### Trade-offs between security and cost

- Bitcoin stores every transaction in its history with the same level of
  irreversibility
  - this is expensive to maintain
  - may not be appropriate for low value or low risk transactions

### Trade-offs for blockchain features

- Bitcoin's script could be made  more powerful in order to enable succinct
  and useful contracts
  - could be made less powerful to assist in auditability

### Risk of monoculture

- Bitcoin is composed of many cryptographic components
  - failure of any of these components could cause a total loss of value
  - would be prudent not to secure every Bitcoin with the same set of algorithms

### New technologies

- new technologies could enable new features not imagined when Bitcoin was
  developed
  - pivacy and censorship-resistance could be improved by use of cryptographic
    accumulators, ring signatures, or Chaumian blinding

### No safe upgrade path for Bitcoin

- all participants must act in concert for any change to be effective
- functionality must be broadly acceptable to gain adoption
  - limits participants personal freedom and autonomy over their own coins
  - small groups are unable to implement features
    - they lack consensus

### Alternate blockchains (altchains)

#### Infrastructure fragmentation

- each altchain uses its own technology stack
  - effort is frequently duplicated and lost
  - implementations of altchains may fail to clear the high barrier of
    security-specific domain knowledge in Bitcoin
    - security problems are often duplicated across altchains while security
      fixes are not
- Example:
  - an internet where every website uses its own TCP implementation
    - advertizing its customized checksum and packet-splicing algorithms
      to end users
      - this is not a viable environment

#### Native cryptocurrency

- floating prices
- currency accessed by markets
  - exposes users to high risk and volatility
- required to independently solve problems
- crowded market discourages technical innovation
- encourages market games

### Pegged sidechains

- assets are moved between sidechains and able to be moved back by whomever
  their current holder is
  - no one else (including previous holders) can move assets
- assets should be moved without couterparty risk
  - no ability for a dishonest party to prevent the transfer from occurring
- transfers should be atomic
  - occur entirely or not at all
  - there should not be failure modes that result in loss or allow fraudulent
    creation of assets
- sidechains should be firewalled
  - a bug in q sidechain enabling creation or theft of assets in that chain
    should not result in the creation or theft of assets on any other chain
- blockchain reorganizations should be handled "cleanly"
  - any disruption should be localized to the sidechain on which it occurs
  - sidechains should be fully independent
    - users provide any necessary data from other chains
  - validators of a sidechain should only be required to track another chain
    if that is an explicit consensus rule of the sidechain it self
- users should not be required to track sidechains they are not actively using

### Proposed solution

- transfer assets by providing proofs of possession in the transferring
  transactions themselves
  - avoids the need to track the sending chain

#### Moving assets from one blockchain to another

1. create a transaction on the 1st blockchain
   - locking the asset
2. create a transaction on the 2nd blockchain
   - inputs contain a cryptographic proof that the asset lock was
     completed correctly
   - inputs are tagged with an asset type
     - such as the genesis hash of its originating blockchain
- 1st blockchain is called the parent chain
- 2nd blockchain is called the sidechain
- possible to transfer an asset from the parent chain to a sidechain
  - can then be transferred onward to another sidechain
    - can be transferred back and forth between sidechains
  - can always be transferred back to the parent chain from any sidechain
- sidechains cannot cause unauthorized creation of coins
  - this is because sidechains transfer existing assets from the parent chain
    - new assets are NOT created
  - relies on the parent chain to maintain the security and scarcity of
    its assets
- sidechains can implement new transaction designs, trust models,
  economic models, assets issuance semantics, or cryptographic features
  - can differ from the parent chain

## Design rationale

### Trustlessness

- the property of not relying on trusting external parties for correct
  operation of the system
- enables all parties to verify the accuracy of information on their own
- Example:
  - in cryptographic signature systems - trustlessness is an implicit
    requirement
    - signatures systems where an attacker can forge signatures are
      considered broken

### Design goal of pegged sidechains

- minimise additional trust over Bitcoin's model
- securing transfers of coins between sidechains
  - receiving chain must see that the coins on the sending chain were
    correctly locked
    - using DMMS to achieve this

#### Avoid the introduction of single points of failure

- trusting individual signers
  - expect them to behave honestly
  - never be compromised
  - never leak secret key material
  - never coerced
  - never stop participating int he network
- digital assets are long-lived
  - any trust requirements must be long lived as well
- community mistrust
  - need to eliminate single points of failure to gain trust

## Two-way peg

### Definitions

- coin/asset: digital property whose controller can be cryptographically
  ascertained
- block: a collection of transactions describing changes in asset control
- blockchain: well-ordered collection of blocks - users must come to consensus
  - determines the history of asset control
  - provides a computationally unforgeable time ordering for transactions
- reorganization (reorg): occurs locally in clients when a previously accepted
  chain is overtaken by a competitor chain with more PoW
  - causes any blocks on the losing side of the fork to be removed from
    consensus history
- sidechain: a blockchain that validates data from other blockchains parent
  chain
- two-way peg: mechanism by which coins are transferred between sidechains and
  back at a fixed or otherwise deterministic exchange rate
- pegged sidechain: a sidechain whose assets can be imported from and returned
  to other chains
  - supports two-way pegged assets
- Simplified Payment Verification (SPV) proof: a DMMS that an action occurred
  on a Bitcoin-like PoW blockchain
  - SPV proof is composed of:
    1. a list of blockheaders demonstrating PoW
    2. a cryptographic proof that an output was created in one of the blocks
       in the list
  - SPV allows verifiers to check that some amount of work has been committed
    to the existence of an output
  - SPV proofs determine history
    - implicitly trusting that the longest blockchain is also the longest
      correct blockchain - by SPV clients in Bitcoin
  - only a dishonest collusion with greater than 50% of the hashpower can
    persistently fool an SPV client
    - unless the client is under a long-term Sybil attack
    - preventing it from seeing the actual longest chain
    - the honest hashpower will not contribute work to an invalid chain
  - anyone in possession of an SPV proof can determine the state
    of the chain without needing to reply to every block
    - this is accomplished by requiring each blockheader to commit to the
      blockchain's unspent output set

### Symmetric two-way peg

- to transfer parent chain coins into sidechain coins:
  - the parent chain coins are sent to a special output on the parent chain
    that can only be unlocked by an SPV proof of possession on the sidechain

#### Synchronize the sidechain to the parent chain

1. confirmation period of a transfer between sidechains
   - a duration for which a coin must be locked on the parent chain before
     it can transferred to the sidechain
   - allows for sufficient work to be created
     - making DoS attacks in the next waiting period difficult
   - after creating the special output on the parent chain:
     1. user waits out the confirmation period
     2. user creates a transaction on the sidechain referencing this output
        - provides SPV proof that the transaction was created and buried
          under sufficient work on the parent chain
     - confirmation period is a per-sidechain security parameter
       - trades cross-chain transfer speed for security
2. user must wait for the contest period
   - a duration in which a newly transferred coin may not be spent on the
     sidechain
   - a contest period prevents double spending by transferring previously
     locked coins during a reorganization
   - reorganization proof:
     - if during the delay a new proof is published
       - containing a chain with more aggregate work
         - not including the block in which the lock output was created
       - the conversion is retroactively invalidated
   - all users of the sidechain have an incentive to produce reorganization
     proofs if possible
   - if a bad proof is admitted - the value of all coins is diluted
- the coin locked on teh parent chain can be freely transferred withing the
  sidechain without further interaction with the parent chain
  - this coin retains its identity as a parent chain coin
  - can only be transferred back to the same chain that is came from
- to transfer coins from the sidechain back to the parent chain:
  1. send the coins on the sidechain to an SPV-locked output
  2. produce a sufficient SPV proof that the 1st step was completed
  3. use the proof to unlock a number of previously locked outputs with equal
     denomination on the parent chain

    ```None
         Parent Chain                                  Sidechain
               |                                           |
        send to SPV-locked output                          |
        wait out confirmation period                       |
               ------------------------SPV Proof---->      |
                                                wait out contest period
                                                           |
                                                           :
                                                 (intra-chain transfers)
                                                           :
                                                           |
                                                send to SPV-locked output
                                              wait out confirmation period
                         <----SPV Proof--------------------
        contest period begins
                         <----SPV Reorganization Proof-----
        contest period ends (failed)
                         <----New SPV Proof----------------
        wait out contest period
                |
                :
        (intra-chain transfers)
                :
                |
    ```