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

#### polymorphism

* polymorphism is an object oriented programming property
  * in C++ polymorphism can be used at compile time or run time
* 2 ways C++ implements compile time polymorphism:
  1. function overloading
     * many functions of the same name but each has a different parameter intake

     ``` C++
     #include <bits/stdc++.h>
     using namespace std;

     class A
     {
         void func (int x) //1st instance of the function takes only 1 int value
         {
             count<<x<<end1;
         }
         void func (double x) // 2nd instance of the function takes only 1 double value
         {
             count<<x<<endl;
         }
         
     }
     ```

  2. operator overloading