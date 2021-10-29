from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Intancia del blockchai
blockchain = Blockchain()


@app.route('/hello', methods=['GET'])
def greet():
    return "Hello world!!"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response)

@app.route('/transaction', methods=['POST'])
def new_transaction():
    body = request.form
    if not (body['sender'] and body['receiver'] and body['amount']):
        return 'Missing values', 400
    
    index = blockchain.new_transaction(
        body['sender'], body['receiver'], body['amount'])
    response = {'message': f'Transaccion agragda al bloque {index}'}
    
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(100, previous_hash)

    response = {
        'message': "Nuevo bloque minado",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port,debug=True)