'''
Our consensus algorithm will be rather simple: if a node’s chain is
different from another’s (i.e. there is a conflict), then the
longest chain in the network stays and all shorter chains will be
deleted. If there is no conflict between the chains in our network,
then we carry on.
'''

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