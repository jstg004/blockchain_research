# notes from _Hashcash - A Denial of Service Counter-Measure_

* by Adam Back ~ 2002

## cost-functions

* efficiently verifiable as well as expensive to compute
* a client is the user who must compute a token using the cost-function MINT()
  * MINT() is used to create tokens to participate in a protocol with a server
  * mint is used term mint for the cost-function because of the analogy between
    creating cost tokens and minting physical money
* the server will check the value of the token using an evaluation function
  VALUE()
  * the server will only proceed with the protocol if the token has the required
    value
* interactive cost-functions
  * the server issues a challenge to the client (CHAL())

## publicly auditable

* publicly auditable cost-functions can be efficiently verified by any third
  party without any trapdoor or secret information
  * the cost-function is efficiently publicly auditable compared to the cost of
    minting the token
* the fastest algorithm to mint a fixed cost token is a deterministic algorithm

## probabilistic cost

* a cost-function where the cost to the client of minting a token had a
  predictable expected time
  * random actual time as the client can most efficiently compute the
    cost-function by starting at a random start value
  * unbounded probabilistic cost cost-function can in theory take forever to
    compute
    * the probability of taking significantly longer than expected decreases
      rapidly towards zero
  * bounded probabilistic cost cost-function is a limit to how unlucky the
    the client can be in it's search for the solution
    * the client is expected to search some key space for a known solution
    * the size of the key space imposes an upper bound on the cost of
      finding the solution

## trapdoor-free

* a trapdoor-free cost-function is one where the server has no advantage in
  mining tokens

## hashcash cost-function

* hashcash is a non-interactive, publicly auditable, trapdoor-free cost
  function with unbounded probabilistic cost
  * based on finding partial hash collisions
  * the fastest algorithm for computing partial collisions is brute force
* the server needs to keep a double spending database of spent tokens
  * this allows for detections and rejection attempts to spend the same token
    again
    * the service string can include the time at which it was minted
    * this prevents the database from growing indefinitely
    * allows for the server to discard entries from the spent database once
      expired
    * expiry period are chosen to take account of clock inaccuracy,
      computation time, and transmission delay

## interactive hashcash

* for use in TCP, TLS, SSH, IPSEC, ect
  * connections are established using a challenge chosen by the server
* aim to defend the server resources from premature depletion
  * provide graceful degradation of service with fair allocation across users
    in face of a DoS attack where one user attempts to deny service to others
    by consuming as many server resources possible

## dynamic throttling

* possible with interactive hashcash
  * dynamically adjust the work factor required for the client based on server
    server CPU load
* it is possible to only use interactive hashcash challenge-response during
  periods of high load
  * makes it possible to phase-in DoS resistent protocols without breaking
    backwards compatibility with old client software
  * during periods of high load, the non-hashcash aware clients are unable
    to connect or placed in a limited connection pool subject to older less
    effective Dos counter-measures (random connection dropping)

## hashcash-cookies

* impose a CPU cost on the connecting machine to reserve a TCP connection-slot
* connection-slot depletion attacks
  * syn-flood attack and straight-forward TCP connection-slot depletion
    * server resource that is being consumed is space available to the TCP stack
      to store per-connection state
    * it is desirable to avoid keeping per connection state until the client has
      computed a token with the interactive hashcash cost-function
* avoid storing the challenge in the connection state
  * server may choose to compute a keyed MAC of the information instead
    * send it to the client as part of the challenge
    * can verify the authenticity of the challenge and token when the client
      returns them
    * performed at the application protocol level