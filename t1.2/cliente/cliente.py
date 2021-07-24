#!/usr/bin/python

import xmlrpc.client
import numpy as np

connection_ = xmlrpc.client.ServerProxy('http://localhost:8000')
connection_.put(46544)
print(f'Recebi do servidor: {connection_.get(46544)}')
print(f'Recebi do servidor: {connection_.get(1)}')