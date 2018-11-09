// my notes for this tutorial:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-1/

package main

import (
	"log"

	"github.com/boltdb/bolt"
)

// BlockchainIterator is used to iterate over blockchain blocks
// BoltDB allows for iteration over all the keys in a bucket
// keys are stored in byte-sorted order
// create a blockchain iterator to read each block in the chain one by one
type BlockchainIterator struct {
	currentHash []byte
	db          *bolt.DB
}
// the above iterator will be created everytime we want to iterate over blocks

// Next returns next block starting from the tip
//    in a blockchain
// the iterator will store the block hash of the current iteration
// the iterator will store a connection to a db
// the iterator is logically attached to the blockchain
//   - a blockchain instance which stores a db connection

// the iterator initially points to the tip of the blockchain
//  - blocks are obtained from the top to the bottom (newest - oldest)
//  - if a blockchain has multiple branches
//    - the longest blockchain is the main chain
//  - a tip can be any block in the blockchain
//    - the entire blockchain can be reconstructed and length can be calculated
//    - the work required to build the block chain can also be calculated
//  - a tip is a type of identifier of a blockchain

// the BlockchainIterator returns the next block from a blockchain
func (i *BlockchainIterator) Next() *Block {
	var block *Block

	err := i.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(blocksBucket))
		encodedBlock := b.Get(i.currentHash)
		block = DeserializeBlock(encodedBlock)

		return nil
	})

	if err != nil {
		log.Panic(err)
	}

	i.currentHash = block.PrevBlockHash

	return block
}
