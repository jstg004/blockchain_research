from blockchain import Blockchain
from hashlib import sha256


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