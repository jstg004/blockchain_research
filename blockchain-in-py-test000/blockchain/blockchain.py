from collections import OrderedDict

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import requests, hashlib, binascii



MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 1
MINING_DIFFICULTY = 2

class Blockchain:
    def __init__(self):
        self.transactions = []
        self.chain = []
        self.nodes = set()

        # Generates rancom number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')

        # Creates a genesis block:
        self.create_block(0, '00')

    def register_node(self, node_url):
        # Adds a new node to the list of nodes
        parsed_url = urlparse(node_url) #check node_url has valid format
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts url without scheme like '192.168.1.1:5000'
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def verify_transaction_signature(self, sender_address, signature, transaction):
        '''
        Check that the provided signature corresponds to transaction signed by
        the public key (sender_address)
        '''
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(transaction).encode('utf8'))
        
        return verifier.verify(h, binascii.unheaxlify(signature))

    def submit_transaction(self, sender_address, recipient_address, value, signature):
        # Add a transaction to transactions array if the signature verified
        transaction = OrderDict({
            'sender_address': sender_address,
            'recipient_address': recipient_address,
            'value': value
        })

        # Reward for mining a block
        if sender_address == MINING_SENDER:
            self.transactions.append(transaction)
            return len(self.chain) + 1
        # Manages transactions from wallet to another wallet
        else:
            transaction_verification = self.verify_transaction_signature(sender_address, signature, transaction)
            if transaction_verification:
                self.transactions.append(transaction)
                return len(self.chain) + 1
        else
            return False

    def create_block(self, nonce, previous_hash):
        # Add a block of transactions to the blockchain
        block = {
            'block_number': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        }

        self.transactions = [] #resets the current list of transactions
        self.chain.append(block)

        return block

    def hash(self, block):
        # Creates a SHA-256 hash of a block
        # Makes sure that the dict is ordered for consistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self):
        # Proof of Work algorithm
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)
        nonce = 0

        while self.valid_proof(self.transactions, last_hash, nonce) is False:
            nonce += 1

        return nonce

    def valid_proof(self, transactions, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        '''`
        Check if a hash value satisfies the mining conditions.
        This function is used within the proof_of_work function.
        '''
        guess = (str(transactions) + str(last_hash) + str(nonce))).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:difficulty] == '0' * difficulty

    def valid_chain(self, chain):
        # Check if a blockchain is valid
        last_block = chain[0]
        current index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Checks if the PoW is correct
            # Deletes the reward transaction
            transactions = block['transactions'] [:-1]

            # Need to make sure that the dictionary is ordered. Otherwise we'll get a different hash
            tranaction_elements = ['sender_address', 'recipient_address', 'value']
            transactions = [OrderedDict((k, transaction[k]) for k in transaction_elements) for transaction in transactions]

            if not self.valid_proof(transactions, block['previous_hash'], block['nonce'], MINING_DIFFICULTY):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        