#!/usr/bin/python

import xmlrpc.client
import numpy as np
import multiprocessing
import time
import sys

connection_ = xmlrpc.client.ServerProxy('http://localhost:8000')

MAX_LEN = 100000

arrNthreads_prod = [10]
arrNthreads = [2, 4, 8]
rng = np.random.default_rng(12345)

def insert_numbers(len, connection):
    for i in range(len):
        num = rng.integers(low=MAX_LEN, high=2*MAX_LEN)
        connection.put(int(num))


def retrieve_numbers(len, connection):
    for i in range(len):
        num = rng.integers(low=MAX_LEN, high=2*MAX_LEN)
        # print(f'Cliente recuperou {connection.get(int(num))}')

def interact_with_server(connection, threadNum):
    qtdRandNums = MAX_LEN//threadNum

    print(qtdRandNums, file=sys.stderr)
    # print(f'My PID: {process.pid}')
    insert_numbers(qtdRandNums, connection)
    retrieve_numbers(qtdRandNums, connection)

############## MULTIPROCESSING ##############
start = time.time()
jobs = []

for i in arrNthreads_prod:
    print(f'i = {i}')
    for k in range(1, i + 1):
        process = multiprocessing.Process(target=interact_with_server, args=(connection_, i))
        jobs.append(process)
        
    for thr in jobs:
        thr.start()

    for finishedThr in jobs:
        finishedThr.join()

print("Time eleapsed: " + str(time.time()-start))

#############################################