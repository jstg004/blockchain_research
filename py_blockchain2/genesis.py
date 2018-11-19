from block import Block


class Genesis:

    def __init__(self):

        self.chain = [] # Creates a list to hold the blocks.

        # Auto generate genesis block when a new blockchain is instantiated:
        self.genesis_block()


    def genesis_block(self):
        
        data = {} # Creates the dictionary to hold the data in the block.

        # No previous block before the genesis block, previous hash = 0.
        genesis_block = Block(data, '0')

        # Add the block to the chain:
        self.chain.append(genesis_block)

        return self.chain