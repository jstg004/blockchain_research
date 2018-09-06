from flask import Flask, request

node = Flask(__name__)


# Store the transactions that this node has in a list
this_nodes_transactions = []

@node.route('/txion', methods=['POST'])
def transaction():
    if request.method == 'POST':
        # On each new POST request, we extract the transaction data
        new_txion = request.get_json()

        # Then we add the transaction to our list
        this_nodes_transaction.append(new_txiod)

        # Because the transaction was successfully submitted,
        # we log it to our console
        print("New transaction")
        print(f"FROM: {new_txion['from']}")
        print(f"TO: {new_txion['to']}")
        print(f"AMOUNT: {new_txion['amount']}\n")

        # Then we let the client know it worked
        return "Transaction submission successful\n"

node.run()