#!/usr/bin/env python

'''
Entryoint for the fibonacci number server
'''

from utils import server

app = server.app

if __name__ == '__main__':
    app.run(debug=False)
