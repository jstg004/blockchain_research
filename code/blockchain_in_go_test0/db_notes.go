// this is a work in progress and notes for this tutorial:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-3/

// uses encoding/gob to serialize the block structs
func b *Block) Serialize() []byte {
	var result bytes.Buffer //declare a buffer that stores the serialized data
	encoder := gob.NewEncoder(&result) //initialize gob encoder-encode the block
	err := encoder.Encode(b)

	return result.Bytes() //a byte array is returned
}

// this deserializing function receives the byte array as input and returns
// a block
func DeserializeBlock(d []byte) *Block {
	var block Block
	decoder := gob.NewDecoder(bytes.NewReader(d))
	err := decoder.Decode(&block)

	return &block
}

// 1. open a database file
// 2. check if there is a blockchain stored in it
// 3. if there is a blockchain then
//   - create a new blockchain instance
//   - set the tip of the blockchain instance to the last block hash stored in
//     the database
// 4. if there is no existing blockchain
//   - create the genesis block
//   - store this genesis block in the database
//   - save the hash of the genesis block as the last block hash
//   - create a new blockchain instance - tip pointing at the genesis block
func NewBlockchain() *Blockchain {
	var tip []byte
	db, err := bolt.Open(dbFile, 0600, nil) //open a BoltDB file

	// operations are run within a transaction
	// there are either read-only or read-write transactions
	// this opens a read-write transaction - db.Update
	err = db.Update(func(tx *bolt.Tx) error {

		// obtain the bucket storing the blocks
		b := tx.Bucket([]byte(blocksBucket))

		if b == nil { //if bucket does not exist, then:

			// - generate the genesis block
			genesis := NewGenesisBlock()

			// - create the bucket
			b, err := tx.CreateBucket([]byte(blocksBucket))
			err = b.Put(genesis.Hash, genesis.Serialize())

			// - save the block into the bucket
			err = b.Put([]byte("l"), genesis.Hash)

			//update the 'l' key storing the last block hash of the chain
			tip = genesis.Hash

		} else { //if the bucket exists - then read the 'l' key from that block
			tip = b.Get([]byte("l"))
		}
		return nil
	})
	// creates the blockchain, only the tip of the chain is stored
	// stores the database connection - keeps the connection open while program
	// is running
	bc := Bockchain{tip, db}

	return &bc
}

// blockchain structure:
type Blockchain struct {
	tip []byte
	db *bolt.DB

}

func (bc *Blockchain) AddBlock(data string) {
	var lastHash []byte

	// read-only transaction
	// get last block hash from the db
	// use it to mine a new block hash
	err := bc.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(blocksBucket))
		lastHash = b.Get([]byte("l"))

		return nil
	})
	// after new block is mined - save its serialized representation into db
	// then update the 'l' key - it now stores the new block's hash
	newBlock := NewBlock(data, lastHash)
	err = bc.db.Update(func(tc *bolt.Tx) error {
		b := tx.Bucket([]byte(blocksBucket))
		err := b.Put(newBlock.Hash, newBlock.Serialize())
		err = b.Put([]byte("l"), newBlock.Hash)
		bc.tip = newBlock.Hash

		return nil
	})
}

// BoltDB allows for iteration over all the keys in a bucket
// keys are stored in byte-sorted order
// create a blockchain iterator to read each block in the chain one by one
type BlockchainIterator struct {
	currentHash []byte
	db        *bolt.DB
}
// the above iterator will be created everytime we want to iterate over blocks
// in a blockchain
// the iterator will store the block hash of the current iteration
// the iterator will store a connection to a db
// the iterator is logically attached to the blockchain
//   - a blockchain instance which stores a db connection
func (bc *Blockchain) Iterator() *BlockchainIterator {
	bci := &BlockchainIterator{bc.tip, bc.db}

	return bci
}
// the iterator initially points to the tip of the blockchain
//  - blocks are obtained from the top to the bottom (newest - oldest)
//  - if a blockchain has multiple branches
//    - the longest blockchain is the main chain
//  - a tip can be any block in the blockchain
//    - the entire blockchain can be reconstructed and length can be calculated
//    - the work required to build the block chain can also be calculated
//  - a tip is a type of identifier of a blockchain

// the BlockchainIterator returns the next block from a blockchain
func (i *BlockchainInterator) Next() *Block {
	ver block *block
	err := i.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(blockBucket))
		encodedBlock := b.Get(i.currentHash)
		block = DeserializeBlock(encodedBlock)

		return nil
	})
	i.currentHash = block.PrevBlockHash

	return block
}