# notes from _IPFS - Content Addressed, Versioned, P2P File System_

##### code contained here is written in the Go programming language

- InterPlanetary File System (IPFS) is a p2p distributed file system
- IPFS seeks to connect all computing devices with the same system of files
  - provides high throughput content addressed block storage model
    - with content addressed hyper links
  - forms a generalized Merkle DAG
    - data structure with versioned file systems, blockchains, and Permanent Web
  - combines a distributed hashtable, an incentivized block exchange, and a
    self-certifying namespace
  - no centralized single point of failure
  - nodes do not need to trust each other
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

### Block Exchanges - BitTorrent

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
  - distribute different versions efficiently
- Git provides powerful Merkle DAG object model
  - captures changes to a filesystem tree in a distributed-
    friendly way
  - immutable objects represent
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

## IPFS Design

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
- users can instantiate a new node identity on every launch if needed
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

#### DSHT interface:

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


### Block Exchange - BitSwap Protocol

- a protocol inspired by the BitTorrent protocol
- novel block exchange protocol
- governs efficient block distribution
- modelled as a market
- data replication is incentivized
- trade strategies are swappable
- data distribution occurs when blocks are exchanged with peers
- peers looking to acquire a set of blocks (```want_list```) and have another
  set of blocks to offer in exchange (```have_list```)
- not limited to the blocks in one torrent
  - operates as a persistent marketplace where a node can acquire the blocks
    blocks that they require
    - the node can acquire the blocks regardless of what files those blocks are
      part of
    - blocks can come from completely unrelated files in the filesystem
    - nodes come together to barter in the market place
- BitSwap nodes must provide direct value to each other in the form of blocks
  - in some cases nodes must work for their blocks
    - if a node has nothing that its peers want - it seeks the pieces its
      peers want
      - lower priority than what the node wants itself
    - this incentivizes nodes to cache and disseminate rare pieces
      - this holds true even if the nodes are not interested in the rare pieces directly

#### BitSwap Credit

- nodes must be incentivized to seed when they do not need anything specific
- BitSwap nodes send blocks to their peers optimistically
  - expect the debt to to be repaid
- the protocol needs to incentivize nodes to seed when they do not need
  specific blocks - they may have the blocks other nodes are seeking
- BitSwap nodes send blocks to their peers optimistically
- a credit system is protection against leeching nodes:
  - peers track their balance (in bytes verified) with other nodes
  - peers send blocks to debtor peers probabilistically, according to
    a function that falls as debt increases
- if a node decides not to send to a peer - that node then ignores the
  peer for an ```ignore_cooldown``` timeout
  - this prevents senders from trying to game the probability
  - default BitSwap is 10 seconds

#### BitSwap Strategy

1. maximize he trade performance for the node - and entire exchange
2. prevent freeloaders from exploiting and degrading the exchange
3. be effective with and resistant to other unknown strategies
4. be lenient to trusted peers

- example of a function sigmoid - scaled by a debt ratio
  - ```r = bytes_sent / (bytes_recv + 1)```
  - given ```r``` - let the probability of sneding to a debtor be:
    - ```P(send | r) = 1 - (1/ (1 + exp(6-3r)))```
    - this function drops off quickly as the nodes' debt ratio
      surpasses twice the established credit
  - the debt ratio if a measure of trust
    - favorable to debts between nodes that have previously exchanged
      large amounts of data successfully
    - unfavorable to unknown/untrusted nodes
    - provides resistance to attackers who would create many new nodes
      - known as sybill attack
    - protects previously successful trade relationships
      - even if one of the nodes is not valuable at the time
    - eventually chokes relationships that have deteriorated until
      they improve

#### BitSwap Ledger

- BitSwap nodes keep ledgers accounting the transfers with other nodes
  - allows doe nodes to keep track of history and avoid tampering
- BitSwap nodes activate a connection and exchange their ledger
  - if ledgers do not match - the ledger is reinitialized from scratch
    - the accrued credit or debt is lost
- possible for malicious nodes - trying to erase debts - to
  purposefully lose the ledger
  - unlikely that nodes will have accrued enough debt to warrant also
    losing the accrued trust
  - partner node is free to count this as misconduct - refuses to trade

    ```Go
    type Ledger struct {
        owner        NodeId
        partner      NodeId
        bytes_sent      int
        bytes_recv      int
        timestamp Timestamp
    }
    ```

- nodes are free to keep the ledger history
  - not necessary for correct operation
- nodes are free to garbage collect ledgers as necessary
  - starting with the less useful ledgers

#### BitSwap Specification

- BitSwap nodes follow this simple protocol:

    ```Go
    // Additional state kept
    type BitSwap struct {
        ledgers map[NodeId]Ledger
        // Ledgers known to this node, inc inactive

        active map[NodeId]Peer
        // currently open connections to other nodes

        need_list []Multihash
        // checksums of blocks this node needs

        have_list []Multihash
        // checksums of blocks this node has
    }

    type Peer struct {
        nodeid NodeId
        ledger Ledger
        // Ledger between the node and this peer

        last_seen Timestamp
        // timestamp of last received message

        want_list []Multihash
        // checksums of all blocks wanted by peer
        // includes blocks wanted by peer's peers
    }

    // Protocol interface:
    interface Peer {
        open (nodeid :NodeId, ledger :Ledger);
        send_want_list (want_list :WantList);
        send_block (block :Block) -> (complete :Bool);
        close (final :Bool);
    }
    ```

- lifetime of a peer connection:
  1. Open: peers send ```ledgers``` until they agree
  2. Sending: peers exchange ```want_lists``` and ```blocks```
  3. Close: peers deactivate a connection
  4. Ignored: (special) a peer is ignored (for the duration of a timeout)
     - if a node's strategy avoids sending

##### ```Peer.open(NodeId, Ledger)```

  - a node initializes a connectionwith a ```Ledger```
    - either stored from a connection in the past or a new ```Ledger``` zeroed
      out
  - the node then sends an ```Open``` message with the ```Ledger``` to the peer
  - when an ```Open``` message is received - the peer chooses to activate the
    connection or not
    - is the receiver's ```Ledger``` - the sender is not a trusted agent
      - the receiver may ignore the request
      - untrusted if the transmission is below 0 or if the sender has a large
        outstanding debt
      - ```ignore_cooldown``` timeout is used to probabilistically ignore
        requests - allows for errors to be corrected
        - aids in thwarting attacks
  - receiver activates a connection - receiver initializes a ```Peer```
    object with the local version of the ```Ledger``` and sets the
    ```last_seen``` timestamp
    - then compares received ```Ledger``` with its own ```Ledger```
    - if they match - peer creates a new zeroed out ```Ledger``` and sends it

##### ```Peer.send_want_list(WantList)```

  - nodes advertise their ```want_list``` to all connected peers while the
    connection is open
  - the ```want_list``` is advertised during the following scenarios:
    - upon opening the connection
    - after a randomized periodic timeout
    - after a change in the ```want_list```
    - after receiving a new block
  - when a ```want_list``` is received - a node stores it
    - then the node checks whether it has any wanted blocks
    - if wanted blocks are found they are sent to the BitSwap Strategy

##### ```Peer.send_block(Block)```

  - node transmits the block data to send a block
  - when all data is received - the receiver computes and verifies the Multihash
    checksum - then returns confirmation
  - when the correct transmission of a block is finalized - the receiver moves
    the block from the ```need_list``` to the ```have_list```
    - receiver and sender then update their ledgers to reflect additional bytes
      transmitted
  - if sender is malfunctioning or attacking the receiver
    - the transmission verification with fail
    - the receiver is free to refuse further trades
  - BitSwap expects to operate on a reliable transmission channel
    - transmission errors
    - the could lead to incorrect penalization of an honest sender
    - expected to be caught before data is given to BitSwap

##### ```Peer.close(Bool)```

  - this parameter signals wether or not the intention to tear down the\
    connection is from the sender
    - if false receiver may opt to re-open connection immediately
      - avoids premature closes
  - a peer connection is closed if either of these conditions are met:
    - ```silence_wait``` timeout has expired without receiving any messages
      from the peer - default BitSwap timeout is 30 seconds
      - ```Peer.close(false)``` is issued by the node
    - node is exiting and BitSwap is being shut down
      - ```Peer.close(true)``` is issued by the node
  - after close message - receiver and sender tear down the connection
    - any stored state is cleared
  - ```Ledger``` may be stored for the future if useful
  - ```Non-open``` message on an inactive connection should be ignored
    - ```send_block``` message - receiver may check the block if it is needed
      and if it is correct before use
    - all out-of-order messages trigger a ```close(false)``` message from
      receiver to force re-initialization of connection

### Object Merkle DAG

- Merkle DAG of content addressed immutable objects with links
- used to represent arbitrary data structures
  - files hierarchy
  - communication systems
- DHT and BitSwap allow IPFS to form a massive p2p system for storing and
  distributing blocks quickly and robustly
- IPFS builds a Merkle DAG - directed acyclic graph where links between objects
  are cryptographic hashes of the targets embedded in the sources
  - a generalization of the Git data structure

#### Content Addressing

  - all content is uniquely identified by its multihash checksum
    - including links

#### Tamper resistance

  - all content is verified with its checksum
  - if data is tampered with or corrupted - IPFS detects it

#### Deduplication

  - all objects that hold the exact same content are equal
    - only stored once

#### IPFS Object format

```Go
    tpye IPFSLink struct {
        Name string
        // name or alias of this link

        Hash Multihash
        // cryptographic hash or target

        Size int
        // total size of target
    }

    tpye IPFSObject struct {
        links []IPFSLink
        // array of links

        data []byte
        // opaque content data
    }
````

### Files
- versioned file system hierarchy
- inspired by Git

### Naming

- self certifying mutable name system
