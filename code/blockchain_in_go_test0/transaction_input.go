// my notes for this tutorial:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-1/

package main

import "bytes"

// every transaction must have at least one input and one output
// the input references an output from a previous transaction
// the input provides data used in the output's unlocking script to unlock
//    the output and use the output's value to create new outputs
// inputs produce outputs - then the outputs make inputs possible

// TXInput represents a transaction input
type TXInput struct {
	Txid      []byte // transaction ID
	Vout      int // index of an output in the transaction
	Signature []byte
	PubKey    []byte
}

// UsesKey checks whether the address initiated the transaction
//    - input uses a specific key to unlock an output
func (in *TXInput) UsesKey(pubKeyHash []byte) bool {
	lockingHash := HashPubKey(in.PubKey)

	return bytes.Compare(lockingHash, pubKeyHash) == 0
}
