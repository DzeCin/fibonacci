'''
Utils module containing some usefull functions
'''

from math import isqrt
import msgpack
from flask import make_response, jsonify, Response


def output(status_code: int, msg: object, msgpack_output) -> Response:
    if msgpack_output:
        return make_response(msgpack.dumps(msg), status_code)
    return make_response(jsonify(msg), status_code)


def is_fibonacci_number(n: int) -> bool:
    if n < 0:
        return False
    if n == 0:
        return True
    return (5 * n**2 + 4) == isqrt(5 * n**2 + 4) ** 2 or (5 * n**2 - 4) == isqrt(5 * n**2 - 4) ** 2


def is_integer(n: any) -> bool:
    try:
        return isinstance(n, int)
    except:
        return False


def next_fibonacci_number(n: int) -> int:
    if n == 0:
        return 1
    if (5 * n**2 + 4) == isqrt(5 * n**2 + 4) ** 2:
        next_number = (n + isqrt(5 * n**2 + 4)) // 2
    else:
        next_number = (n + isqrt(5 * n**2 - 4)) // 2
    return next_number


def process_request(number: any, msgpack_output: bool) -> Response:
    if not is_integer(number):
        return output(400, {'error': 'Not an integer'}, msgpack_output)
    if not is_fibonacci_number(number):
        return output(400, {'error': 'Not a fibonnaci number'}, msgpack_output)
    return output(200, {'n': next_fibonacci_number(number)}, msgpack_output)
