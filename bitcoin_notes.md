# notes from _Bitcoin: A Peer-to-Peer Electronic Cash System_

* by Satoshi Nakamoto ~ 2008

## transactions

* electronic coin is defined as a chain of digital signatures
  * coin is transferred from one owner to the next:
    * digitally sign a hash of the previous transaction and the public key of
      the new owner
    * add this hash to the end of the coin
  * payee can verify the signatures to verify the chain of ownership

## double-spend problem

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

## time-stamp server

* takes a hash of a block of items to be timestamped
  * the hash is widely published
  * proves that the data must have existed at the time
  * each timestamp includes the previous timestamp in its hash
    * this forms a chain
    * each additional timestamp reinforces the ones before it

## proof of work (PoW)

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

## network

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

## incentive

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

## reclaiming disk space

* disk space is reclaimed without breaking the block's hash
  * transactions are hashed in a Merkle Tree
    * only the root is included in the block's hash
    * old blocks can then be compacted by stubbing off branches of the tree
    * interior hashes do not need to be stored anymore

## payment verification

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

## combining and splitting value

* coins are not handled individually
  * it would be unwieldy to make a separate transaction for every cent in a
    transfer
* transactions contain multiple inputs and outputs
  * allow value to be split and combined
  * either a single input from a larger previous transaction or multiple inputs
    combining smaller amounts
    * at most 2 outputs
    * 1 for the payment and 1 returning the change (if any) back to the sender

## privacy

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
  
## calculations

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
