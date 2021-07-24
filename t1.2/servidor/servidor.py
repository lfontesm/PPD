#!/usr/bin/python

from xmlrpc.server import *

hashTable = {}

def put(value):
    valueStr = str(value)
    hashTable[valueStr] = value

def get(key):
    keyStr = str(key)
    return hashTable.get(keyStr)

server_ = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
server_.register_function(put, 'put')
server_.register_function(get, 'get')

server_.serve_forever()