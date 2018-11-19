from blockchain import Blockchain
from hashlib import sha256

import json


'''
TODO:
- make json persistent
- if chain exists, then add to it
- if no chain exists, then create genesis block
'''


block_data0 = {
    'uid': 'dsf34f234sd3dsafp',
    'name': 'First0 Last0',
    'member': 'Team0'
}

block_data1 = {
    'uid': 'dsfasdfa34q52saf1',
    'name': 'First1 Last1',
    'member': 'Team1'
}

block_data2 = {
    'uid': 'dsfa2asds234gs116',
    'name': 'First2 Last2',
    'member': 'Team0'
}


print('')
print('Before adding data to the blockchain:')
local_blockchain = Blockchain()

local_blockchain.print_blocks()
print('-------------------------------------------')
print('')

'''
local_blockchain.add_block(block_data0)
local_blockchain.add_block(block_data1)
local_blockchain.add_block(block_data2)


print('')
print('After adding data to the blockchain:')
local_blockchain.print_blocks()
print('')

print('Is this blockchain valid?')
print(local_blockchain.validate_chain())
print('-------------------------------------------')
print('')


fake_block_data = {
    'uid': '000a2asds234gs116',
    'name': 'First4 Last4',
    'member': 'Team2'
}

print('')
print('After adding manipulated block data to the blockchain:')
local_blockchain.chain[2].data = fake_block_data
local_blockchain.print_blocks()
print('')
print('Is this blockchain valid?', local_blockchain.validate_chain())
'''



'''
Before adding data to the blockchain:
Block 0 <block.Block object at 0x10a587550>
timestamp: 2018-11-18 10:50:32.667587
data: {}
current hash: 44402c51bfb6b6407d82ff3b9df0106a98f5b77bd9ad1e6429cc233e39e50401
previous hash: 0
-------------------------------------------


After adding data to the blockchain:
Block 0 <block.Block object at 0x10a587550>
timestamp: 2018-11-18 10:50:32.667587
data: {}
current hash: 44402c51bfb6b6407d82ff3b9df0106a98f5b77bd9ad1e6429cc233e39e50401
previous hash: 0
Block 1 <block.Block object at 0x10a5875c0>
timestamp: 2018-11-18 10:50:32.667705
data: {'uid': 'dsf34f234sd3dsafp', 'name': 'First0 Last0', 'member': 'Team0'}
current hash: facaa2adee8140533f98e7d178f9a07eddc7cef2f5e08b5410ac53120634bf11
previous hash: 44402c51bfb6b6407d82ff3b9df0106a98f5b77bd9ad1e6429cc233e39e50401
Block 2 <block.Block object at 0x10a587940>
timestamp: 2018-11-18 10:50:32.669303
data: {'uid': 'dsfasdfa34q52saf1', 'name': 'First1 Last1', 'member': 'Team1'}
current hash: 703c639c85292bd0c1069f44aef3152c61816e8bbbbad06247d74a0633c314c4
previous hash: facaa2adee8140533f98e7d178f9a07eddc7cef2f5e08b5410ac53120634bf11
Block 3 <block.Block object at 0x10a5879b0>
timestamp: 2018-11-18 10:50:32.669703
data: {'uid': 'dsfa2asds234gs116', 'name': 'First2 Last2', 'member': 'Team0'}
current hash: 400facc99436044a2b1f556f7aa59ebce139f3c5a39a78902b0964595aa52174
previous hash: 703c639c85292bd0c1069f44aef3152c61816e8bbbbad06247d74a0633c314c4

Is this blockchain valid?
True
-------------------------------------------


After adding manipulated block data to the blockchain:
Block 0 <block.Block object at 0x10a587550>
timestamp: 2018-11-18 10:50:32.667587
data: {}
current hash: 44402c51bfb6b6407d82ff3b9df0106a98f5b77bd9ad1e6429cc233e39e50401
previous hash: 0
Block 1 <block.Block object at 0x10a5875c0>
timestamp: 2018-11-18 10:50:32.667705
data: {'uid': 'dsf34f234sd3dsafp', 'name': 'First0 Last0', 'member': 'Team0'}
current hash: facaa2adee8140533f98e7d178f9a07eddc7cef2f5e08b5410ac53120634bf11
previous hash: 44402c51bfb6b6407d82ff3b9df0106a98f5b77bd9ad1e6429cc233e39e50401
Block 2 <block.Block object at 0x10a587940>
timestamp: 2018-11-18 10:50:32.669303
data: {'uid': '000a2asds234gs116', 'name': 'First4 Last4', 'member': 'Team2'}
current hash: c6915af79c31d0bd3c4363084fdf13aa1856952ce6e3e8aa1c21971aeb2d2b53
previous hash: facaa2adee8140533f98e7d178f9a07eddc7cef2f5e08b5410ac53120634bf11
Block 3 <block.Block object at 0x10a5879b0>
timestamp: 2018-11-18 10:50:32.669703
data: {'uid': 'dsfa2asds234gs116', 'name': 'First2 Last2', 'member': 'Team0'}
current hash: 400facc99436044a2b1f556f7aa59ebce139f3c5a39a78902b0964595aa52174
previous hash: 703c639c85292bd0c1069f44aef3152c61816e8bbbbad06247d74a0633c314c4

The hash of the current block is not equal to the value that the current block generates.
Is this blockchain valid? False
'''


"""
import sqlite3

conn = sqlite3.connect('blockchain.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchone())

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

"""



"""
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
            contact = input("Enter Contact: ")

            block_data = {
                'uid': name_id,
                'name': name,
                'contact': contact
            }


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
"""