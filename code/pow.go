// proof of work - hashcash - brute force algorithm
// 1. take the block header
// 2. add a counter to it (starts at 0)
// 3. create a hash of (data + counter)
// 4. check the hash - must meet a set of requirements
//    - if it meets requirements, then move on
//    - if requirements are not met, then the counter is increased and steps 3
//      and 4 are repeated

package main

import "math/big"

//this is the block header - stores difficulty at which the block was mined
const targetBits = 24

type ProofOfWork struct {
	block  *Block
	target *big.Int
}

// the PoW structure - holds a pointer to a block and a pointer to a target
// the target is the requirement set that the hash must meet
// converts the hash to a big integer and checks if it is less than the target
func NewProofOfWork(b *Block) *ProofOfWork {
	target := big.NewInt(1) // initializes big.Int with value of 1
    // shifts the above target left by (256 - targetBits)
	target.Lsh(target, uint(256-targetBits))
    // this target starts out as:
    // 0x10000000000000000000000000000000000000000000000000000000000
    // this occupies 29 bytes in memory
    // the target is the upper boundary of a range
    //  - if the hash is lower than the boundary, then it is valid
    //  - if the hash is higher than the boundary, then it is not valid
    //  - the lower the boundary - the fewer valid numbers - more difficult work

    // if you check the below hashes with the target
	// #1 is larger - not valid
	// #2 is smaller - valid
    // 1. 0fac49161af82ed938add1d8725835cc123a1a87b1b196488360e58d4bfb51e3
    // 2. 0000010000000000000000000000000000000000000000000000000000000000

	pow := &ProofOfWork{b, target}

	return pow
}

// data:
// merge the block fields with the target and nonce
// the nonce here is the counter
func (pow *ProofOfWork) prepareData(nonce int) []byte {
	data := bytes.Join(
		[][]byte{
			pow.block.PrevBlockHash,
			pow.block.Data,
			IntToHex(pow.block.Timestamp),
			IntToHex(int64(targetBits)),
			IntToHex(int64(nonce)),
		},
		[]byte{},
	)
	return data
}

// PoW algorithm:
