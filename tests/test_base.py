'''
Test file for the fibonacci next number generator
'''

import json
import pytest
import msgpack
from utils import server
from utils import utils

@pytest.fixture
def fibo_client():
    '''
    App client fixture used in all the tests
    '''
    app = server.app
    app.testing = True
    return app.test_client()


def test_get_health(fibo_client):
    '''
    Test the health endpoint
    '''
    response = fibo_client.get('/health')
    assert response.status_code == 200


def test_is_fibonacci_number():
    '''
    Test if a number is a fibonacci number
    '''
    fibonacci_numbers=[420196140727489673, 43566776258854844738105 ,3416454622906707, 23416728348467685,
                       61305790721611591, 83621143489848422977, 4660046610375530309, 7540113804746346429,
                       1500520536206896083277, 1500520536206896083277]
    for i in fibonacci_numbers:
        assert utils.is_fibonacci_number(i)

def test_next_fibonacci_number():
    '''
    Check if the right results are returned for some random fibonacci numbers
    '''
    fibonacci = {3416454622906707:5527939700884757, 420196140727489673:679891637638612258,
                 43566776258854844738105:70492524767089125814114}
    for i in fibonacci:
        assert utils.next_fibonacci_number(i) == fibonacci[i]


def test_post_int_fibonacci_number_ok(fibo_client):
    '''
    Test with a correct a string fibonacci number
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': 34}),
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': 34}),
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': 34}),
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': 34}),
    )
    assert response_msgpack_json_output.status_code == 200
    assert response_msgpack_json_output.get_json() == {'n': 55}
    assert response_json_json_output.status_code == 200
    assert response_json_json_output.get_json() == {'n': 55}
    assert response_json_msgpack_output.status_code == 200
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {'n': 55}
    assert response_msgpack_msgpack_output.status_code == 200
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {'n': 55}


def test_post_str_fibonacci_number_nok(fibo_client):
    '''
    Test with a string instead of an int for n
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': '34.000'}),
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': '34.000'}),
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': '34.000'}),
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': '34.000'}),
    )
    assert response_msgpack_json_output.status_code == 400
    assert response_msgpack_json_output.get_json() == {'error': 'Not an integer'}
    assert response_json_json_output.status_code == 400
    assert response_json_json_output.get_json() == {'error': 'Not an integer'}
    assert response_json_msgpack_output.status_code == 400
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {'error': 'Not an integer'}
    assert response_msgpack_msgpack_output.status_code == 400
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {'error': 'Not an integer'}


def test_post_float_fibonacci_number_nok(fibo_client):
    '''
    Test with a float instead of an int for n
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': 34.000}),
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': 34.000}),
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': 34.000}),
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': 34.000}),
    )
    assert response_msgpack_json_output.status_code == 400
    assert response_msgpack_json_output.get_json() == {'error': 'Not an integer'}
    assert response_json_json_output.status_code == 400
    assert response_json_json_output.get_json() == {'error': 'Not an integer'}
    assert response_json_msgpack_output.status_code == 400
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {'error': 'Not an integer'}
    assert response_msgpack_msgpack_output.status_code == 400
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {'error': 'Not an integer'}


def test_post_multiple_fibonacci_number_ok(fibo_client):
    '''
    Test multiple fibonacci number
    Number (and output) must be at most 2**64-1 for this specific test because both msgpack (unsigned int64) and json (no limit) are used. 
    input: msgpack and json
    output: msgpack and json
    '''
    fibonacci = {3416454622906707:5527939700884757, 308061521170129:498454011879264,
                 7540113804746346429:12200160415121876738}
    for n in fibonacci:
        response_msgpack_json_output = fibo_client.post(
            '/next_fibonacci_number',
            headers={'Content-Type': 'application/msgpack'},
            data=msgpack.dumps({'n': n}),
        )
        response_json_msgpack_output = fibo_client.post(
            '/next_fibonacci_number?output_type=msgpack',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'n': n}),
        )
        assert response_msgpack_json_output.status_code == 200
        assert response_msgpack_json_output.get_json() == {'n': fibonacci[n]}
        assert response_json_msgpack_output.status_code == 200
        assert msgpack.loads(response_json_msgpack_output.get_data()) == {'n': fibonacci[n]}

def test_post_no_header_fibonacci_number_nok(fibo_client):
    '''
    Test with no header
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number', data=msgpack.dumps({'n': 34})
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number', data=json.dumps({'n': 34})
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack', data=msgpack.dumps({'n': 34})
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack', data=json.dumps({'n': 34})
    )
    assert response_msgpack_json_output.status_code == 400
    assert response_msgpack_json_output.get_json() == {
        'error': 'Unsupported content type'
    }
    assert response_json_json_output.status_code == 400
    assert response_json_json_output.get_json() == {'error': 'Unsupported content type'}
    assert response_json_msgpack_output.status_code == 400
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {
        'error': 'Unsupported content type'
    }
    assert response_msgpack_msgpack_output.status_code == 400
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {
        'error': 'Unsupported content type'
    }


def test_post_wrong_header_fibonacci_number_nok(fibo_client):
    '''
    Test with wrong header
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/json'},
        data=msgpack.dumps({'n': 34}),
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/msgpack'},
        data=json.dumps({'n': 34}),
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/json'},
        data=msgpack.dumps({'n': 34}),
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/msgpack'},
        data=json.dumps({'n': 34}),
    )
    assert response_msgpack_json_output.status_code == 400
    assert response_msgpack_json_output.get_json() == {
        'error': 'Input data is incorrectly formatted'
    }
    assert response_json_json_output.status_code == 400
    assert response_json_json_output.get_json() == {
        'error': 'Input data is incorrectly formatted'
    }
    assert response_json_msgpack_output.status_code == 400
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {
        'error': 'Input data is incorrectly formatted'
    }
    assert response_msgpack_msgpack_output.status_code == 400
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {
        'error': 'Input data is incorrectly formatted'
    }


def test_post_wrong_fibonacci_number_nok(fibo_client):
    '''
    Test with wrong fibonacci number
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': -34}),
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': -34}),
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': -34}),
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': -34}),
    )
    assert response_msgpack_json_output.status_code == 400
    assert response_msgpack_json_output.get_json() == {
        'error': 'Not a fibonnaci number'
    }
    assert response_json_json_output.status_code == 400
    assert response_json_json_output.get_json() == {'error': 'Not a fibonnaci number'}
    assert response_json_msgpack_output.status_code == 400
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {
        'error': 'Not a fibonnaci number'
    }
    assert response_msgpack_msgpack_output.status_code == 400
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {
        'error': 'Not a fibonnaci number'
    }


def test_post_extreme_cases_fibonacci_number_ok(fibo_client):
    '''
    Test with extreme cases:
      - msgpack only supports unsigned int up to 2**64 - 1
      - 0 is a special case because formula is not supported for 0
    input: msgpack and json
    output: msgpack and json
    '''
    response_msgpack_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': 18446744073709551615}),
    )
    response_json_json_output = fibo_client.post(
        '/next_fibonacci_number',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': 18446744073709551615}),
    )
    response_msgpack_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/msgpack'},
        data=msgpack.dumps({'n': 0}),
    )
    response_json_msgpack_output = fibo_client.post(
        '/next_fibonacci_number?output_type=msgpack',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'n': 0}),
    )
    assert response_msgpack_json_output.status_code == 400
    assert response_msgpack_json_output.get_json() == {
        'error': 'Not a fibonnaci number'
    }
    assert response_json_json_output.status_code == 400
    assert response_json_json_output.get_json() == {'error': 'Not a fibonnaci number'}
    assert response_json_msgpack_output.status_code == 200
    assert msgpack.loads(response_json_msgpack_output.get_data()) == {'n': 1}
    assert response_msgpack_msgpack_output.status_code == 200
    assert msgpack.loads(response_msgpack_msgpack_output.get_data()) == {'n': 1}
