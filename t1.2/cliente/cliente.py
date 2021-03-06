#!/usr/bin/python

import xmlrpc.client
import numpy as np
import multiprocessing
import time
import sys

# Conexao com o servidor
connection_ = xmlrpc.client.ServerProxy('http://localhost:8000')

# Quantidade de numeros aleatorios para inserir
MAX_LEN = 100000

# Mudar o numero de threads a ser usada
K = 4

# Objeto gerador de numeros aleatorios com seed de 12345
rng = np.random.default_rng(12345)

def insert_numbers(len, connection):
    for i in range(len):
        num = rng.integers(low=MAX_LEN, high=2*MAX_LEN)
        connection.put(int(num))


def retrieve_numbers(len, connection):
    for i in range(len):
        num = rng.integers(low=MAX_LEN, high=2*MAX_LEN)
        connection.get(int(num))

def interact_with_server(connection, threadNum):
    qtdRandNums = MAX_LEN//threadNum

    insert_numbers(qtdRandNums, connection)
    retrieve_numbers(qtdRandNums, connection)

############## MULTIPROCESSING ##############
start = time.time()
jobs = []

for k in range(1, K + 1):
    process = multiprocessing.Process(target=interact_with_server, args=(connection_, K))
    jobs.append(process)
        
for thr in jobs:
    thr.start()

for finishedThr in jobs:
    finishedThr.join()

print("Time elapsed: " + str(time.time()-start))

#############################################