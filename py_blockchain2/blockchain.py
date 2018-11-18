# Import the Block class from block.py:
from block import Block


class Blockchain:

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


    # Prints contents of blockchain:
    def print_blocks(self):
        # Iterates though the chain:
        for i in range(len(self.chain)):
            current_block = self.chain[i]

            print(f'Block {i} {current_block}')

            current_block.print_contents()


    # Add block to blockchain:
    def add_block(self, data):
        # The previous hash is created using the data from the previous block
        # in the chain:
        prev_hash = self.chain[len(self.chain) - 1].hash

        # Places the data and the previous hash into the new block:
        new_block = Block(data, prev_hash)

        new_block.generate_hash() # Generates a hash of the new block.

        proof = self.proof_of_work(new_block) # Performs PoW on the new block.

        self.chain.append(new_block) # Append the new block to the chain.

        return proof, new_block


    # Checks to see if blocks are linked to each other properly:
    def validate_chain(self):

        for i in range(1, len(self.chain)):
            current = self.chain[i] # Most recent block in the chain.
            prev = self.chain[i - 1] # Previous block in the chain.

            # Check if the hash of the current block is NOT = to the value that
            # the current block generates:
            if current.hash != current.generate_hash():
                print('The hash of the current block is not equal to the value that the current block generates.')
                # If NOT = then blockchain is invalid.
                return False

            # Check if the hash of the previous hash of the current block
            # is NOT = to the value generated over the previous block:
            if current.prev_hash != prev.generate_hash():
                print("The hash of the previous hash of the current block is not equal to the value generated over the previous block")
                # If NOT = then blockchain is invalid.
                return False

        # If above conditions are not satisfied, then blockchain is valid:
        return True


    # Performs the PoW algorithm, difficulty refers to number of leading zeros.
    def proof_of_work(self, block, difficulty = 2):
        # Generates hash of the block:
        proof = block.generate_hash()

        # Increase the nonce value in the loop and generate a new hash,
        # until found hash matches the hash which includes the leading zeros:
        while proof[:difficulty] != '0' * difficulty:
            block.nonce += 1
            proof = block.generate_hash()

        # After finding the correct hash, set the value back to 0:
        block.nonce = 0

        return proof