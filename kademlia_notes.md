# notes from _Kademlia: A Peer-to-peer Information System Based on the XOR Metric_

* Kademlia is a p2p distributed hash table (DHT)
  * minimizes amount of configuration messages nodes send to learn about each
    other
  * configuration spreads automatically via key lookups
  * nodes have the knowledge and flexibility to route queries through low
    latency paths
  * uses parallel asynchronous queries to avoid timeout delays from failed nodes
  * the algorithm which nodes use to record each other's existence is resistent
    to some denial of service attacks
  * uses novel XOR metric for distance between points in the key space
    * XOR is symmetric
      * Kademlia participants receive lookup queries from precisely the same
        distribution of nodes contained in their routing tables
      * Kademlia can send a query to any node within an interval
        * allows it to select routes based on latency
        * allows to send parallel asynchronous queries to several equally
          appropriate nodes
* Kademlia uses a single routing algorithm from start to finish in order to
  locate nodes near a particular ID
* assigns 160-bit opaque IDs to nodes
  * provides a lookup algorithm that locates successively closer nodes to any
    desired ID - converges to the lookup target in logarithmically many steps
* nodes are treated as leaves on a binary tree
  * each node's position is determined by the shortest unique prefix of its ID
  * for any given node - divide the binary tree into a series of successively
    lower subtrees that don't contain the node
  * the highest subtree consists of the half of the binary tree not containing
    the node
  * the nest subtree consists of the half of the remaining tree not containing
    the node
    * this pattern repeats
  * ensures every node knows of at least 1 node in each of its subtrees
    * this guarantees that any node can locate any other node by its ID

## XOR metric

* each Kademlia node has a 160-bit node ID
* every message that a node transmits includes its node ID
* keys are also 160-bit identifiers
  * assign ``(key, value)``` pairs to particular nodes
    * relies on a notion of distance between 2 identifiers
* in a fully populated binary tree of 160-bit IDs - the magnitude of the
  distance between 2 IDs = height of the smallest subtree containing both IDs

## node state

* Kademlia nodes store contract information about each other to route query
  messages
  * for each ```0 <= i < 160``` every nodes keeps a list of IP address, UDP
    port, and node ID for nodes of distance between _2<sup> i</sup>_ and
    _2<sup> i+1</sup>_ from it self
    * these lists are called k-buckets
* each k-bucket is kept sorted by time last seen
  * the least recently seen node at the head and the most recently seen node at
    the tail end
  * if the values of _i_ are small the k-buckets are generally empty
    * no appropriate nodes will exist
  * if the values of _i_ are large the lists can grow up to size _k_
    * _k_ is a system wide replication parameter
    * _k_ is chosen so that any given _k_ nodes are very unlikely to fail within
      an hour of each other
* when a Kademlia node receives any message (request or reply) from another node
  * updates the appropriate k-bucket for the sender's node ID
    * if sending node already exists in recipient's k-bucket
      * then the recipient moves it to the tail of the list
    * if the node is not already in the appropriate k-bucket and the bucket
      has fewer than _k_ entries
      * then the recipient inserts the new sender at the tail of the list
    * if appropriate k-bucket is full
      * then the recipient pings the k-bucket's least recently seen node
        and decides what to do from there
    * if least recently seen node fails to respond
      * then it is evicted from the k-bucket and new sender is inserted at
        the tail end
    * if least recently seen node responds
      * then it is moved to the tail of the list and new sender's contract
        is discarded
* k-buckets implement a least recently seen eviction policy
  * but live nodes are never removed
* the longer a node has been up - the more likely it is to remain up for
  another hour
  * by keeping the oldest live contacts around - k-buckets maximize the
    probability that the nodes they contain will remain online
* k-buckets provide resistance to certain DoS attacks
  * the routing state of the nodes cannot be flushed by flooding the system
    with new nodes
  * Kademlia nodes will only insery the new nodes in the k-buckets when old
    nodes leave the system