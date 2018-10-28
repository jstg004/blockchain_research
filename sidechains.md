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
    - POW has the property that anyone can contribute without enrolling
    - contribution is weighed by computational power
      - allows for anonymous membership without risk of Sybil attack
        - Sybil attack is when 1 party joins many times - has a disproportionate
          input into the signature
  - DMMS could be a solution to the Byzantine Generals Problem
  - Bitcoin's DMMS is cummulative - blocks are chained together
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
  - validators of a sidechainshould only be required to track another chain
    if that is an explicit consensus rule of the sidechain it self
- users should not be required to track sidechains they are not actively using

### Proposed solution

- transfer assets by providing proofs of possession in the transferring
  transactions themselves
  - avoids the need to track the sending chain
1. when moving assets from one blockchain to another:
   - create a transaction on the 1st blockchain - locking the asset
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
- sidechains cannot cause unauthorised creation of coins
  - this is because sidechains transfer existing assets from the parent chain
    - new assets are NOT created
  - relies on the parent chain to maintain the security and scarcity of
    its assets
- sidechains can implement new transaction designs, trust models,
  economic models, assets issuance semantics, or cryptographic features
  - can differ from the parent chain

## Design rationale

- ...