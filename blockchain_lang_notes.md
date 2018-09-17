# notes from _Blockchain Coding: The Many different Languages You Need!_

* <https://blockgeeks.com/guides/blockchain-coding/>

## performance

* some tasks in the blockchain are parallelizable and some are not
  * example of a parallelizable task - digital signature verification
    * key, transaction, and signature are need for a signature verification
    * verifications can be conducted in a parallelized manner
  * transaction execution
    * multiple transactions cannot be executed in parallel
      * needs to be one at a time - this avoids errors such as double spends
* certain programming languages are proficient at parallel operations and
  other languages are better at non-parallel operations

## isolation

* deterministic behavior
  * if ```A + B = C``` - then ```A + B``` will always be ```=``` to ```C```
  * hash functions are deterministic
    * ```A```'s hash will always be ```H(A)```
* all transaction operations must be deterministic
  * there cannot be a transaction that behaves one way then behaves another way
    at another point in time
  * smart contracts cannot work in two different ways in two different machines
* isolate smart contracts and transactions from non-deterministic elements

## C++

* in C++ - the data functions are wrapped into 1 small package caled objects
  * once an object is created it can easily be called and reused in other
    programs
    * this reduces coding time

### memory control

* effective resource management
* a blockchain interacts with a many untrusted endpoints and provides fast
  service to all nodes
* cryptocurrency is based on the principle of consensus
  * all nodes on the network must accept and reject the exact same blocks
* C++ allows for tight and complete control over CPU and memory usage

### threading

* C++'s threading ability can efficiently handle both parallel and non-parallel
  tasks
  * a thread is a set of instructions that can be executed simultaneously
* C++ allows for effective multithreading facilities with inter-thread
  communication - while optimizing single thread performance

### move semantics

* provides a way for the contents to be moved between objects rather than being
  copied outright

#### differences between copy semantics and move semantics:

* copy semantics:
  * ```assert(b == c);```
  * ```a = b;```
  * ```assert(a == b && b == c);```
  * the value of ```b``` goes into ```a``` and ```b``` remains unchanged at
    the end

* move semantics:
  * ```assert(b == c);```
  * ```move(a,b);```
  * ```assert(a == c);```
  * the value of ```b``` is replaced with ```a```
    * "the value of “b” need not be the unchanged"
  * advantage of move semantics - you can get copies of certain data only when
    you need them
  * decreases redundancy in the code and gives a performance boost

* efficient memory management and high performance

### compile time polymorphism

* polymorphism is an object oriented programming property
  * in C++ polymorphism can be used at compile time or run time

#### 2 ways C++ implements compile time polymorphism

##### function overloading

* many functions of the same name but each has a different parameter intake

``` C++
#include <bits/stdc++.h>
using namespace std;

class A
    {
        // first instance of the function takes only one integer value
        void func (int x)
        { cout<<x<<endl; }

        // second instance of the function takes only one double value
        void func (double x)
        { cout<<x<<endl; }

        // third instance of the function takes two integer values
        void func (int x, int y)
        { cout<<x=y<<endl; }
    }

int main()
    {
        //making one object of the class A
        A obj1

        //now we are going to call the functions
        obj1.func(2);
        obj1.func(2.65);
        obj1.func(2,5);

        return 0;
    }
 ```

* when the above function is run - it outputs the following:
  * 2
  * 2.65
  * 7
* the same ```func()``` was used 3 different ways

##### operator overloading

* the same operator can more than one meaning
  * ```+``` can be used for both mathematical addition and concatenation
* polymorphism helps with dividing responsibilities between various functions
  * this helps with performance

### code isolation

* C++ namespace features can be imported from one program to another
  * namesapce helps in avoiding collisions
  * classes can act as boundaries between various APIs - clear separation
  * classes are either a user defined type or data structure which are declared
    with a keyword class
    * a class contains data and functions as its members
    * functions can be accessed by declaring objects of the particular class

## javascript

* blockchain - a chain of blocks that contain data
  * a linked list
  * immutable - data goes into a black and cannot be changed
* each block is connected to teh previous block with a hash pointer
  * this hash pointer contains the hash of the previous block

### to construct a block

#### contents

* index - the block's number in the chain
* timestamp - time of the block's creation
* data - data contained in the block
* previous hash - hash of the subsequent block in the chain
* hash - the hash of this block

#### javascript blockchain

* ```this``` keyword invoked inside a function enables access to values
  contained inside a specific object which calls that particular function
* a contructor is a special function which helps create and initialize an object
  within a class
  * each class is restricted to 1 constructor

* below is an example of an out block:

``` javascript
    // call the crypto-js library for the sha256 function
    const SHA256 = require("crypto-js/sha256");

    // invoke a constructor inside class Block
    // calls objects that have certain values
    class Block
    {
        constructor(index, timestamp, data, previousHash = '')
            {
                this.index = index;
                this.previousHash = previousHash;
                this.timestamp = timestamp;
                this.data = data;
                this.hash = this.calculateHash();
            }

        // turn the block data into a string and hash it
        calculateHash()
            {
                return SHA256(this.index + this.previousHash + this.timestamp +
                              JSON.stringify(this.data)).toString();
            }
    }
```

* create the blockchain:

``` javascript
    class Blockchain
    {
        // section 1 genesis block creation:
        // invoked immediately when a new chain is crested
        constructor()
        {
            this.chain = [this.createGenesisBlock()];
        }

        createGenesisBlock()
        {
            return new Block(0, "01/01/2017", "Genesis block", "0");
        }

        // section 2 adding new blocks:
        getLatestBlock() //must 1st find the latest block in the chain
        {
            return this.chain[this.chain.length - 1];
        }

        // compare the previous hash value to the new block with the hash value
        // of the latest block
        // if these 2 values match - the new block is legit and gets added to
        // the blockchain
        addBlock(newBlock)
        {
            newBlock.previousHash = this.getLatestBlock().hash;
            newBlock.hash = newBlock.calculateHash();
            this.chain.push(newBlock);
        }

        // section 3 validating the chain:
        // check that the chain is correct and stable
        // iterate from the current block to the genesis block
        // if the previous hash of the current block is not equal to the hash of
        // the previous block - return false
        isChainValid()
        {
            for (let i = 1; i < this.chain.length; i++)
            {
                const currentBlock = this.chain[i];
                const previousBlock = this.chain[i - 1];

                if (currentBlock.hash !== currentBlock.calculateHash())
                {
                    return false;
                }

                if (currentBlock.previousHash !== previousBlock.hash)
                {
                    return false;
                }
            }
                return true;
        }
    }
```

* create coins in the blockchain:

``` javascript
    // invoke a new object and activate the constructor
    // the constructor 1st creates the genesis block
    let BlockGeeksCoin = new Blockchain();

    // after the genesis block is created the other blocks may be added
    BlockGeekCoin.addBlock(new Block(1, "20/07/2017", { amount: 4 }));
    BlockGeekCoin.addBlock(new Block(2, "20/07/2017", { amount: 8 }));
```

## python