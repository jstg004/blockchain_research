# This is the code that generates the first block in the
# SnakeCoin blockchain.

import datetime as date


'''
Create a function that returns a genesis block.
This block is of index 0, and it has an arbitrary data value
and an arbitrary value in the “previous hash” parameter.
'''
def create_genesis_block():
    # Manually construct a block with
    # index zero and arbitrary previous hash
    return Block(0, datetime.now(), "Genesis Block", "0")