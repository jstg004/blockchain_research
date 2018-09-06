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