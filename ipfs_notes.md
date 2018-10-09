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

## distributed hash tables (DHTs)

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

- 