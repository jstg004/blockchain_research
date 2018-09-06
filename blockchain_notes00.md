# notes from my initial blockchain research

## notes from _Hashcash - A Denial of Service Counter-Measure_

### cost-functions

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

### publicly auditable

* publicly auditable cost-functions can be efficiently verified by any third
  party without any trapdoor or secret information
  * the cost-function is efficiently publicly auditable compared to the cost of
    minting the token
* the fastest algorithm to mint a fixed cost token is a deterministic algorithm

### probabilistic cost

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

### trapdoor-free

* a trapdoor-free cost-function is one where the server has no advantage in
  mining tokens

### hashcash cost-function

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

### interactive hashcash

* for use in TCP, TLS, SSH, IPSEC, ect
  * connections are established using a challenge chosen by the server
* aim to defend the server resources from premature depletion
  * provide graceful degradation of service with fair allocation across users
    in face of a DoS attack where one user attempts to deny service to others
    by consuming as many server resources possible

### dynamic throttling

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

### hashcash-cookies

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

## notes from _Bitcoin: A Peer-to-Peer Electronic Cash System_

### transactions

* electronic coin is defined as a chain of digital signatures
  * coin is transferred from one owner to the next:
    * digitally sign a hash of the previous transaction and the public key of
      the new owner
    * add this hash to the end of the coin
  * payee can verify the signatures to verify the chain of ownership

### double-spend problem

* payee unable to verify that one of the owners did not double-spend the coin
  * a solution is needed for the payee to know that the previous owners did not
    sign any earlier transactions
    * verify the integrity of the chain
    * only way to confirm the absence of a transaction is to be aware of all
      transactions
    * transactions must be publicly announced
    * participants need to agree on a single history of the order in which the
      transactions were received
    * payee needs proof that at time of transaction, the majority of nodes
      agreed it was the 1st received

### time-stamp server

* takes a hash of a block of items to be timestamped
  * the hash is widely published
  * proves that the data must have existed at the time
  * each timestamp includes the previous timestamp in its hash
    * this forms a chain
    * each additional timestamp reinforces the ones before it

### proof of work (PoW)

* PoW involves scanning for a value then when hashed
  * the has begins with a number of zero bits
* average work required is exponential in the number of zero bits required
  * can be verified by executing a single hash
* to implement a PoW in a time-stamp server
  * increment a nonce in the block until a value is found that gives the block's
    hash the required zero bits
  * the block cannot be changed without redoing the work
    * as later blocks are chained after it, the work to change the block would
      include redoing all the blocks after it
* PoW solves the problem of determining representation in majority decision
  making
  * Proof-of-work is essentially one-CPU-one-vote
  * majority decision is represented by the longest chain, which has the
    greatest proof-of-work effort invested in it
* to compensate for increasing hardware speed and varying interest in running
  nodes over time
  * proof-of-work difficulty is determined by a moving average targeting an
    average number of blocks per hour
    * if they're generated too fast - difficulty of PoW increases

### network

  1. new transactions are broadcast to all nodes
  2. each node collects new transactions into a block
  3. each node works on finding a difficult proof-of-work for its block
  4. when a node finds a proof-of-work, it broadcasts the block to all nodes
  5. nodes accept the block only if all transactions in it are valid and not
    already spent
  6. nodes express their acceptance of the block by working on creating the next
    block in the chain, using the hash of the accepted block as the previous
    hash
* nodes always accept the longest chain as the correct chain
* if 2 nodes broadcast different versions of the next block simultaneously,
  some nodes may receive one or the other first
  * if this occurs they work on the first one they received the other branch is
    saved in case it becomes longer
  * a tie is broken when the next proof-of-work is found and one branch
      becomes longer
  * nodes that were working on the other branch will then switch to the
      longer one
* if a node does not receive a block, it will request it when it receives the
  next block and realizes it missed one

### incentive

* the 1st transaction in a block is a special transaction
  * this transaction starts a new coin owned by the creator of the block
  * adds an incentive for nodes to support the network
  * provides a way to initially distribute coins into circulation
* incentive can also be funded with transaction fees
  * if the output value of a transaction is less than its input value
    * the difference is a transaction fee that is added to the incentive value
      of the block containing the transaction
    * once a predetermined number of coins have entered circulation
    * the incentive can transition entirely to transaction fees and be
      completely inflation free
* if a malicious attacker is able to assemble more CPU power than all the honest
  nodes (51% attack)
  * attacker would have to choose between using it to defraud others by stealing
    back its previous payments
    * or using the CPU power to generate new coins
  * but it should prove to be more profitable to play by the rules
    * the rules would reward the node with the most CPU power more coins than
      that of everyone else on the chain
    * it is worth more to use all that power to keep generating coins honestly
      by the rules, as it is more profitable than to steal all the other coins
      on the chain

### reclaiming disk space

* disk space is reclaimed without breaking the block's hash
  * transactions are hashed in a Merkle Tree
    * only the root is included in the block's hash
    * old blocks can then be compacted by stubbing off branches of the tree
    * interior hashes do not need to be stored anymore

### payment verification

* a blockchain user only needs to keep a copy of the block headers of the
  longest proof-of-work chain
  * can get this by querying network nodes until convinced the longest chain is
    found
    * also obtaining the Merkle branch linking the transaction to the block it's
      timestamped in
* by linking the transaction to a place in the chain
  * it can be confirmed that a network node has accepted it
  * blocks added after the transactions further confirm that the transaction has
    beed accepted by the blockchain network
* this verification is reliable as long as honest nodes control the network
* this is vulnerable from a 51% attack
* steps to thwart a 51% attack:
  * accept alerts from network nodes when they detect an invalid block
  * prompt the user's software to download the full block and alerted
    transactions - to confirm the inconsistency
* businesses that receive frequent payments will want to run their own nodes
  for more independent security and quicker verification

### combining and splitting value

* coins are not handled individually
  * it would be unwieldy to make a separate transaction for every cent in a
    transfer
* transactions contain multiple inputs and outputs
  * allow value to be split and combined
  * either a single input from a larger previous transaction or multiple inputs
    combining smaller amounts
    * at most 2 outputs
    * 1 for the payment and 1 returning the change (if any) back to the sender

### privacy

* keeping public keys anonymous
  * even with the necessity to announce all transactions publicly,
    privacy can be maintained by breaking the flow of information
  * public can see that someone is sending an amount to someone else
    * without information linking the transaction to anyone
    * model: ```identities | transactions --> public```
    * identities are protected while the transactions are public
  * a new key pair should be used for each transaction
    * this keeps the key pairs from being linked to a common owner
  * some linking inevitable with multi-input transactions
    * multi-point transactions reveal that their inputs were owned by the same
      owner
    * if that owner of a key is revealed, linking can reveal other
      transactions in the blockchain belonging to that same owner
  
### calculations

* the race between the honest chain and an attacker chain
  * if an attacker is tries to generate an alternate chain faster than the
    honest chain
    * it does not throw the system open to arbitrary changes
    * nodes will not accept an invalid transaction as payment
    * honest nodes will never accept a block containing invalid transactions
    * attacker can only try to change one of its own transactions to take back
      money it recently spent
  * Binomial Random Walk
    * success event is the honest chain being extended by one block
      * increasing its lead by +1
      * the failure event is the attacker's chain being extended by 1 block,
        reducing the gap by -1
  * Gambler's Ruin problem
    * a gambler with unlimited credit starts at a deficit and plays potentially
      an infinite number of trials to try to reach breakeven
      * can calculate the probability he ever reaches breakeven or that an
        attacker ever catches up with the honest chain
    * with the odds against him, if he doesn't make a lucky lunge forward early
      on, his chances become vanishingly small as he falls further behind

## notes from _A Next-Generation Smart Contract & Decentralized Application Platform_

### history

* blockchain - a technology tool of distributed consensus

#### Ethereum description

* intends to provide a blockchain with a built-in fully fledged
  Turing-complete programming language that can be used to create "contracts"
  * these contracts can be used to encode arbitrary state transition functions
    * this allows users to create any systems such as:
      * on-blockchain digital assets to represent custom currencies and
        financial instruments (colored coins)
      * the ownership of an underlying physical device (smart property)
      * non-fungible assets such as domain names (Namecoin)
      * other more complex applications involving having digital assets being
        directly controlled by a piece of code implementing smart contracts
      * blockchain-based decentralized autonomous organizations (DAOs)
    * these systems can be created withe ethereum by writing a logic with just
      a few lines of code

#### proof of work

* PoW simultaneously solved 2 problems
  * provides a simple and moderately effective consensus algorithm
    * allows nodes in the network to collectively agree on a set of canonical
      updates to the state of the ledger
  * provides a mechanism for allowing free entry into the consensus process
    * solves the political problem of deciding who gets to influence the
      consensus, while simultaneously preventing sybil attacks
      * substitutes a formal barrier to participation
        * the requirement to be registered as a unique entity on a particular
          list with an economic barrier
        * the weight of a single node in the consensus voting process is
          directly proportional to the computing power of the node

#### proof of stake

* proof of stake is an alternative to PoW
  * calculates the weight of a node as being proportional to its currency
    holdings - not computational resources
  * proof of stake along with PoW can serve as the backbone of a cryptocurrency

### bitcoin as a state transition system

* a cryptocurrency ledger can be thought of as a state transition system
  * a state consists of the following:
    1. the ownership status of all existing bitcoins
    2. a state transition function
       * this function takes a state and a transaction and outputs a new state
       * the new state is the result
  * _simple example:_
    * state is a balance sheet
      * transactions requests to move $x from A to B
      * the state transition function reduces the value in A's account by $x
      * the state transition function also increases the value in B's account
        by $x
      * if A's account is less than $x, the transition function returns an error
    * ```APPLY(S,TX) -> S' or ERROR```
      1. for each input TX:
          * if the referenced UTXO (unspent transaction output) is not in S,
            return an error
          * this prevents transaction senders from spending coins that do not
            exist
          * if the provided signature does not match the owner of the UTXO,
            return an error
          * this prevents transaction senders from spending coins owned by
            others
      2. if the sum of the denominations of all input UTXO is less than the
         sum of the denominations of all output UTXO, return an error
          * enforces conservation of value
      3. return S' with all input UTXO removed and all output UTXO added

    ``` none
    APPLY({ Alice: $50, Bob: $50 }, "send $20 from Alice to Bob") =
    { Alice: $30, Bob: $70 }
    ```

    ``` none
    APPLY({ Alice: $50, Bob: $50 }, "send $70 from Alice to Bob") = ERROR
    ```

* the state in bitcoin is the collection of all unspent transaction outputs
  (UTXO) that have been mined but not spent yet
  * each UTXO has a denomination and an owner
    * this is defined by a cryptographic public key
* a transaction contains one or more inputs
  * each input contains a reference to an existing UTXO and a cryptographic
    signature
  * this cryptographic signature is produced by the private key associated
    with the owner's address and one or more outputs
    * each output contains a new UTXO to be added to the state'

  ``` none
  Alice wants to send 11.7 BTC to Bob
    1. Alice looks for a set of available UTXO that she owns
       - needs to total up to at least 11.7 BTC for the transfer
       - typically a user cannot get an exact amount
       - for example the smallest UTXO Alice can get at this point is
         6 + 4 + 2 = 12
    2. Alice creates a transaction with those 3 inputs and these 2 outputs:
       - 1st output will be 11.7 BTC with Bob's address as its owner
       - 2nd output will be the remaining 0.3 BTC (the change leftover)
         with Alice's address as its owner
  ```

### mining

#### bitcoin

* bitcoin builds a decentralized currency system by combining the state
  transition system with a consensus system
  * this ensures that everyone agrees on the order of transactions
  * requires nodes in the network to continuously attempt to produce packages
    * these packages are called blocks
  * the bitcoin network is intended to produce about 1 block every 10 minutes
    * each block contains:
      * timestamp
      * nonce
      * reference (hash of) the previous block
      * list of all of transactions previously taken place
    * this creates a persistent blockchain which is constantly updating to
      represent the latest state of the bitcoin ledger
* algorithm for checking if a block is valid:
  1. check if the previous block referenced by the block exists and is valid
  2. check that the timestamp of the block is greater than that of the
      previous block and less than 2 hours into the future
  3. check that the proof of work on the block is valid
  4. let ```S[0]``` be the state at the end of the previous block
  5. suppose ```TX``` is the block's transaction list with ```n```
      transactions
      * for all ```i``` in ```0...n-1``` set ```S[i+1] = APPLY(S[i], TX[i])```
      * if any application returns an error, exit and return False
  6. return True and register ```S[n]``` as the state at the end of this block
* each transaction in a block must provide a valid state transition
  * _FROM_ what was the canonical state before the transaction was executed
  * _TO_ some new state
* the state is an abstraction to be remembered by the validating node
  * the state can only be securely computed for any block by starting from
    the genesis state and sequentially applying every transaction in every
    block
  * the state is not encoded in the block in any way
* the order a miner adds transactions into the block has an impact:
  * if 2 transactions A and B in a block such that B spends UTXO created
    by A
  * then the block will be valid only if A comes before B

#### the proof of work condition in bitcoin

* the double-SHA256 hash of every block (treated as a 256-bit number)
  must be less than a dynamically adjusted target
* this makes mining computationally difficult
* prevents sybil attackers from remaking the entire blockchain in their
  favor
  * sybil attack
    * attacker subverts the reputation system of a peer-to-peer network by
      creating a large number of pseudonymous identities
    * the attacker uses these identities are used to gain a
      disproportionately large influence on the system being attacked
    * "51% attack"
* SHA256 is designed to be a completely unpredictable pseudorandom function
  * only way to create a valid block is trial and error
    * repeatedly incrementing the nonce and seeing if the new hash matches
* if the dynamically adjusted target is ~2^187, the network needs to make an
  average of ~2^69 tries before a valid block is found
  * the target is recalibrated by the network every 2016 blocks
  * on an average a new block is produced by some node in the network every
    10 minutes
  * for this computational work (PoW) a miner is compensated 12.5 BTC
    * this 12.5 BTC is newly created bitcoin
  * a miner is also compensated if any transaction has a higher total
    denomination in its inputs than in its outputs
    * the difference is called a _transaction fee_ and it goes to the miner
* the bitcoin genesis state did not contain any coins
  * the only mechanism by which BTC are issued/created is the BTC awarded
    to the miner for a PoW computation
* the order of transactions is the only part of the bitcoin system that is not
  directly protected by cryptography

##### EXAMPLE: order of transactions attack

1. send 100 BTC to a merchant in exchange for some product
   * after a few minutes a miner will include this transaction in a block --
     ```block 270```
   * after around 1 hour, 5 more blocks have been added to the chain after this
     block
     * each of these blocks indirectly point to the transaction and confirm it
     * at this point the merchant will accept the payment as finalized and
       deliver the product
2. wait for the delivery of the product
   * ideally the attacker would choose a rapid-delivery digital good
3. produce another transaction sending the same 100 BTC to himself
   * if this is just released into the wild, the transaction will not process
     * miners will attempt to run ```APPLY(S,TX)```
     * miners will notice that ```TX``` consumes a UTXO which is no longer
      contained in the state
4. try to convince the network that this transaction to himself was the
   transaction that came 1st
   * the attacker creates a _fork_ of the blockchain
     * starts by mining another version of ```block 270``` pointing to the same
       ```block 269``` as a parent but with the new transaction in place of the
       old one
     * the block data is different on this fork and requires a PoW redo
     * the attackers version of ```block 270``` has a different hash
     * the original blocks ```271``` though ```275``` do not point to the
       attacker's version of ```block 270```
   * the rule when there is a fork of the blockchain is to accept the longest
     blockchain as the truth
     * legitimate miners will be working on ```block 275```
     * the attacker will have to catch up from his version of ```block 270```
       * to succeed at this this the attacker would require more computational
         power than the rest of the network combined (_51% attack_)

### Merkle trees

* a block in bitcoin is stored in a multi-level data structure
  * this allows bitcoin to scale
* the hash of a block is only the hash of the block header ~ 200 bytes
  * contains the timestamp, nonce, previous block hash, and the root hash
  * this data structure is known as a Merkle tree
  * all transactions in a block are stored in a Merkle tree
    * a Merkle tree is a binary tree that is composed of:
      * a set of nodes with a large number of leaf nodes at the bottom of the
        tree which contain the underlying data
      * a set of intermediate nodes where each node is the hash of its 2
        children
      * a single root node (top of the tree) formed from the hash of its 2
        children
* a Merkle tree allows for the data in a block to be delivered piecemeal
  * a node can download only the header of a block from one source and the
    small part of the tree relevant to them from another source
    * while still being assured that all of the data is correct
  * this works because hashes propagate upward
    * if a malicious user attempts to swap in a fake transaction into the
      bottom of a Markel tree, the node above will be changed, this error
      propagates up the tree until it changes the root of the tree
      * changing the root changes the hash of the block and the protocol
        registered it as a completely different block

#### simplified payment verification (SPV)

* SPV allows for another class of nodes to exist, called "light nodes"
  * light nodes download the block headers and verify the proof of work on the
    block headers
    * then the light nodes download only the branches associated with
      transactions that are relevant to them
    * this allows for a strong guarantee of security in knowing the status of
      any bitcoin transaction and the current balance while only downloading a
      a very small portion of the entire blockchain

### scripting

* UTXO in Bitcoin can be owned not just by a public key, but also by a more
  complicated script expressed in a simple stack-based programming language
  * a transaction spending that UTXO must provide data that satisfies the
    script
  * the basic public key ownership mechanism is also implemented via a script
  * the script takes an elliptic curve signature as input
    * the script verifies the input against the transaction and the address
      that owns the UTXO
    * then returns 1 if verification is successful or returns 0 if not
* more complicated scripts exist in bitcoin for various additional use cases
* a script can be constructed which requires signatures from 2 out of a given 3
  private keys to validate (this is called a multisig)
  * this is useful for corporate accounts, secure savings accounts, and some
    merchant escrow situations
* scripts can be used to pay bounties for solutions to computational problems
* can construct a script such as the following example:
  > "this Bitcoin UTXO is yours if you can provide an SPV proof that you sent
  > a Dogecoin transaction of this denomination to me"
  * this allows for a decentralized cross-cryptocurrency exchange

#### the scripting language in bitcoin has limitations

##### lack of Turing-completeness

* missing loops
* this leads to scripts that are very inefficient on space

##### value-blindness

* no way for a UTXO script to provide fine-grained control over the amount
  that can be withdrawn
* UTXO are _all-or-nothing_ -- must have many UTXO of varying denominations

##### lack of state

* a UTXO can either be spent or unspent
* no opportunity for multi-stage contracts or scripts which keep any other
  internal state beyond that
* this makes it difficult to create the following:
  * multi-stage option contracts
  * decentralized exchange offers
  * 2-stage cryptographic commitment protocols
    * necessary for secure computational bounties
* UTXO can only be used to build simple one-off contracts and not more complex
  stateful contracts (decentralized organizations)
  * meta-protocols are difficult to implement
* withdrawal limits are impossible because of binary state and value-blindness

##### blockchain-blindness

* UTXO are blind to blockchain data (nonce, timestamp, previous block hash)
* this limits applications in gambling by depriving the scripting language of
  a potentially valuable source of randomness

### Ethereum

* intends to create an alternative protocol for building decentralized
  applications
* Ethereum is a blockchain with a built in Turing-complete programming language
  * allows anyone to write smart contracts and decentralized applications
    * anyone can create their own arbitrary rules for ownership, transaction
      formats, and state transition functions

#### philosophy

##### design

1. _simplicity_
   * the protocol should be as simple as possible
   * an average programmer can ideally be able to follow and implement the
     entire Ethereum specification
   * any optimization which adds complexity should not be included unless that
     optimization provides very substantial benefits
2. _universality_
   * Ethereum does not have features
   * Ethereum provides an internal Turing-complete scripting language
     * programmers can use this scripting language to construct any smart
       contract or transaction type that can be mathematically defined
3. _modularity_
   * parts of the Ethereum protocol should be designed to be as modular and
     separable as possible
   * Etherium development should be maximally done so as to benefit the entire
     cryptocurrency ecosystem
4. _agility_
   * details of the Ethereum protocol are not set in stone
5. _non-discrimination/non-censorship_
   * the protocol does not attempt to actively restrict or prevent specific
     categories of usage
   * all regulatory mechanisms in the protocol should be designed to directly
     regulate the harm and not attempt to oppose specific undesirable
     applications

#### Ethereum accounts

* the state in Ethereum is made up of objects called accounts
  * each account has a 20-byte address
  * state transitions are direct transfers of value and information between
    accounts
  * contents of an account:
    * nonce - a counter used to make sure each transaction can only be
      processed once
    * the current ether balance of the account
    * contract code for the account (optional)
    * storage for the account (empty by default)

##### Ether

* ether is the main internal "crypto-fuel" of Ethereum
* used to pay transaction fees
* there are 2 types of accounts:
  1. externally owned accounts
     * these accounts are controlled by private keys
     * contains no code
     * messages can be sent from an externally owned account by creating and
       signing a transaction
  2. contract accounts
     * these accounts are controlled by their contract code
     * every time the contract account receives a message its code activates
       * this allows for reading and writing to internal storage, sending other
         messages, and creating other contracts in succession
* contracts in Ethereum are not to be fulfilled or complied with
  * contracts act as autonomous agents that live inside the Ethereum execution
    environment
  * contracts always execute a specific piece of code when they are poked by a
    message or transaction
  * contracts have direct control over their own ether balance and their own
    key/value store in order to keep track of persistent variables

#### messages and transactions

* a transaction is a signed data package that stores a message to be sent from
  an externally owned account
* transactions contain the following:
  1. the recipient of the message
  2. a signature identifying the sender
  3. the amount of ether to transfer from the sender to the recipient
  4. data field (optional)
     * virtual machine has an opcode which a contract can use to access the data
     * _example:_
       * if a contact is functioning as an on-blockchain domain registration
         service
       * the contact could interpret the data being passed to it as containing
         2 fields
         * 1st field is a domain to register
         * 2nd field is the IP address to register to the domain
       * the contract reads these values from the message data and appropriately
         places them into storage
  5. a ```STARTGAS``` value
     * this represents the maximum number of computational steps the transaction
       execution is allowed to take
  6. a ```GASPRICE``` value
     * this represents the fee the sender pays per computational step
* to prevent accidental or hostile infinite loops (or other computational waste)
  each transaction is required to set a limit to how many computational steps of
  code execution it can use
  * the fundamental unit of computation is ```gas```
  * typically a computational step costs 1 ```gas```
    * some more computationally expensive operations cost higher amounts of
      ```gas```
    * there is a fee of 5 ```gas``` per byte in the transaction data
      * this fee systems is implemented to that an attacker would have to pay
        proportionately for every resource that they consume

#### messages

* contracts have the ability to send messages to other contracts
* messages are virtual objects that are never serialized
* messages only exist in the Ethereum execution environment
* message contents:
  1. sender of the message (implicit)
  2. recipient of the message
  3. amount of ether to transfer alongside the message
  4. data field (optional)
  5. a ```STARTGAS``` value
* a message is like a transaction that is produced by a contract instead of an
  external actor
* a message is produced when a contract is executing code and the ```CALL```
  opcode is executed
  * this produces and executes a message
* a message leads to the recipient account running its code
* contracts can have relationships with other contracts
* the ```gas``` allowance assigned by a transaction or contract applies to the
  total ```gas``` consumed by that transaction and all sub-executions
  * _example:_
    * external actor A sends a transaction to B with 1000 gas
    * and B consumes 600 gas before sending a message to C
    * and the internal execution of C consumes 300 gas before returning
    * then B can spend another 100 gas before running out of gas

#### Ethereum state transition function

```APPLY(S,TX) -> S'```
* definition:
  1. check if transaction is well-formed (correct number of values), has a valid
     signature, and the nonce matches the nonce in the sender's account
     * if nonce does not match then return an ```error```
  2. calculate transaction fee as ```STARTGAS * GASPRICE```
     * determine the sending address from the signature
     * subtract the fee from the sender's account balance
     * increment the sender's nonce
     * if there is not enough balance to spend then return an ```error```
  3. initialize ```GAS = STARTGAS```
     * take off a certain quantity of ```gas``` per byte to pay for the bytes in
       the transaction
  4. transfer the transaction value from the sender's account to the receiving
     account
     * if receiving account does not yet exist then create it
     * if receiving account is a contract then run the contract's code
       * the contract's code runs to completion or until the execution runs out
         of ```gas```
  5. if the value transfer failed because the sender did not have enough funds
     or the code execution ran out of gas then revert all state changes except the payment of the fees
     * add these fees to the miner's account
  6. otherwise, refund the fees for all remaining gas to the sender
     * send the fees paid for ```gas``` consumed to the miner

  * _contract code example:_
    * written in Serpent (an Ethereum high-level language)

    ``` Serpent
    if !self.storage[calldataload(0)]:
        self.storage[calldataload(0)] = calldataload(32)
    ```
  
  * contract code is actually written in low-level EVM code
  * _example:_
    * the contract's code starts empty
    * a transaction is sent containing:
      * 10 ether value
      * 2000 gas
      * 0.001 ether gasprice
      * 64 bytes of data
        * bytes 0 - 31 representing the number ```2```
        * bytes 32 - 63 representing the string ```CHARLIE```
    * process for the state transition function:
      1. check that the transaction is valid and well formed
      2. check that the transaction sender has at least 2 ether
         (2000 gas * 0.001 ether gasprice)
         * if True then subtract 2 ether from the sender's account
      3. initialize gas = 2000
         * if transaction is 170 bytes long and the byte-fee is 5
           then subtract 850 gas = 1150 gas left over
      4. subract 10 more ether from the sender's account
         add this ether to the contract's account
      5. run the code
         * code checks if the contract's storage at index ```2``` is used or not
         * code notices that index ```2``` is not used
         * then code sets the storage at index ```2``` to the value
           ```CHARLIE```
         * this takes 187 gas
         * remaining amount of gas is 963 (1150 gas - 187 gas)
      6. add 0.963 ether (963 gas * 0.001 gasprice) back to the sender's account
         * then returns the resulting state
      * if no contract at the receiving end of the transaction
        * then the total transaction fee is equal to the provided ```GASPRICE```
          multiplied by the length of the transaction in bytes
        * the data sent with the transaction is irrelevant
* if a message execution runs out of gas, then that message's execution, and all
  other executions triggered by that execution, revert
  * parent executions do not need to revert
  * this makes it safe for a contract to call another contract
    * _example:_
      * if A calls B with G gass
      * then A's execution is guaranteed to lose as most G gas
* the opcode ```CREATE``` creates a contract
  * the execution mechanics of ```CREATE``` are similar to ```CALL```
    * except that the output of the execution determines the code of a newly
      created contract
  
#### code execution

* Ethereum contracts are written in Ethereum Virtual Machine code (EVM code)
  * EVM code is a low-level stack-based bytecode language
    * it consists of a series of bytes
    * each byte represents an operation
* code execution is an infinite loop that consists of repeatedly carrying out
  the operation at the current program counter
  * the counter begins at 0
* then incrementing the program counter by 1 until the end of the code is
  reached, an error occurs, or a ```STOP``` or ```RETURN``` instruction is
  detected

##### operations have access to 3 types of space to store data

  1. the stack
     * last-in-first-out container
     * values can be pushed and popped
     * this data store resets after computation ends
  2. memory
     * infinitely expandable byte array
     * this data store resets after computation ends
  3. the contract's long-term storage
     * a key/value store
     * this data store persists

* code can access the value, sender, and data of the incoming message
* code can access block header data
* code can return a byte array of data as an output

##### execution model of EVM code

* while the Ethereum virtual machine is running the full computational state is
  defined by:
  * the tuple:
  
    ``` none
    (block_state, transaction, message, code, memory, stack, pc, gas)
    ```

  * ```block_state``` is the global state containing all accounts
    * includes balances and storage
  * at the start of every round of execution, current instruction is found by:
    * taking the ```pc```-th byte of ```code``` (or 0 if ```pc >= len(code)```)
    * each instruction has its own definition
      (in terms of how it affects the tuple)
    * _example:_
      * ```ADD``` pops 2 items off the stack and pushes their sum
        * reduces ```gas``` by 1
        * increments ```pc``` by 1
      * ```SSTORE``` pops the top 2 items off the stack
        * inserts the 2nd item into the contract's storage at the index specified by the 1st item

#### blockchain and mining

* the bitcoin blockchain only contains a copy of the transaction list
* Ethereum blocks contain a copy of the transaction list and the most recent
  state
  * the block number as well as the difficulty are stored in a block

##### basic validation algorithm in Ethereum

1. check if the previous block referenced exists and is valid
2. check the timestamp of the block is greater than that of the referenced block
   and less then 15 minutes into the future
3. check the block number, difficulty, transacrion root, uncle root, and gas
   limit are valid
4. check that the PoW on the block is valid
5. let ```S[0]``` be the state at the end of the previous block
6. let ```TX``` be the block's transaction list with ```n``` transactions
   * for all ```i``` in ```0...n-1``` set ```S[i+1] = APPLY(S[i],TX[i])```
   * if any applications return an error or if the total gas consumed in the
     block up until this point exceeds the ```GASLIMIT``` then return an error
7. let ```S_FINAL```  be ```S[n]```
   * add the block reward paid to the miner
8. check if the Merkle tree root of the state ```S_FINAL``` is equal to the final
   state root provided in the block header
   * if it is equal, then the block is valid
   * if it is not equal, then it is invalid
* the state is stored in the tree structure
  * after every block only a small part of the tree needs to be changed
  * the vast majority of the tree should be the same between 2 adjacent blocks
    * this allows data to be stored once and referenced twice using a
      **_Patricia tree_**
      * this uses pointers which are hashes of subtrees
      * it is a modification to the Merkle tree concept that allows for nodes to
        be inserted and deleted efficiently
* all state information is part of the last block
  * no need to store the entire blockchain history
* the process of executing contract code is part of the definition of the state
  transition function
  * the state transition function is part of the block validation algorithm
  * if a transaction is added into block ```B```
  * the code execution spawned by that transaction will be executed by all nodes
    (now and in future) that download and validate block ```B```
