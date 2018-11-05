// my notes for this tutorial:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-1/

// Simplified Payment Verification (SPV) - light Bitcoin node
//    - does not downlowd the entire blockchain
//    - does not verify blocks and transactions
//    - finds transactions in blocks (to verify payments)
//    - the SPV is linked to a full node for retrieval of required data
//    - multiple light wallet nodes run from only 1 full node
//    - needs a way to check if a block contains a certain transaction without
//        downloading the entire block

// Merkle trees are used to obtain a transactions hash - then saved in block
//    headers - considered by the PoW system
// each block has a Merkle tree built for it
// tree starts at the bottom (leaves - this is a hash)
// double SHA256 hashing is used
// the number of leaves must be even
//    - if there is an odd number of transactions then the last transaction is
//      duplicated in the Merkle tree
// moving from bottom up:
//    - leaves are grouped in pairs
//    - the hashes of the leave groups are concatenated
//    - a new hash is obtained from the concatenated hashes
//    - new hashes form new tree nodes
// the above process is repeated until there is only 1 node - Merkle tree root
// root hash is used as the unique representation fo the transactions
//    - saved in block headers - used in the PoW system

// with a Merkle tree - a node can verify membership of a certain transaction
//    without downloading the entire block
// - only required data: transaction hash, Merkle tree root hash, Merkle path


package main

import (
	"crypto/sha256"
)

// MerkleTree represent a Merkle tree
type MerkleTree struct {
	RootNode *MerkleNode
}

// MerkleNode represent a Merkle tree node
// every MerkleNode keeps data and links to its branches
// the MerkleTree is the root node linked to the next nodes
//    - they are then linked to further nodes... 
type MerkleNode struct {
	Left  *MerkleNode
	Right *MerkleNode
	Data  []byte
}

// NewMerkleTree creates a new Merkle tree from a sequence of data
// every node contains data
// when a node is a leaf - data is passed from the outside
// when the node is linked to other nodes - data from the other linked nodes is
//    concatenated and hashed inside that node
func NewMerkleTree(data [][]byte) *MerkleTree {
	var nodes []MerkleNode

	if len(data)%2 != 0 { //ensure there is an even amount of leaves
	// data is an array of serialized transactions
		data = append(data, data[len(data)-1])
	}
	// data is converted into tree leaves - tree is grown from these leaves
	for _, datum := range data {
		node := NewMerkleNode(nil, nil, datum)
		nodes = append(nodes, *node)
	}

	for i := 0; i < len(data)/2; i++ {
		var newLevel []MerkleNode

		for j := 0; j < len(nodes); j += 2 {
			node := NewMerkleNode(&nodes[j], &nodes[j+1], nil)
			newLevel = append(newLevel, *node)
		}

		nodes = newLevel
	}

	mTree := MerkleTree{&nodes[0]}

	return &mTree
}

// NewMerkleNode creates a new Merkle tree node
// 
func NewMerkleNode(left, right *MerkleNode, data []byte) *MerkleNode {
	mNode := MerkleNode{}

	if left == nil && right == nil {
		hash := sha256.Sum256(data)
		mNode.Data = hash[:]
	} else {
		prevHashes := append(left.Data, right.Data...)
		hash := sha256.Sum256(prevHashes)
		mNode.Data = hash[:]
	}

	mNode.Left = left
	mNode.Right = right

	return &mNode
}
