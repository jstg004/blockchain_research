import datetime

from hashlib import sha256


class Block:

    def __init__(self, data, prev_hash):
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.generate_hash()


    # Convert block contents to string and hash that string:
    def generate_hash(self):
        block_header = str(self.timestamp) + str(self.data) \
            + str(self.prev_hash) + str(self.nonce)

        block_hash = sha256(block_header.encode())

        return block_hash.hexdigest()


    # Print block contents:
    def print_contents(self):
        print("timestamp:", self.timestamp)
        print("data:", self.data)
        print("current hash:", self.generate_hash())
        print("previous hash:", self.prev_hash)