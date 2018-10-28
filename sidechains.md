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

- minimize additional trust over Bitcoin's model
- securing transfers of coins between sidechains
  - receiving chain must see that the coins on the sending chain were
    correctly locked
    - using DMMS to achieve this

#### Avoid the introduction of single points of failure

- trusting individual signers
  - expect them to
    - behave honestly
    - never be compromised
    - never leak secret key material
    - never coerced
    - never stop participating in the network
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

- transfer mechanisms from parent chain to sidechain and back are the same
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
    ```

- pegged sidechains may carry assets from many chains
  - assumptions cannot be made about the security of these chains
  - different assets must not be interchangeable
    - only by explicit trade
    - sidechains must treat assets from separate parent chains as separate
      asset types
- the parent chain and sidechains should perform SPV validation of data on
  each other
  - parent chain clients cannot be expected to observe every sidechain
  - users import PoW from the sidechain into the parent chain in order to prove
    possession
    - in a symmetric two-way peg - the converse is also true

### Asymmetric two-way peg

- users of the sidechain are full validators of the parent chain
- transfers from parent chain to sidechain do not require SPV proofs
  - all validators are ware of the state of the parent chain
  - the parent chain is still unaware of the sidechain
    - SPV proofs are required to transfer back
- prevents 52% attacker from falsely moving coins from the parent chain to
  the sidechain
- the sidechain validators are forced to track the parent chain
- implies that reorganizations on the parent chain may cause reorganizations
  on the sidechain
  - results in significant expansion in complexity

## Drawbacks

### Complexity

#### Network level complexity

- multiple unsynchronized blockchains that support transfers between each other
  - must support transaction scripts which can be invalidated by a later
    reorganization proof
  - need software which can automatically detects misbehavior as well as
    produce and publish the proofs

#### Asset level complexity

- individual chains may support arbitrarily many assets
  - even assets that did not exist when the chain was 1st created
- each asset is labelled with the chain it was transferred from
  - ensures their transfers can be unwound correctly

### Fraudulent transfers

#### Reorganizations of arbitrary depth

- could allow an attacker to completely transfer coins between sidechains
  before causing a reorganization longer than the contest period on the
  sending chain to undo its half of the transfer
- results in an imbalance between the number of coins on the recipient chain
  and the amount of locked output value backing them on the sending chain
- if attacker is allowed to return the transferred coins to the original chain
- attacker would increase the number of coins in their possession
  - this is at the expense of other users of the sidechain
- this risk can be made arbitrarily small by increasing the contest period
  for transfers
  - the duration of the contest period could be made a function of the
    relative hashpower of the 2 chains
    - the recipient chain might only unlock coins given an SPV proof of a day's
      worth of its own PoW
      - this could correspond to several days of the sending chain's PoW

#### Sidechain responses

1. no reaction
   - results in the sidechain becoming a fractional reserve of the assets it
     is storing from other chains
2. the peg and all dependent transactions could be reversed
   - coins tend to diffuse and histories intermingle
   - limits fungibility
3. reduce the amount of all coins while leaving the exchange rate intact
   - users who transferred coins to the sidechain prior to the attack are
     disadvantaged relative to new ones

### Risk of mining centralization

- miners receive compensation from the bock subsidy and fees of each chain
  they provide work for
  - in the miners economic interest to switch between providing DMMS for
    different but similarly valued blockchains
    - following changes in difficulty and movements in market value

#### Merged mining

- the blockheader definition includes a part of the parent chain's DMMS
  - enables miners to provide a single DMMS that commits to the parent chain and sidechains
- enables re-use of work for multiple blockchains
  - miners are able to claim compensation from from each blockchain that they
    provide DMMS for
- the more blockchains miners provide work for the more recourses are needed
  to track and validate all of blockchains
- miners who provide work for a subset of blockchains (not all) are
  compensated less than those who provide work for every possible blockchain
- possible for miners to delegate validation and transaction selection of any
  subset of the blockchains they provide work for
  - a delegate authority enables miners to avoid almost all of the additional
    resource requirements
    - or provide work for blockchains that they are still in the process of
      validating
    - this is centralization for validation and transaction selection for
      the blockchain - even if work generation is distributed
    - miners could choose not to provide work for blockchains which they are
      still in the process of validating
      - voluntarily giving up some compensation in exchange for increased
        validation decentralization

### Risk of soft-fork

- a soft-fork is an addition to the protocol which is backwards compatible
  - designed to strictly reduce the set of valid transactions or blocks
- a soft-fork can be implemented with a supermajority of the mining
  computational power participating - not all full nodes are needed
- participants' security with respect to the soft-forked features in only
  SPV-level until they upgrade
- a two-way peg has only SPV security
  - greater short-term dependence on miner honesty unless all full nodes on
    both systems inspect each other's chain and demand mutual validity as a
    soft-forking rule
  - could cause loss of isolation of any soft-forked-required sidechain

## Applications

- Applications to extend Bitcoin

### Altchain experiments

- creating altchains with coins that derive their scarcity and supply from
  Bitcoin
- using a sidechain that carries Bitcoins instead of a completely new currency
  - avoids issues of initial distribution and market vulnerability
  - avoids barriers to adoption for new users
    - users do not need to locate a trustworthy marketplace or invest in mining
      hardware to obtain altcoin assets

#### Technical experimentation

- sidechains are technically fully independent chains
  - able to change features of Bitcoin such as:
    - block structure
    - transaction chaining
  - sidechains only affect the transfer of coins not their creation
    - no need for them to require separate currency
    - ability for experimentation without much risk for participants

##### Fixing undesired transaction malleability

- protocols that involve chains of unconfirmed transactions can be executed
  safely
- transaction malleability is a problem in Bitcoin
  - allows arbitrary users to tweak transaction data
    - this breaks any later transactions which depend on that tweaked data
    - actual content of the transaction is unchanged
- probabilistic payments is an example of a protocol broken by
  transaction malleability

##### Improved payer privacy

- ring signature scheme used by Monero can reduce the systemic risk of the
  transactions of particular parties being censored
  - protects the fungibility of the cryptocurrency
- ring signatures cna be used with Monero coins
  - sidechains on Bitcoin could add this feature to Bitcoin
- provacy improvement suggestions:
  - Maxwell and Poelstra's _Output distribution obfuscation_
  - Back's _Bitcoins with homomorphic value (validatable but encrypted)_

##### Script extensions

- support for new cryptographic primitives such as Lamport signatures to
  potentially secure against quantum computers

#### Economic experimentation

##### Demurrage idea be Freicoin

- alternate mechanism for achieving block rewards on the sidechain
- in a demurring cryptocurrency all spent outputs lose value over time
  - the lost value is recollected by miners
  - keeps currency supply stable while rewarding the miners
- loss to demurrage is enacted uniformly everywhere and instantaneously
- mitigates the possibility of ong-unspent lost coins being reanimated at
  their current valuation and shocking the economy
- creates incentives to increase monetary velocity and lower interest rates
- in pegged sidechains - demurrage allows miners to be paid in existing
  valued currency

### Issued assets

- it is possible for sidechains to produce their own tokens (issues assets)
  - these tokens carry their own semantics
  - tokens can be transferred to other sidechains and traded for other assets
    and currencies - without trusting a central party
- allows for external protocols to delegate ownership and transfer tracking
  to the sidechain on which the ownership shares were issued
- issued asset chains could also support more innovative instruments
  - such as smart property
- a suitably extended scripting system and an asset-aware transaction format
  could allow for the creation of useful transactions from well-audited
  components
  - merger of a bid and an ask to form an exchange transaction
  - enables the creation of completely trustless p2p marketplaces for asset
    exchange and complex contracts

## Future directions

### Hashpower attack resistance

- a two-way peg using SPV proofs are forgeable by a 51% majority
  - they are blockable by however much hashpower is needed to build a
    sufficiently long proof during the transfer's contest period
    - if 33% hashpower can block a proof - then 67% is needed to successfully
      use a false proof

#### Assurance contracts

- sidechain's transaction fees are withheld from miners unless their hashpower
  is at least ~66% of that of the parent chain
- designed into the cryptocurrency from the start
- serve to increase the cost of blocking transfers

#### Time-shifted fees

- miners receive part of their fees in a block far in the future
  - or spread across many blocks
  - incentivized to keep the chain operational
- could incentivize miners to receive fees out-of-band
  - avoids the need to wait for future in-chain rewards
- miners could receive a token enabling them to mine a low-difficulty block far
  into the future
  - directly incentivizes its recipient to mine the chain

#### Demurrage

- block subsidies can be given to miners through demurrage to incentivize
  honest mining
- only as much can be transferred to the parent chain or other sidechains as
  was transferred out
  - fund reallocation would be localized to the sidechain in which it occurs

#### Subsidy

- a sidechain could issue its own separate native currency as a reward
  - these coins would have a free-floating value
  - this would not solve the volatility and market fragmentation issues

#### Co-signed SPV proofs

- introduces signer who must sign off on valid SPV proofs
  - watching for false proofs
  - results in a direct trade-off between centralization and security against
    a high hashpower attack
- trade-offs include:
  - signers may be required only for high value transfers
  - signers may be required only when the sidechain hashpower is too small
    of a percentage of the parent chain's hashpower

#### SNARKs

- space efficient, quickly verifiable zero-knowledge cryptographic proofs which
  verify the completion of a computation
- slow to generate - depending on computational power
- the need of a trusted setup allows for the creator of the system the ability
  to create false proofs
- possible for a low value/experimental sidechain which invokes a trusted
  authority whose only task is to execute trusted setup for a SNARK scheme
  - then blocks that prove their changes to the unspent output set could be
    constructed
    - this must be done in a zero-knowledge in the actual transactions
  - could commit to the full verification of all previous blocks
    - allows new users to get up to speed by verifying only the single latest
      block
    - these proofs could also replace the DMMS used to move coins from another
      chain
      - accomplished by proving that the sending chain is valid according to
        previously defined rules