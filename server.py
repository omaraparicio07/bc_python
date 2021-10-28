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
    return jsonify({"greet": "Hello world!!"}), 201


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port,debug=True)