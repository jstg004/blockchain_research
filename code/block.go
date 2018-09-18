package main

type Block struct {
	Timestamp      int64 // current timestamp when block is created
	Data          []byte // actual information contained in the block
	PrevBlockHash []byte // hash of the previous block
	Hash          []byte
}

// take block fields, concatenate them, then calculate a SHA-256 hash
func (b *Block) SetHash() {
	timestamp := []byte(strconv.FormatInt(b.Timestamp, 10))
	headers := bytes.Join([][]byte{b.PrevBlockHash, b,Data, timestamp}, []byte{})
	hash := sha256.Sum256(headers)
	b.Hash = hash[:]
}

// implement a function that will simplify the creation of the block
func NewBlock(data string, prevBlockHash []byte) * Block {
	block := &Block{time.Now().Unix(), []byte(data), prevBLockHash, []byte{}}
	block.SetHash()
	return block
}

// a blockchain is a database with an ordered structure - a back-linked list
// blocks are stored in the insertion order and each block is linked to the
// previous block
// this is implemented using an array and a map
// the array keeps ordered hashes
// the map keeps hash block - pairs
type Blockchain struct{
	blocks []*Block
}

func (bc *Blockchain) AddBlock(data string) {
	prevBlock := bc.blocks[len(bc.blocks)-1]
	newBlock := NewBlock(data, prevBlock.Hash)
	bc.blocks = apend(bc.blocks, newBlock)
}

// create the genesis block
func NewGenesisBlock() *Block {
	return NewBlock("Genesis Block", []byte{})
}

// implement a function that creates a blockchain with the genesis block
func NewBlockchain() *Blockchain{
	return &Blockchain{[]*Block{NewGenesisBlock()}}
}

// check to make sure the blockchain is working correctly
func main() {
	bc := NewBlockchain()
	bc.AddBlock("send 1 BTC to Ivan")
	bc.AddBlock("send 2 more BTC to Ivan")

	for _, block := range bc.blocks {
		fmt.Printf("prev. hash: %x\n", block.PrevBlockHash)
		fmt.Printf("Data: %s\b", block.data)
		fmt.Printf("Hash: %x\n", block.Hash)
		fmt.Println()
	}
}

// below is the output of this code:
//
// Prev. hash:
// Data: Genesis Block
// Hash: aff955a50dc6cd2abfe81b8849eab15f99ed1dc333d38487024223b5fe0f1168
//
// Prev. hash: aff955a50dc6cd2abfe81b8849eab15f99ed1dc333d38487024223b5fe0f1168
// Data: Send 1 BTC to Ivan
// Hash: d75ce22a840abb9b4e8fc3b60767c4ba3f46a0432d3ea15b71aef9fde6a314e1
//
// Prev. hash: d75ce22a840abb9b4e8fc3b60767c4ba3f46a0432d3ea15b71aef9fde6a314e1
// Data: Send 2 more BTC to Ivan
// Hash: 561237522bb7fcfbccbc6fe0e98bbbde7427ffe01c6fb223f7562288ca2295d1