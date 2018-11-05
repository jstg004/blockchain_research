'''
Testing out building a blockchain from scratch in python.
    - initially used only for storing some data in a blockchain
    - this is the very start and I am slowly learning techniques and adding to
      this code
    - the code will drastically change and include lots of tests and unnecessary
      code for breaking down how each little part works
'''


import hashlib, json, datetime


date_time = str(datetime.datetime.utcnow())

# hashes the blocks in the blockchain
def hash_blocks(blocks):
    prev_hash = None

    for block in blocks:
        block['prev_hash'] = prev_hash
        block_serialized = json.dumps(block, sort_keys=True).encode('utf-8')
        block_hash = hashlib.sha256(block_serialized).hexdigest()
        prev_hash = block_hash

    return prev_hash

try:
    with open('blockchain.json') as infile:
        blockchain_load = json.load(infile)
        count = 0

        if blockchain_load["chain"]['genesis'] == True:
            count += 1
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

            current_hash = hash_blocks([blockchain_load, block])
            blockchain_load[current_hash] = block

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
'''