# This is the code defines what a block is in SnakeCoin blockchain.

'''
What is a Blockchain?
 - a public database where new data are stored in a container
   called a block
 - the blocks are added to an immutable chain (Blockchain)
'''

import hashlib as hasher


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

        sha.update(str(self.index)) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(self.previous_hash))

        return sha.hexdigest()