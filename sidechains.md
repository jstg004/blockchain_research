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