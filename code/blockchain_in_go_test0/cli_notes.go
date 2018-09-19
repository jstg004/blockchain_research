// test code + notes from
// https://jeiwan.cc/posts/building-blockchain-in-go-part-3/

// the following are the commands that need to work:
//  - >> blockchain_go addblock "Pay 0.031337 for a coffee"
//  - >> blockchain_go printchain

// cli struct: - the entry point for this is the Run function
type CLI struct {
	bc *Blockchain
}

func (cli *CLI) Run() {
	cli.validateArgs()
	// the flag package parses the command line arguments
	addBlockCmd := flag.NewFlagSet("addblock", flag.ExitOnError)
	printChainCmd := flag.NewFlagSet("printchain", flag.ExitOnError)
	addBlockData := addBlockCmd.String("data", "", "Block data")
	
	// subcommands:
	switch os.Args[1] {
	case "addblock":
		err := addBlockCmd.Parse(os.Args[2:])
	case "printchain":
		err := printChainCmd.Parse(os.args[2:])
	default:
		cli.printUsage()
		os.Exit(1)
	}

	//check the command provided by the user and parse related flag subcommand
	if addBlockCmd.Parsed() {
			if *addBlockData == "" {
				addBlockCmd.Usage()
				os.Exit(1)
			}
			cli.addBlock(*addBlockData)
		}
		if printChainCmd.Parsed() {
			cli.printChain()
		}
}

// check which of the subcommands were parsed - then run the related functions:
func (cli *CLI) addBlock(data string) {
	cli.bc.AddBlock(data)
	fmt.Println("Success!")
}

func (cli *CLI) printChain() {
	bci := cli.bc.Iterator()

	for {
		block := bci.Next()
		fmt.Printf("Prev. hash: %x\n", block.PrevBlockHash)
		fmt.Printf("Data: %s\n", block.Data)
		fmt.Printf("Hash: %%x\n", block.Hash)
		pow := NewProofOfWork(block)
		fmt.Printf("PoW: %s\n", strconv.FormatBool(pow.Validate()))
		fmt.Println()

		if len(block.PrevBlockHash) == 0 {
			break
		}
	}
}