# notes from _IPFS - Content Addressed, Versioned, P2P File System_

- code written in the Go programming language
  - <https://golang.org/>

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

## Background

### Distributed Hash Tables (DHTs)

- used to coordinate and maintain metadata about p2p systems

#### Kademlia DHT

- efficient lokup through large networks
  - queries on average contact nodes
  - 20 hops are required for a network of 10,000,000 nodes
- low coordination overhead
  - optimizes the number of control messages it sends to other nodes
- resistance to various attacks by preferring long-lived nodes
- wide usage in p2p applications
  - used in Gnutella and BitTorrent

#### Coral DSHT

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

#### S/Kademlia DHT

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

#### Merkle Directed Acyclic Graph (DAG)

- a more general construction of a Merkle Tree
- deduplicated
- no need to be balanced
- non-leaf nodes contain data

### Self-Certified File Systems - SFS

- distributed trust chains
- egalitarian shared global namespaces
- addressing remote file systems using the following scheme:
  - ```/sfs/<Location>:<HostID>```
- Location is the server network address:
  - ```HostID = hash(public_key || Location)```
- the name of an SFS file system certifies its server
- user can verify the public key offered by the server, negotiate a shared
  secret, and secure all traffic
- all SFS instances share a global namespace where name allocation is
  cryptographic - not gate by any centralized body

### IPFS Design

- distributed file system
- synthesizes successful ideas form previous p2p systems
  - evolves from and improves upon proven techniques of these previous systems
    into a single system
- a platform for writing and del=ploying applications
- a system for distributing and versioning large data
- no nodes are privileged
- nodes store IPFS objects in local storage
- nodes connect to each other and transfer objects
  - objects represent files and other data structures

### IPFS protocol is divided into a stack of sub-protocols

- each protocol is responsible for different functionality
- the subsystems are not independent
  - they are all integrated
  - leverage blended properties

#### Identities

- manage node identity generation and verification
- nodes are identified by a ```NodeId```
  - cryptographic hash of a public key
  - created with S/Kademlia's static crypto puzzle
- nodes store their public and private keys
  - they are encrypted with a passphrase
- users can instatiate a new node identity on every launch if needed
  - nodes are incentivized to remain the same

    ```Go
    type NodeId Multihash
    type Multihash []byte
    // self-describing cryptographic hash digest

    type PublicKey []byte
    type PrivateKey []byte
    // self-describinh keys

    type Node struct {
        NodeId NodeID
        PubKey PublicKey
        PriKey PrivateKey
    }
    ```

- S/Kademlia based IPFS identity generation:

    ```Go
    difficulty = <integer parameter>
    n = Node{}
    do {
        n.PubKey, n.PriKey = PKI.genKeyPair()
        n.NodeId = hash(n.PubKey)
        p = count_preceding_zero_bits(hash(n.NodeId))
    } while (p < difficulty)
    ```

- when peers connect the exchange public keys
  - check that ```hash(other.PublicKey) = other.NodeId```
  - if not, then the connection is terminated

##### Cryptographic Functions

- IPFS favors self describing values
- hash digest values are stored in multihash format
  - includes a short header specifying the hash function used and digest length
    in bytes
  - ```<function code><digest length><digest bytes>```
  - allows the system to:
    - choose the best function for the use case
    - evolve as function choices change
    - self describing values allow using different parameter choices capability

#### Network

- manages connections to other peers
- uses various underlying network protocols
- configurable
- IPFS nodes communicate regularly with other nodes in the network

##### Network stack features

- Transport:
  - uses any transport protocol
  - best suited for WebRTC DataChannels or uTP
- Reliability:
  - can provide reliability if underlying networks do not provide it
  - using uTP or SCTP
- Connectivity:
  - uses ICE NAT traversal techniques
- Integrity:
  - optionally checks integrity of messages using a hash checksum
- Authenticity:
  - optionally checks authenticity of messages using HMAC with the sender's
    public key

##### Peer Addressing

- IPFS can use any network
  - does not rely on or assume access to IP
  - allows IPFS to be used in overlay networks
- IPFS stores addresses ad ```multiaddr``` formatted byte strings for the
  underlying network to use
- ```multiaddr``` provides a way to express addresses and their protocols
  - includes support for encapsulation

    ```Go
    # an SCTP/IPv4 connection
    /ip4/10.20.30.40/sctp/1234/

    # an SCTP/IPv4 connection proxied over TCP/IPv4
    /ip4/5.6.7.9/tcp/5678/ip4/1.2.3.4/sctp/1234/
    ```

#### Routing

- maintains information to locate specific peers and objects
- responds to both local and remote queries
- defaults to a DHT
  - is swappable
- IPFS nodes require a routing system
  - the routing systems can find other peers' network addresses
  - the routing systems can find other peers who can serve particular objects
  - uses a DSHT based on S/Kademlia and Coral
- the IPFS DHT makes a distinction for values stored based on their size
  - small values (<= 1KB) are stored directly on the DHT
  - larger values are stored in the DHT as references
    - ```NodeId``` of peers who can serve the block

##### DSHT interface:

    ```Go
    type IPFSRouting interface {
        FindPeer(node NodeId)
        // gets a particular peer's network address

        SetValue(key []bytes, value []bytes)
        // stores a small metadata value in DHT

        GetValue(key []bytes)
        // retrieves small metadata value from DHT

        ProvideValue(key Multihash)
        // announces this node can serve a large value

        FindValuePeers(key Multihash, min int)
        // gets a number of peers serving a large value
    }
    ```

- the IPFS routing system can be swapped for one that fits the user's needs
  - the interface above must be met as a requirement


#### Exchange

- novel block exchange protocol
- BitSwap
- governs efficient block distribution
- modelled as a market
- data replication is incentivized
- trade strategies are swappable

#### Objects
- Merkle DAG of content addressed immutable objects with links
- used to represent arbitrary data structures
  - files hierarchy
  - communication systems

#### Files
- versioned file system hierarchy
- inspired by Git

#### Naming

- self certifying mutable name system
