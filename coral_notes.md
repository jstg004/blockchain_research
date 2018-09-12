# notes on _Democratizing content publication with Coral_

* CoralCDN is a p2p content distribution network that allows a user to run a
  web site that offers high performance and meets large demands for a low price
  * volunteer sites that run CoralCDN automatically replicate content as a side
    effect of users accessing it
* to publish through CoralCDN - make a small change to the hostname in an
  object's URL
  * this p2p DNS layer transparently redirects browsers to nearby participating
    cache nodes
    * these nodes cooperate to minimize load on the origin web server
* key goal is to avoid creating hot spots that might dissuade volunteers and
  degrade performance
  * this is achieved through Coral
    * Coral is a latency-optimized hierarchical indexing infrastructure based on
      a novel abstraction - _distributed sloppy hash table_ (DSHT)

## introduction

* availability of content on the Internet is mostly a function of the cost
  shouldered by the publisher
  * a well funded web site can reach a large audience through a combination of
    load balanced servers, fast network connections, and commercial content
    distribution networks (CDNs)
* static content can be mirrored by volunteer servers and networks
* CoralCDN leverages the aggregate bandwidth of volunteers running the software
  to absorb and dissipate most of the traffic for web sites using the system
  * replicates content in proportion to the content's popularity
* CoralCDN is built on top of Coral
  * Coral is a novel key/value indexing infrastructure
  * Coral is an ideal system for CDN's
    * allows nodes to locate nearby cached copies of web objects without
      querying more distant nodes
    * Coral prevents hot spots in the infrastructure - even under degenerate
      loads
    * exploits overlay routing technique utilized by p2p distributed hash
      tables (DHTs)
    * Coral differs from DHTs:
      * locality and hot spot prevention properties are not possible for DHTs
      * Coral's architecture is based on clusters of well connected machines
        * clusters are exposed in the interface to higher level software
      * provides weaker consistency than traditional DHTs
* CoralCDN enables people to publish content at a very low cost
* Coral introduces an epidemic clustering algorithm
  * exploits distribution network measurements
* Coral can scale to many stores of the same key without hot spot congestion
* the CoralCDN contains a p2p DNS redirection infrastructure that allows the
  system to inter-operate with unmodified web browsers

## the Coral Content Distribution Network

* the CoralCDN is composed of 3 main parts
  1. a network of cooperative HTTP proxies that handle user's requests
  2. a network of DNS nameservers for ```nyucd.net``` that map clients to nearby
     Coral HTTP proxies
  3. the underlying Coral indexing infrastructure and clustering machinery on
     which the above two parts are built

### usage models

* CoralCDN is transparent to clients

#### publishers

* a wb site published for ```x.com``` can change selected URLs in their pages
  to Coralized URLs
  * ```http://www.x.com.nyud.net:8090/y.jpg```

#### third parties

* an interested 3rd partycan Coralize a URL before publishing it
  * causes all embedded relative links to use CoralCDN as well

#### users

* Coral-aware users can manually construct Coralized URLs when surfing slow or
  overloaded web sites
  * all relative links and HTTP redirects are automatically Coralized

### system overview

#### steps for a client to access a Coralized URL

  1. client sends a DNS request for ```www.x.com.nyud.net``` to its local resolver
  2. clients resolver attempts to resolve the host name using some Coral DNS
     server(s)
     * could start at one of the few registered under the ```.net``` domain
  3. when a query is received - a Coral DNS server probes the client to
     determine its round-trip-time and last few network hops
  4. based on probe results - DNS server checks Coral to see if there are any
     known nameservers or HTTP proxies near client's resolver
  5. DNS server replies - returns and servers found through Coral
     * if none are found - returns a random set of nameservers and proxies
     * if DNS server is close to client - returns nodes that are close to itself
  6. client's resolver returns the address of a Coral HTTP proxy for
     ```www.x.com.nyud.net```
  7. client sends the HTTP request ```http://www.x.com.nyud.net:8090/```
     to the specified proxy
     * if proxy is chaching the file locally - returns file and stops
     * if not cached than process continues to step 8
  8. proxy looks up web object's URL in Coral
  9. if Coral returns the address of a node caching the object - proxy fetches
     the object from this node
     * if no address is returned - proxy downloads the object from the origin
       server ```www.x.com```
  10. proxy stores the web object and returns it to the client browser
  11. proxy stores a reference to itself in Coral
      * records the fact that it is now caching the URL

### Coral indexing abstraction

* DSHTs are designed for applications applications storing soft-state key/value
  pairs - where multiple values may be stored under the same key
  * the CoralCDN uses this mechanism to map a variety of keys to addresses of
    CoralCDN nodes
* each Coral node belongs to several distinct DSHTs - called clusters
  * each cluster is characterized by a max desired network round-trip-time (RTT) - called diameter
  * system is parameterized by a fixed hierarchy of diameters - known as levels
  * every node is a member of 1 DSHT at each level
* Coral queries nodes in higher-level fast clusters before those in lower-level
  slower clusters
  * this reduces latency of lookups and increases chances of returning values
    stored by nearby nodes

#### Coral interface for higher-level applications

* ```put(key, val, ttl, [levels])```
  * inserts a mapping from the key to some arbitrary value
  * specifies the time-to-live of the reference
  * caller can optionally specify a subset of the cluster hierarchy
    * this restricts the operation to certain levels
* ```get(key, [levels])```
  * retrieves some subset of the values stored under a key
  * can optionally specify a subset of the cluster hierarchy
* ```nodes(level, count, [target], [services])```
  * returns ```count``` neighbors belong to the node's cluster as specified by
    ``level```
  * ```target```- if supplied - specifies the IP address of a machine to which
    the returned nodes would ideally be near
  * Coral can probe ```target``` and exploit network topology hints stored in
    DSHT to satisfy the request
  * if ```services``` is specified - Coral will only return nodes running the
    specidied service
* ```levels()```
  * returns the number of levels in Coral's hierarchy and their corresponding
    RTT thresholds

## application layer components

* Coral DNS server directs browsers fetching Coralized URLs to Coral HTTP
  proxies
  * proxies exploit each others caches - minimize transfer latency and load on
    origin web servers

### Coral DNS server

* Coral DNS server (```dnssrv```) - returns IP addresses of Coral HTTP proxies
  when browsers look up the host-names in Coralized URLs
* attempts to return proxies near the requesting clients to improve locality
  * whenever a DNS resolver (client) contacts a nearby ```dnssrv``` instance
    the ```dnssrv``` returns proxies within an appropriate cluster and ensures
    that future DNS requests from that client do not need to leae the cluster
* using the ```nodes``` function - the ```dnssrv``` exploits Coral's on-the-fly
  network measurement capabilities and stored topology hints to increase the
  chances of clients discovering nearby DNS servers
* every instance of ```dnssrv``` in an authoritative nameserver for the domain
  ```nyucd.net```
  * DNS maps any domain name ending in ```http.L2.L1.L0.nyucd.net``` to one or
    more Coral HTTP proxies - (L2 = level 2, ect)
    * for ```(n + 1)-level``` hierarchy - domain name extended out to ```Ln```
    * these domains names can get unwieldy
      * to aid this a DNS DNAME alias of ```nyud.net``` is established with a
        target as ```http.L2.L1.L0.nyucd.net```
        * this allows URLs to have more concise form
        ```http://www.x.com.nyud.net:8090/```
* to achieve locality - ```dnssrv``` measures its RTT to the resolver and then
  categorizes it by level
* the ```dnssrv``` returns the addresses of CoralProxies in the cluster whose
  level corresponds to the client's level categorization
  * if the RTT between the DNS client and the ```dnssrv``` is below the level-i
    threshold (for the best i)
    * ```dnssrv``` obtains a list of these nodes using the ```nodes``` function
    * a ```dnssrv```` always returns CoralProxy addresses with short TTL fields
* to achieve better locality:
  * ```dnssrv``` also specifies the client's IP address as a target argument to
    nodes
    * causes Coral to probe the addresses of the last 5 network hops to the client - use this result to look for clustering hints in the DSHT
* to avoid significantly delaying clients:
  * Coral maps the netowrk hops using a built in traceroute type of mechanism
    * combines concurrent probes and aggressive time-outs to minimize latency
    * a Coral node caches results to avoid repeatedly probing the same client
* the closer the ```dnssrv``` is to a client - the better its selection of
  CoralProxy addresses will likely be for the client
  * ```dnssrv``` exploits the authority section of DNS replies to lock a DNS
    client into a good cluster whenever it sees a nearby ```dnssrv```
* ```dnssrv``` selects the nameservers it returns from the appropriate cluster
  level
  * uses the ```target``` argument to exploit measurement and network hints
  * gives nameservers in the authority section a long TTL
    * this makes nearby ```dnssrv``` override any inferior nameservers that a
      DNS server may be caching from previous queries
    * if more distant than the level-1 timing threshold - ```dnssrv``` then
      claims to return nameservers for domain ```L0.nyucd.net```
    * clients closer than the level-1 timing threshold - returns nameservers for
      ```L1.L0.nyucd.net```
    * for clients closer the level-2 threshold - returns the nameservers for
      domain ```L2.L1.L0.nyucd.net```
  * DNS resolvers query the servers for the most specific known domain
    * so the closer ```dnssrv``` instances to override the results of more
      distant ones
* CoralProxy addresses are returned with short TTL fields because browsers
  do not handle bad HTTP servers well
  * added precaustion to this - ```dnssrv``` only returns CoralProxy addresses
    which it has recently verified 1st hand
    * sometimes need to synchronously checking a proxy's status via UDP RPC
      prior to replying to a DNS query
* upstream bandwidth only clients can flag their proxy as non-recursive
  * ```dnssrv``` will only return that proxy to clients on local networks

### Coral HTTP proxy

* CoralProxy satisfies HTTP requests for Coralized URLs
* many Coral origin servers are likely to have slower network connections
* Coral selects proxies only based on client locality
  * CoralCDN is easier for proxy to fetch a particular URL
* CoralProxy fetches web pages from other proxies whenever possible
  * this minimizes load on origin servers
  * each proxy keeps a local cache - so it can immediately fulfill requests
    * when client requests a non-resident URL - CoralProxy 1st attempts to
      locate a cached copy of the referenced resource which is using Coral
      with the resource indexed by a hash of its URL
    * if CoralProxy discovers 1 or more other proxies have the data
      * then attempts to fetch the data from the proxy it 1st connects to
    * if Coral provides no referrals or if no referrals return the data - then
      CoralProxy fetches the resource directly from the origin
* when CoralProxy fetches a web object it inserts a reference to itself in its
  DSHT with a TTL of 20 seconds
* once any CoralProxy obtains a complete file - it inserts a longer lived
  reference to itself (something like 1 hour)
  * these longer lived references overwrite shorter lived references
  * can be stored on well selected nodes - even under high insertion load
* CoralProxies periodically renew referrals to resources in their cache

## Coral - hierarchical indexing system

### Coral's key-based routing layer

* Coral's keys are opaque 160-bit ID values
  * nodes are assigned IDs in the same 160-bit identifier space
    * a node's ID is a hash of its IP address
* a node is close to a key if the distance between the key and the node's ID is
  small
* Coral ```put``` operation stores a key/value pair at a node close to the key
* Coral ```get``` operation searches for stored key/value pairs at nodes
  successively closer to the key
* every DSHT contains a routing table
  * for any key ```k```, a node ```R```'s routing table allows it to find a node
    closer to ```k```, unless ```R``` is already the closest node
  * these routing tables are based on Kademlia
    * Kademlia defines the distance between 2 values in the ID-space to be their
      bitwise exclusive (XOR) - interpreted as an unsigned integer
    * using XOR metric:
      * IDs with longer matching prefixes (of most significant bits) are
        numerically closer
* the size of a node's routing table in a DSHT is logarithmic in the total

### sloppy storage

* the Coral sloppy storage technique caches key/value pairs at nodes whose IDs
  are close to the key being referenced
  * these cached values reduce hot spot congestion and tree saturation
    throughout the indexing infrastructure
    * frequently satisfy ```put``` and ```get``` requests at nodes other than
      those closest to the key

#### insertion algorithm

* Coral performs a 2 phase operation to insert a key/value pair
  * in the forward phase (1st phase) - Coral routes to nodes that are
    successively closer to the key


### hierarchical operations

* several levels of DSHTs are used for locality-optimized routing and data
  placement - these are called clusters
* each Coral node has the same node ID in all clusters it belongs to
  * a node projects its presence to the same location in each of its clusters
  * this structure is reflected in Coral's basic routing infrastructure
    * supports switching between a nodee's distinct DSHTs midway through a
       lookup

#### hierarchical retrieval algorithm

* a requesting node ```R``` specifies the starting and stopping levels at which
  Coral should search
  * default: initiates the ```get``` query on its highest (L2) cluster to try
    to take advantage of network locality
  * if routing RPCs on this cluster hit some node storing key ```k```:
    * the lookup halts at this point and returns corresponding stored value(s)
      * this is done without-level clusters
  * if a key is not found - the lookup will reach ```k```'s closest node
    ```C2``` in this cluster - this indicates a failure at this level
  * node ```R``` continues the search in its L1 cluster
    * these clusters are usually concentric
    * ```C2``` likely exists at the identical location in the identifier space
      in all clusters
  * ```R``` begins searching onward from ```C2``` in its L1 cluster
    * already traversed the ID space up to ```C2```'s prefix

#### hierarchical insertion algorithm

* a node starts by performing a ```put``` on its L2 cluster
  * nearby nodes can take advantage of locality
  * this is only correct within the context of the local L2 cluster
* 


### joining and managing clusters

## implementatio

## evaluation

### server load

### client latency

### clustering

### load balancing