ref: https://r-knott.surrey.ac.uk/Fibonacci/fibtable.html

ref: https://github.com/msgpack/msgpack/blob/master/spec.md#int-format-family

ref: https://math.stackexchange.com/a/3392157

### Purpose
This repo contains a web server which can return the fibonacci number after the one sent.

### Tech stack/Structure
- Python3 + Flask
- utils/ contains the utils functions
- main.py is the entrypoint
- test/ contains a few tests

### Setup
- Install dependencies: 

      pip3 install -r requirements.txt

- Run the server 

      python3 main.py

OR

- Build the docker image and run it

### Endpoint specification
There are 2 enpoints:
#### GET /health
simple health endpoint returning 200,ok
#### POST /next_fibonacci_number
- Require header 

        Content-Type: application/json (for json input) 
        OR
        Content-Type: application/msgpack (for msgpack inputs)

- Require payload in this format :

        {'n': number} 

    where number is an integer (it will not work wth float and number as string)
- Optional:

        ?output_type=msgpack if the output needs to be in msgpack format (in json by default)

- Max integer for both input and output is the unsigned 2**64 - 1 for msgpack
- There is no limit for the json format as only the "int" type is used in the server

### Live test
- A docker image has been created at dockerhub.io/dzenanc/fibonacci.
- The server has been deployed and is live at fibo.cindrak.com

### Exemples

    # curl -k -X POST "https://fibo.cindrak.com/next_fibonacci_number" -H "Content-Type: application/json" -d '{"n": 420196140727489673}'
    # {"n":679891637638612258}

    # curl -k -X POST "https://fibo.cindrak.com/next_fibonacci_number?output_type=msgpack" -H "Content-Type: application/json" -d '{"n": 420196140727489673}'
