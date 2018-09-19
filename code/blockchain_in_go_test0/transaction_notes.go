// notes and test code from:
// https://jeiwan.cc/posts/building-blockchain-in-go-part-4/

// a transaction is a comination of inputs:
type Transaction struct {
	ID       []byte
	Vin   []TXInput
	Vout []TXOutput
}

// inputs of a new transaction reference the outputs of the previous tranaction
// inputs can reference outputs from multiple transactions
// transactions lock values wih a script
//  - these can only be unlocked by the one who locked the values

// outputs:
type TXOutput struct {

	Value           int
	ScriptPubKey string // stores a user defined wallet address
}

// inputs:
type TXInput struct {
	TXid      []byte // transaction ID
	Vout         int // index of an output in the transaction
	ScriptSig string // provides data to be used in output's ScriptPubKey
}
// if the data in the ScriptSig is correct - output can be unlocked
// once the output is unlocked - its value can be used to generate new outputs
//  - if data is not correct - the output cannot be referenced in the input

// each output has an unlocking script
//    - this script determines the logic of unlocking the output
// every transaction must have at least one input and one output
// the input references an output from a previous transaction
// the input provides data used in the output's unlocking script to unlock
//    the output and use the output's value to create new outputs
// inputs produce outputs - then the outputs make inputs possible

// a miner starts mining a block
//    - then a coinbase transaction is added to the block
//    - a coinbase transaction does not require a previously existing output
//    - outputs are generated - in bitcoin these are rewards in coins to miners
// coinbase transaction:
func NewCoinbaseTX(to, data string) *Transaction {
	if data == "" {
		data = fmt.Sprintf("Reward to '%s'", to)
	}
	txin := TXInput{[]byte{}, -1, data}
	txout := TXOutput{subsidy, to} // subsidy is the amount of the reward
	tx := Transaction{nil, []TXInput{txin}, []TXOutput{txout}}
	tx.SetID()

	return &tx
}