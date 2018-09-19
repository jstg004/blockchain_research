// my notes for this tutorial:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-1/

package main

import (
	"bytes"
	"encoding/gob"
	"log"
	"time"
)

// a blockchain is a database with an ordered structure - a back-linked list
// blocks are stored in the insertion order and each block is linked to the
//     previous block
// this is implemented using an array and a map
// the array keeps ordered hashes
// the map keeps hash block - pairs
// Block represents a block in the blockchain
type Block struct {
	Timestamp     int64 //current timestamp when block is crated
	Transactions  []*Transaction
	PrevBlockHash []byte //hash of the previous block
	Hash          []byte
	Nonce         int
	Height        int
}

// NewBlock creates and returns Block
func NewBlock(transactions []*Transaction, prevBlockHash []byte, height int) *Block {
	block := &Block{time.Now().Unix(), transactions, prevBlockHash, []byte{}, 0, height}
	pow := NewProofOfWork(block)
	nonce, hash := pow.Run()

	block.Hash = hash[:]
	block.Nonce = nonce

	return block
}

// NewGenesisBlock creates and returns genesis Block
func NewGenesisBlock(coinbase *Transaction) *Block {
	return NewBlock([]*Transaction{coinbase}, []byte{}, 0)
}

// HashTransactions returns a hash of the transactions in the block
func (b *Block) HashTransactions() []byte {
	var transactions [][]byte

	for _, tx := range b.Transactions {
		transactions = append(transactions, tx.Serialize())
	}
	mTree := NewMerkleTree(transactions)

	return mTree.RootNode.Data
}

// uses encoding/gob to serialize the block structs
func (b *Block) Serialize() []byte {
	var result bytes.Buffer //declare a buffer that stores the serialized data
	encoder := gob.NewEncoder(&result) //initialize gob encoder & encode block

	err := encoder.Encode(b)
	if err != nil {
		log.Panic(err)
	}

	return result.Bytes() //a byte array is returned
}

// this deserializing function receives the byte array as input and returns
//    a block as the output
func DeserializeBlock(d []byte) *Block {
	var block Block

	decoder := gob.NewDecoder(bytes.NewReader(d))
	err := decoder.Decode(&block)
	if err != nil {
		log.Panic(err)
	}

	return &block
}
