# notes from _IPFS - Content Addressed, Versioned, P2P File System_

- InterPlanetary File System (IPFS) is a p2p distributed file system
- seeks to connect all computing devices with the same system of files
  - provides high throughput content addressed block storage model
    - with content addressed hyper links
  - forms a generalized Merkle DAG
    - data structure with versioned file systems, blockchains, and Permanent Web
- combines a distributed hashtable, an incentivized block exchange, and a
  self-certifying namespace
- no centralized single point of failure
- nodes to not need to trust each other
- all data is modeled as part of the same Merkle DAG

## Distributed Hash Tables (DHTs)

- used to coordinate and maintain metadata about p2p systems

### Kademlia DHT

- efficient lokup through large networks
  - queries on average contact nodes
  - 20 hops are required for a network of 10,000,000 nodes
- low coordination overhead
  - optimizes the number of control messages it sends to other nodes
- resistance to various attacks by preferring long-lived nodes
- wide usage in p2p applications
  - used in Gnutella and BitTorrent

### Coral DSHT

- extends Kademlia
1. Kademlia stores values in nodes whose IDs are nearest to the key
   - using XOR-distance
   Coral stores addresses to peers who can provide the data blocks
2. Coral relaxes the DHT API from ```get_value(key)``` to
   ```get_any_values(key)``` - Distributed Sloppy Hash Table
   - Coral users only need a single working peer
     - not complete list
   - Coral can distribute only subsets of the values to the
     nearest nodes - avoids overloading all nearest nodes when a
     key becomes popular
3. Coral organizes a hierarchy of separate DSHTs - clusters
   - depending on region and size
   - enables nodes to query peers in their region 1st
     - find nearby data without querying distant nodes
     - reduces latency of lookups

### S/Kademlia DHT

- extends Kademia to protect against malicious attackes
- provides schemes to secure ```NodeId``` generation
  - prevents Sybill attacks
  - requires nodes to create a PKI key pair
    - derive their identity from it
    - sign their messages to each other
  - one scheme includes PoW crypto puzzle to make generating
    Sybils expensive
- nodes lookup values over disjoint paths
  - in order to ensure honest nodes can connect to each other in
    the presence of a large fraction of adversaries in the network
  - achieves a success rate of 0.85 even with an adversarial fraction as large as 1/2 of the nodes

### BLock Exchanges - BitTorrent

- succeeds in coordinated networks of trusting peers (swarms) to
  cooperate in distributing pieces of files to each other
- data exchange protocol for BitTorrent uses a quasi tit-fot-tat
  strategy
  - rewards nodes who contribute to each other
  - punishes nodes who only leech others' resources
- peers track the availability of file pieces
  - prioritizing sending rarest pieces 1st
  - takes load off the seeders
  - non-seeding peers capable of trading with each other
- vulnerable to exploitative bandwidth sharing strategies
  - ProShare is a peer bandwidth allocation strategy that resists
    exploitative strategies
    - improves performance of swarms

### Version Control Systems - Git

- Version Control Systems provide facilities to model files
  changing over time
  - distribute diferent versions efficiently
- Git provides powerful Merkle DAG object model
  - captures changes to a filesystem tree in a distributed-
    friendly way
  - immuteable objects represent
    - Files ```(blob)```
    - Directories ```(trees)```
    - Changes ```(commit)```
  - objects are content-addressed - by cryptographic hash of their
    contents
  - links to other objects are embedded
    - forms a Merkle DAG
    - provides many useful integrity and work-flow properties
  - most versioning metadata are only pointer references
    - inexpensive to create and update
  - version changes only update references or add objects
  - distributing version changes to other users
    - transferring objects and updating remote references

### Self-Certified Filesystems - SFS

- 