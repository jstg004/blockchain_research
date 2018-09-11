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

