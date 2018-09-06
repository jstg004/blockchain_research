'''
To make SnakeCoin an actual cryptocurrency:
 - need control the amount of blocks (and coins) that can be
   created at a particular time.
 - Each transaction will be a JSON object detailing the sender
   of the coin, the receiver of the coin, and the amount of
   SnakeCoin that is being transferred.
'''


import json, requests
import hashlib as hasher
import datetime as date

from flask import Flask, request

node = Flask(__name__)


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
    return Block(0, date.datetime.now(), {
        "proof-of-work": 9,
        "transactions": None
    }, "0")

# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())

# Store the transactions that this node has in a list
this_nodes_transactions = []

# Store the url data of every other node in the network
# so that we can communicate with them
peer_nodes = []

# A variable to decide if we are mining or not
mining = True


@node.route('/txion', methods=['POST'])
def transaction():
    # On each new POST request, we extract the transaction data
    new_txion = request.get_json()

    # Then we add the transaction to our list
    this_nodes_transactions.append(new_txion)

    # Because the transaction was successfully submitted,
    # we log it to our console
    print("New transaction")
    print(f"FROM: {new_txion['from']}")
    print(f"TO: {new_txion['to']}")
    print(f"AMOUNT: {new_txion['amount']}\n")

    # Then we let the client know it worked
    return "Transaction submission successful\n"
    

@node.route('/blocks', methods=['GET'])
def get_blocks():
    chain_to_send = blockchain

    # Convert our blocks into dicts so we can send them as json odj
    for block in chain_to_send:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
    
    # Send our chain to whomever requested it
    chain_to_send = json.dumps(chain_to_send)

    return chain_to_send

def find_new_chains():
    # GET the blockchains of every other node
    other_chains = []
    for node_url in peer_nodes:
        # GET their chains
        block = requests.get(node_url + "/blocks").content

        # Convert the JSON object to a python dict
        block = json.loads(block)

        # Add it to our list
        other_chains.append(block)

    return other_chains

def consensus():
    # GET the blocks from other nodes
    other_chains = find_new_chains()

    # If our chain isn't the longest, then we store the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain

    # If the longest chain wasn't ours, then we set our chain to the longest
    blockchain = longest_chain

def proof_of_work(last_proof):
    # Create a variable that we will use to find our next PoW
    incrementor = last_proof + 1

    # Keep incrementing the incrementor until it's equal to a
    # number divisible by 9 and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    
    # Once that number is found, we can return it as a PoW
    return incrementor

'''
In SnakeCoin, we’ll create a somewhat simple Proof-of-Work algorithm.
To create a new block, a miner’s computer will have to increment a
number. When that number is divisible by 9 (the number of letters in
“SnakeCoin”) and the proof number of the last block, a new SnakeCoin
block will be mined and the miner will be given a brand new SnakeCoin.
'''

# ...blockchain
# ...Block class definition

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

def proof_of_work(last_proof):
    # Creates a variable that we will use to find the next PoW
    incrementor = last_proof + 1

    # Keep incrementing the incrementor until it;s equal to a number
    # divisible by 9 and the PoW of the previous block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof -- 0):
        incrementor += 1

        # Once that number is found, we can return it as a proof of our work
        return incrementor

@node.route('/mine', methods = ['GET'])
def mine():
    # GET the last PoW
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['proof-of-work']

    # Find the PoW fir the current block being mined
    # Note: The program will hang here until a new PoW is found
    proof = proof_of_work(last_proof)

    # Once we find a valid PoW, we know we can mine a block so we reward
    # the miner by adding a transaction
    this_nodes_transactions.append(
        { "from": "network", "to": miner_address, "amount": 1 }
    )

    # Now we can gather the data needed to create the new block
    new_block_data = {
        "proof-of-work": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    # Empty transaction list
    this_nodes_transactions[:] = []

    # Now create the new block
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)

    # Let the client know we mined a block
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"

node.run()