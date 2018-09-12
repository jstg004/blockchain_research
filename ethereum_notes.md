# notes from _A Next-Generation Smart Contract & Decentralized Application Platform_

## history

* blockchain - a technology tool of distributed consensus

### Ethereum description

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
    * these systems can be created with Ethereum by writing a logic with just
      a few lines of code

### proof of work

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

### proof of stake

* proof of stake is an alternative to PoW
  * calculates the weight of a node as being proportional to its currency
    holdings - not computational resources
  * proof of stake along with PoW can serve as the backbone of a cryptocurrency

## bitcoin as a state transition system

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

## mining

### bitcoin

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

### the proof of work condition in bitcoin

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

#### EXAMPLE: order of transactions attack

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

## Merkle trees

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
      bottom of a Merkle tree, the node above will be changed, this error
      propagates up the tree until it changes the root of the tree
      * changing the root changes the hash of the block and the protocol
        registered it as a completely different block

### simplified payment verification (SPV)

* SPV allows for another class of nodes to exist, called "light nodes"
  * light nodes download the block headers and verify the proof of work on the
    block headers
    * then the light nodes download only the branches associated with
      transactions that are relevant to them
    * this allows for a strong guarantee of security in knowing the status of
      any bitcoin transaction and the current balance while only downloading a
      a very small portion of the entire blockchain

## scripting

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

### the scripting language in bitcoin has limitations

#### lack of Turing-completeness

* missing loops
* this leads to scripts that are very inefficient on space

#### value-blindness

* no way for a UTXO script to provide fine-grained control over the amount
  that can be withdrawn
* UTXO are _all-or-nothing_ -- must have many UTXO of varying denominations

#### lack of state

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

#### blockchain-blindness

* UTXO are blind to blockchain data (nonce, timestamp, previous block hash)
* this limits applications in gambling by depriving the scripting language of
  a potentially valuable source of randomness

## Ethereum

* intends to create an alternative protocol for building decentralized
  applications
* Ethereum is a blockchain with a built in Turing-complete programming language
  * allows anyone to write smart contracts and decentralized applications
    * anyone can create their own arbitrary rules for ownership, transaction
      formats, and state transition functions

### philosophy

#### design

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
   * Ethereum development should be maximally done so as to benefit the entire
     cryptocurrency ecosystem
4. _agility_
   * details of the Ethereum protocol are not set in stone
5. _non-discrimination/non-censorship_
   * the protocol does not attempt to actively restrict or prevent specific
     categories of usage
   * all regulatory mechanisms in the protocol should be designed to directly
     regulate the harm and not attempt to oppose specific undesirable
     applications

### Ethereum accounts

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

#### Ether

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

### messages and transactions

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

### messages

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

### Ethereum state transition function

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
      4. subtract 10 more ether from the sender's account
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
      * if A calls B with G gas
      * then A's execution is guaranteed to lose as most G gas
* the opcode ```CREATE``` creates a contract
  * the execution mechanics of ```CREATE``` are similar to ```CALL```
    * except that the output of the execution determines the code of a newly
      created contract
  
### code execution

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

#### operations have access to 3 types of space to store data

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

#### execution model of EVM code

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

### blockchain and mining

* the bitcoin blockchain only contains a copy of the transaction list
* Ethereum blocks contain a copy of the transaction list and the most recent
  state
  * the block number as well as the difficulty are stored in a block

#### basic validation algorithm in Ethereum

1. check if the previous block referenced exists and is valid
2. check the timestamp of the block is greater than that of the referenced block
   and less then 15 minutes into the future
3. check the block number, difficulty, transaction root, uncle root, and gas
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

### applications

* 3 types of applications on top of Ethereum
  1. financial applications
     * provides users with more powerful ways of managing and entering into
       contracts using their money
     * financial derivatives, hedging contracts, savings wallets, wills
  2. semi-financial applications
     * money is involved but there is also a heavy non-monetary side to what is
       being done
     * such as self-enforcing bounties for solutions to computational problems
  3. non-financial
     * online voting and decentralized governance

#### token systems

* a currency/token system is a database with 1 operation:
  * subtract X units from A and give X units to B
    * A must have at least X units before the transaction
    * the transaction must be approved by A
  * basic code for implementing a token system in Serpent code:

    ``` Serpent
    def send(to, value):
        if self.storage[msg.sender] >= value:
            self.storage[msg.sender] = self.storage[msg.sender] - value
            self.storage[to] = self.storage[to] + value
    ```
    * this is a literal implementation of the banking system state function

#### financial derivatives and stable-value currencies

* financial derivatives are the most common application of smart contracts
  * typically require reference to external price ticker
    * hedging against the volatility of a cryptocurrency in respect to US dollar
  * need to do this through a data feed maintained by a specific party
    * this provides and interface that allows other contracts to send a message
      to that contract and get back a response that provides the price
  * _hedging contract_ _example:_
    1. wait for party A to input 1000 ether
    2. wait for party B to input 1000 ether
    3. record the USD value of 1000 ether
       * calculated by querying the data feed contract ($x)
    4. after 30 days, allow A or B to reactivate the contract in order to send
       $x worth of ether to A and the rest to B
       * calculated by querying the data feed contract again, updated conversion
* the above type of contract allows any non-cryptographic asset to be uplifted
  into a cryptographic asset - if user can be trusted
  * still have to rely on a trusted party?
* issuers are not alway trustworthy
* banking system can be too weak
* a decentralized market of speculators bet that the price of a cryptographic
  reference asset (like ETH) will go up
  * this provides the role of funds to backup an asset
  * hedging contract holds their funds in escrow
  * this os not fully decentralized
    * a trusted source is required for the price tracker

#### identity and reputation systems

* _namecoin-like_ _contract_ _example:_

  ''' none
  def register(name, value):
      if !self.storage[name]:
          self.storage[name] = value
  '''

  * the above example is a database inside the Ethereum network that can be
    added to, but not modified or removed from

#### decentralized file storage

* Ethereum contracts can allow for development of decentralized file storage
  * individuals users can earn small quantities of money by renting out their own hard drives and unused space
  * _example:_
    1. the contract splits the desired data up into blocks
       * each block is encrypted
    2. a Merkle tree is built out of the data
    3. a contract is created with the rule that every N blocks the contract
      picks a random index in the Merkle tree
       * the source of randomness is the previous block hash, accessible from
         contract code
    4. give X ether to the 1st entity to supply a transaction with a simplified
       payment verification-like proof of ownership of the block at that
       specific index in the tree
    5. when a user wants to re-download their file, they use a micropayment
       channel protocol to recover the file
* -- I do not see this being practical without all data being almost everywhere       and the cryptography being really really good. --

#### decentralized autonomous organizations (DAO)

* a virtual entity that has a certain set of members or shareholders have the
  right to spend the entity's funds and modify its code
* members collectively decide how the organization allocates its funds
* a piece of self-modifying code that changes only if 2/3rds of members agree
  on a change
  * de-facto mutability is achived by having chunks of the code in separate
    contracts
    * the address of which contracts to call stored in modifiable storage
* there are 3 different transaction types distinguished by the data provided
  in the transaction
  1. ```[0,i,K,V]``` to register a proposal with index ```i``` to change the
     address at storage index ```K``` to value ```V```
  2. ```[1,i]``` to register a vote in favor of proposal ```i```
  3. if enough votes in favor, then ```[2,i]``` to finalize proposal ```i```
  * the contract has clauses for each of these
    * maintains records of all open storage changes and a list of who voted for
      them
    * maintains a list of all members
  * when any storage change gets 2/3rds of the vote, a finalizing transaction
    executes the change
* liquid democracy vote delegation:
  * anyone can assign someone to vote for them
  * alows DAO to grow organically
  * -- To me this sounds like it could cause a lot of issues. --

### Greedy Heaviest Observed Subtree (GHOST) protocol

* blockchains with fast confirmation times suffer from reduced security due to
  high stale rate
  * blocks take a certain time to propagate throught he network
  * if miner A mins a block and then miner B mines another block before miner
    A's block propagates to B, miner B's blocks end up wasted and will not
    contribute to network security 
* centralization issue:
  * if miner A is a mining pool with 30% hashpower and B has 10% hashpower,
    miner A will have a risk of producing a stale block 70% of the time
    * B will have the risk of producing a stale block 90% of the time
    * if block is short enough for the stale rate to be high, A will be
      substantially more efficient by virue of its size
* GHOST seeks to solve this by including stale blocks in the calculation of
  which chain is the longest
  * the parent and further ancestors of a block and the stale descendants of
    the block's ancestor are added to the calculation of which blocks has the
    largest total proof of work backing it
  * Ethereum also provides block rewards to stales
    * a stale block receives 87.5% of its base reward
    * the nephew block that includes the stale block receives the remaining
      12.5%
    * transaction fees are not awarded to uncles
* in Ethereum the GHOST protocol only goes down 7 levels and is defined as:
  * a block must specify a parent and must specify 0 or more uncles
  * an uncle included in block ```B``` must have the following properties:
    * must be a direct child of the ```k```-th generation ancestor of ```B```
      where ```2 <= k <= 7```
    * cannot be an ancestor of ```B```
    * uncle must be a valid block header
    * uncle must be different from all uncles included in previous blocks
      * all other uncles included in the same block (non-double-inclusion)
  * for every uncle ```U``` in block ```B``` gets an addtional 3.125% added to
    its coinbase reward
    * the miner U gets 93.75% of a standard coinbase reward

### fees

* every transaction published into the blockchain imposes on the network the
  cost of needed to download and verify it
  * there is a need for a regulatory mechanism to prevent abuse
    * this typically involves transaction fees
* bitcoin has voluntary fees
  * miners act as the gatekeepers and set dynamic minimums
  * supply and demand between miners and transaction senders determine the price
  * every transaction that a miner includes will need to be processed by every
    node in the network
    * majority of the cost of transaction processing ir created by 1rd parties
    * this can be canceled out:
      1. a transaction leads to ```k``` operations, offering the reward ```kR```
         to any miner that includes it where ```R``` is set by the sender and
         ```k``` and ```R``` are visible to the miner beforehand
      2. an operation has a processing cost of ```C``` to any node
         * all nodes have equal efficiency
      3. ```N``` mining nodes, each with exactly equal processing power
      4. no non-mining full nodes exist
      * a miner would be willing to process a transaction if the expected reward
        is greater than the cost
      * expected reward is ```kR/N```
        * miner has ```1/N``` chance of processing the next block
      * processing cost for the miner is ```kC```
      * miners will include transactions where ```kR/N > kC``` or ```R > NC```
        * ```R``` is the per-operation fee provided by the sender
        * ```NC``` is the cost to the entire network together of processing an
          operation
      * miners have the incentive to include only those transactions for which
        total utilitarian benefit exceeds the cost
    * deviations from the above assumptions:
      1. miner pays a higher cost to process the transaction than the other
         verifying nodes
         * extra verification time delays block propagation - increases chances
           the block will become a stale
         * provides a tendency for the miner to include fewer transactions
      2. non-mining full nodes exist
         * increases ```NC```
      3. mining power distribution may end up radically inegalitarian in
         practice
      4. malicious actors can set up contracts where their cost is much lower
         than the cost paid by other verifying nodes
      * #1 and #2 cancel eachother out
      * to solve the issues in #3 and #4a floating cap is implemented
        * no block can have more operations than ```BLK_LIMIT_FACTOR``` times
          the long-term exponential moving average

          ``` none
          blk.oplimit = floor((blk.parent.oplimit * (EMAFACTOR - 1) +
              floor(parent.opcount + BLK_LIMIT_FACTOR))) / EMA_FACTOR)
          ```

          * ```BLK_LIMIT_FACTOR``` and ```EMA_FACTOR``` are constants that will
            be set to 65536 and 1.5, but can change
* in bitcoin larger blocks take longer to propagate
  * larger blocks have a higher probability of becoming stales
* in Ethereum highly gas-consuming blocks can also take longer to propagate
  * physically larger
  * take longer to process the transaction state transitions to validate

### computing and Turing-completeness

* EVM code can encode any computation that can be conceivably caried out
* EVM allows looping in 2 ways:
  1. ```JUMP``` instruction aloows the program to jump back to a previous spot
     in the code
     * ```JUMPI``` instruction performs conditional jumping
       * allows for statements like: ```while x < 27: x = x * 2```
  2. contracts can call other contracts
     * this could cause a halting problem
  * solution requires a transaction to set a max number of computational steps
    * if execution take s longer, then computation is reverted but fees are
      still paid