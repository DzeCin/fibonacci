'''
The endpoints for the server
'''
from flask import Flask, request
import msgpack
from utils import utils

app = Flask(__name__)


@app.route('/health')
def health():
    return {'health': 'OK'}, 200


@app.route('/next_fibonacci_number', methods=['POST'])
def next_fibonacci_number():
    msgpack_output = request.args.get('output_type') == 'msgpack'
    content_type = request.headers.get('Content-Type')
    try:
        if content_type == 'application/json':
            number = request.get_json()['n']
        elif content_type == 'application/msgpack':
            number = msgpack.loads(request.get_data())['n']
        else:
            return utils.output(
                400, {'error': 'Unsupported content type'}, msgpack_output
            )
        return utils.process_request(number, msgpack_output)
    except Exception:
        return utils.output(
            400, {'error': 'Input data is incorrectly formatted'}, msgpack_output
        )
