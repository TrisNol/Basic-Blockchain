from model.Block import Block
from model.Blockchain import Blockchain

from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests
import time
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

blockchain = Blockchain()

peers = set()

@app.route('/register_node', methods=['POST'])
@cross_origin()
def register_new_node():
    node_address = request.get_json()['node_address']
    if not node_address:
        return "Invalid data", 400
    peers.add(node_address)
    return get_chain()

@app.route('/register_with', methods=['POST'])
@cross_origin()
def register_with_existing_node():
    """
    Internally calls the register_node endpoint to register current node with the remote node
    specified in the request, and sync the blockchain as well with the remote node
    """

    node_address = request.get_json()['node_address']
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type':"application/json"}

    # Make a request to register with remote node and obtain information
    response = request.post(node_address + "/register_node", data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        return "Registration successful", 200
    else:
        return response.content, response.status_code

def create_chain_from_dump(chain_dump):
    blockchain = Blockchain()
    for idx, block_data in enumerate(chain_dump):
        block = Block(
            index=block_data['index'],
            transactions=block_data['transactions'],
            timestamp=block_data['timestamp'],
            previous_hash=block_data['previous_hash']
        )
        proof = block_data['hash']
        if idx > 0:
            added = blockchain.add_block(block, proof)
            if not added:
                raise Exception("The chain dump is tempered!")
        else:
            blockchain.chain.append(block)
    return blockchain

@app.route("/new_transaction", methods=["POST"])
@cross_origin()
def new_transaction():
    tx_data = request.get_json()
    required_fields = ['author','content']

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404
    
    tx_data['timestamp'] = time.time()

    blockchain.add_new_transaction(tx_data)
    return "Success", 200

@app.route("/chain", methods=['GET'])
@cross_origin()
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    chain = {"length": len(chain_data), "chain": chain_data}
    return json.dumps(chain)

@app.route("/mine", methods=['GET'])
@cross_origin()
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "Not transactions to mine"
    else:
        chain_length = len(blockchain.chain)
        # update our blockchain before we check length
        consensus()
        if chain_length == len(blockchain.chain):
            announce_new_block(blockchain.last_block)
    return "Block #{} is mined.".format(result)

@app.route('/pending_tx')
@cross_origin()
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

@app.route('/add_block', methods=['POST'])
@cross_origin()
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(
        index=block_data['index'],
        transactions=block_data['transactions'],
        timestamp=block_data['timestamp'],
        previous_hash=block_data['previous_hash']
    )
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400
    return "Block added to the chain", 200

def announce_new_block(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their respective chains.
    """

    for peer in peers:
        url = "{}/add_block".format(peer)
        requests.post(url,data=json.dumps(block.__dict__, sort_keys=True))

def consensus():
    """
    Our simple consensus algorithm. If a longer valid chain is found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)
    for node in peers:
        response = requests.get('{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True
    return False

app.run(debug=True, port=8000)