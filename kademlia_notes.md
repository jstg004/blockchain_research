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