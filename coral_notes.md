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