# notes from _IPFS - Content Addressed, Versioned, P2P File System_

<<<<<<< HEAD
##### _code is written in the Go programming language_
=======
##### code contained here is written in the Go programming language
>>>>>>> 70fd5f3a419b63c2e836e7c26ed7a41416844a05

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

### IPFS protocol

- divided into a stack of sub-protocols
- each sub-protocol is responsible for different functionality
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

##### Network Stack Features

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

#### DSHT Interface:

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

#### Tamper Resistance

  - all content is verified with its checksum
  - if data is tampered with or corrupted - IPFS detects it

#### Deduplication

  - all objects that hold the exact same content are equal
    - only stored once

#### IPFS Object Format

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
```

- To store data on the IPFS Merkle DAG - object references must be content
  addressed and encoded in the IPFS Object format
- applications have complete control over the data field
  - applications can use any custom data format
    - IPFS does not need to understand the format
- IPFS uses a separate in-object link table which allows the following:
  - list all object references in an object
    - ```<object multihash> <object size> <link name>```
  - resolve string path lookups - ```foo/bar/baz```
    - IPFS resolves the 1st path component to a hash in the object's link table
    - then fetches the 2nd object
    - then repeats with the next component
    - string paths can walk the Merkle DAG regardless of the data formats
      contained in the Merkle DAG
  - resolve all objects referenced recursively
- a raw data field and a common link structure are required components for
  constructing arbitrary data structures on top of IPFS

##### Potential IPFS Merkle DAG Data Structures

- the following systems can be modeled on top of the IPFS Merkle DAG:
  - key-value stores
  - traditional relational databases
  - linked data triple stores
  - linked document publishing systems
  - linked communications platforms
  -  cryptocurrency blockchains
- these systems use IPFS as a transport protocol

#### Paths

<<<<<<< HEAD
- IPFS objects can be traversed with a string path API
=======
- IPFS objects cna be traversed with a string path API
>>>>>>> 70fd5f3a419b63c2e836e7c26ed7a41416844a05
- full path format:
  - ```/ipfs/<hash-of-object>/<name-path-to-object>```
- there is no global root
  - the root is simulated with content addressing
  - all objects are always accessible via their hash
- given 3 objects in path ```<foo>/bar/baz```
  - the last object is accessible by all of the following:
    - ```/ipfs/<hash-of-foo>/bar/baz```
    - ```/ipfs/<hash-of-bar>/baz```
    - ```/ipfs/<hash-of-baz>```

#### Local Objects

- IPFS clients require some local storage
  - external system on which to store and retrieve local raw data
    - this data is for the objects IPFS manages
  - type of storage depends on the node's use case
- all blocks available in IPFS are in some node's local storage
  - when users request objects - they are found, downloaded, and stored locally
    - the data may only be stored temporarily
  - provides fast lookup for some configurable amount of time for which the
    data is kept in storage

#### Object Pinning

<<<<<<< HEAD
- to ensure the survival of a particular object - nodes can do this by
  ```pinning``` the objects
  - ensures objects are kept in the node's local storage
  - can be done recursively
    - pin down all linked descendent objects
      - all objects pointed to are also stored locally
- allows for IPFS to be a web with permanent links
  - objects can ensure the survival of other objects pointed to

#### Publishing Objects

- IPFS is globally distributed
  - designed to allow data from millions of users to coexist together
- DHT allows publishing objects fairly, securely, and in a distributed fashion
  - uses content-hash addressing
- to published an object:
  - add the object key to the DHT
  - add the publisher as a peer
  - give users the object's path
- objects are immutable
  - like in Git - new versions of the objects hash differently

#### Object-level Cryptography

- IPFS can handle object-level cryptography operations
  - an encrypted or signed object is wrapped in a special frame
    - this frame allows encryption or verification of the raw bytes

    ```Go
        type EncryptedObject struct {
            Object []bytes
            // raw object data encrypted

        Tag []bytes
        // optional tag for encryption groups
        }

        type SignedObject struct {
            Object []bytes
            // raw object data signed

            Signature []bytes
            //hmac signature

            PublicKey []multihash
            // multihash identifying key
        }
    ```

- cryptographic operations change the object's hash
  - this defines a different object
- IPFS automatically verifies signatures
  - data can be decrypted with user-specified keychains
- the links to the encrypted objects are also protected
  - this makes traversal impossible without a decryption key
  - possible to have a parent object encrypted under one key and the child
    object can be encrypted with a different key or not encrypted at all
    - this secured links to shared objects

### Files
- versioned file system hierarchy
- IPFS defines a set of objects for modeling a versioned filesystem on top of
  the Merkle DAG

#### Object model inspired by Git

1. ```block```: a variable-sized block of data
2. ```list```: a collection of blocks or other lists
3. ```tree```: a collection of blocks, lists, or other trees
4. ```commit```: a snapshot in the version history of a tree
- features from Git:
  - fast size lookups
    - aggregate byte sizes added to objects
  - large file deduplication
    - adding a list object
  - embedding of ```commits``` into ```trees```
- IPFS file objects are close enough to Git that conversion between the two
  systems is possible
  - a set of Git object can be converted without losing any data

#### File Object: blob

- the ```blob``` object contains an addressable unit of data
  - represents a file
- IPFS blocks are like Git blobs or filesystem data blocks
  - the IPFS blocks store user's data
  - IPFS files can be represented by both ```lists``` and ```blobs```
  - ```blobs``` have no links

    ```Go
      {
         "data": "some data here",
         // blobs have no links
      }
    ```

#### File Object: list

- ```list``` objects prepresent large/deduplicated files made up of several IPFS
  ```blobs``` concatenated together
- ```lists``` contain an ordered sequence of ```blob``` or ```list``` objects
  - the IPFS ```list``` functions similar to a filesystem file with indirect
    blocks
  - ```lists``` can contain other ```lists```
    - topologies including linked lists and balanced trees are possible
- in-file deduplications is possible using directed graphs where the same node
  appears in multiple locations
- cycles are not possible
  - this is enforced by hash addressing

    ```Go
      {
        "data": ["blob", "list", "blob"],
        // lists have an array of object types as data

        "links": [
          {
            "hash": "<has_is_entered_here>",
            "size": "<123456>"
          },
          {
            "hash": "<has_is_entered_here>",
            "size": "<123456>"
          },
          {
            "hash": "<has_is_entered_here>",
            "size": "<123456>"
          }
          // lists have no names in links
        ]
      }
    ```

#### File Object: commit

- the ```commit``` object in IPFS represents a snapshot in the version history
  of any object
  - similar to Git - but can reference any type of object
  - also links to author objects

    ```Go
      {
        "data": {
          "type": "tree",
          "data": "2014-09-20 12:44:06Z",
          "message": "This is a commit message."
        },

        "links": [
          {
            "hash": "<hash_goes_here>",
            "name": "parent", "size": 12345
          },
          {
            "hash": "<hash_goes_here>",
            "name": "object", "size": 1234
          },
          {
            "hash": "<hash_goes_here>",
            "name": "author", "size": 123
          }
        ]
      }
    ```

    ```Go
      - Sample Object Graph:
                 ccc111
                    |
             ___ ttt111 ____
            |       |       |
        ttt222   ttt333_    |
            |       |    \  |
        bbb111   lll111  bbb222
             ______ | ______
            |       |       |
         bbb333  bbb444  bbb555

      - Sample Objects:
          > ipfs file-cat <ccc111-hash> --json
          {
            "data": {
              "type": "tree",
              "data": "2014-09-20 12:44:06Z",
              "message": "This is a commit message."
            },
            "links": [
              {
                "hash": "<ccc000-hash>",
                "name": "parent", "size": 12345
              },
              {
                "hash": "ttt000-hash>",
                "name": "object", "size": 1234
              },
              {
                "hash": "<aaa000-hash>",
                "name": "author", "size": 123
              }
            ]
          }
          > ipfs file-cat <ttt111-hash> --json
          {
            "data": ["tree", "tree", "blob"],
            "links": [
              {
                "hash": "<ttt222-hash>",
                "name": "ttt222-name", "size": 12345
              },
              {
                "hash": "ttt333-hash>",
                "name": "ttt333-name", "size": 1234
              },
              {
                "hash": "<bbb222-hash>",
                "name": "bbb222-name", "size": 123
              }
            ]
          }
          > ipfs file-cat <bbb222-hash> --json
          {
            "data": "blob222 data",
            "links": []
          }
    ```

#### Version Control


=======
- ...

### Files
- versioned file system hierarchy
- inspired by Git
>>>>>>> 70fd5f3a419b63c2e836e7c26ed7a41416844a05

### Naming

- self certifying mutable name system
