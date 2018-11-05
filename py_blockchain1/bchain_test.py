'''
Testing out building a blockchain from scratch in python.
    - initially used only for storing some data in a blockchain
    - this is the very start and I am slowly learning techniques and adding to
      this code
    - the code will drastically change and include lots of tests and unnecessary
      code for breaking down how each little part works
'''


import hashlib, json, datetime

from hashlib import blake2b
from hmac import compare_digest

from Crypto.PublicKey import RSA


date_time = str(datetime.datetime.utcnow())

# hashes the blocks in the blockchain
def hash_blocks(blocks):
    prev_hash = None

    for block in blocks:
        block_serialized = json.dumps(block, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()
        prev_hash = block_hash

    return prev_hash

# for signing blocks
SECRET_KEY = b''
AUTH_SIZE = 64

# sign a block
def sign(block):
     h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
     h.update(block)
     return h.hexdigest().encode('utf-8')

# verify a block signature
def verify(block, sig):
    good_sig = sign(block)
    return compare_digest(good_sig, sig)


try:
    with open('blockchain.json') as infile:
        blockchain_load = json.load(infile)
        count = 0

        if blockchain_load["chain"]['genesis'] == True:
            count += 1
            # when new data is entered into the blockchain it must be broadcast
            # to other nodes on the network, so all blockchains stay in sync
            # ask for next block data:
            name = input("Enter Name: ")
            name_id = input("Enter ID: ")

            date_time = str(datetime.datetime.utcnow())

            prev_hash = hash_blocks([blockchain_load])

            block = {
                'prev_hash': prev_hash,
                'genesis': False,
                'data': {
                    'name': name,
                    'name_id': name_id,
                    'time': date_time
                }
            }

            # sign the block which will be added to the bockchain
            block_to_sig = hash_blocks([blockchain_load]).encode('utf-8')
            block_sig = str(sign(block_to_sig))
            #verify = verify(block_to_sig, block_sig)

            blockchain_load[block_sig] = block

            with open('blockchain.json', 'w') as outfile:
                json.dump(blockchain_load, outfile)

except:
    blockchain = {}
    # generate genesis block
    block_genesis = {
        'prev_hash': None,
        'genesis': True,
        'data': {
            'name': 'genesis',
            'name_id': 0,
            'time': date_time
        }
    }

    blockchain['chain'] = block_genesis
    # add the genesis block to the blockchain json file
    with open('blockchain.json', 'w') as outfile:
        json.dump(blockchain, outfile)




'''
TODO:
    check if chain has been tampered with
        - edit an entry, hash it, check the hash
    add other nodes and add functionality for blockchain syncing
        - try kademlia
'''