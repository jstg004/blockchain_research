'''
To make SnakeCoin an actual cryptocurrency:
 - need control the amount of blocks (and coins) that can be
   created at a particular time.
 - Each transaction will be a JSON object detailing the sender
   of the coin, the receiver of the coin, and the amount of
   SnakeCoin that is being transferred.
'''


import hashlib as hasher
import datetime as date


# This is the code defines what a block is in SnakeCoin blockchain.
'''
What is a Blockchain?
 - a public database where new data are stored in a container
   called a block
 - the blocks are added to an immutable chain (Blockchain)
'''

# Define what the blocks will look like:
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    '''
     - Each block’s hash will be a cryptographic hash of the
       block’s index, timestamp, data, and the hash of the
       previous block’s hash.
    '''
    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()


# This is the code that generates the first block in the
# SnakeCoin blockchain.
'''
Create a function that returns a genesis block.
This block is of index 0, and it has an arbitrary data value
and an arbitrary value in the “previous hash” parameter.
'''
def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")


# This is the code that creates a new block in the SnakeCoin blockchain
'''
Creates a function that will generate succeeding blocks in the
blockchain.
This function will take the previous block in the chain as a
parameter, create the data for the block to be generated, and return
the new block with its appropriate data.
When new blocks hash information from previous blocks, the integrity
of the blockchain increases with each new block.
This chain of hashes acts as cryptographic proof and helps ensure that
once a block is added to the blockchain it cannot be replaced or removed.
'''

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash

    return Block(this_index, this_timestamp, this_data, this_hash)


# This is the code for the the blockchain itself.
# In this blockchain example the blockchain is a simple Python list.

# Creates the blockchain and add the genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# How many blocks should we add to the chain after the genesis block.
num_of_blocks_to_add = 20

# Add blocks to the chain
for i in range(0, num_of_blocks_to_add):
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    previous_block = block_to_add

    # Announce that the blocks have been added to the blockchain
    print(f"Block #{block_to_add.index} has been added to the blockchain")
    print(f"Hash: {block_to_add.hash}\n")