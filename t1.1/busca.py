#!/home/uncanny/miniconda3/envs/PPD/bin/python

import numpy as np
import threading
import multiprocessing
import sys
import time
import random

def busca(needle, hay, lo, hi):
    for idx in range(lo, hi):
        if hay[idx] == needle:
            print(f'achou {needle} em array')
            return

def selectInterval(nthreads, arrLen):
    nhi=arrLen/nthreads
    nhiAux=nhi
    lo = 0

    hiArr = []

    hiArr.append((lo, int(nhi-1)))
    while nhiAux < arrLen:
        lo = nhiAux
        nhiAux+=nhi
        hiArr.append((int(lo), int(nhiAux-1)))

    return hiArr

arrLenGlobal = 50000000
nthreadsGlobal = 8
randArrGlobal = np.random.randint(1000000000, 2000000000, arrLenGlobal)
randPos = random.randrange(0, arrLenGlobal)
print(f'Posicao aleatoria do -1 sera em: {randPos}')
randArrGlobal[randPos] = -1
loHiArrGlobal = selectInterval(nthreadsGlobal, arrLenGlobal)
# Array com o numero de threads a ser utilizar depois que terminar a iteracao atual
iterThreadArrGlobal = [ j for j in [1 << i for i in range(nthreadsGlobal//2 + 1)][::-1] if j <= nthreadsGlobal]

start = time.time()
############## MULTIPROCESSING ##############
jobs = []
loHiArrGlobal = selectInterval(nthreadsGlobal, arrLenGlobal)
for threadNum, interval in zip(range(0, nthreadsGlobal), loHiArrGlobal):
    lo, hi = interval
    thread=multiprocessing.Process(target=busca, args=(-1, randArrGlobal, lo, hi))
    jobs.append(thread)

for thr in jobs:
    thr.start()

for finishedThr in jobs:
    finishedThr.join()

print("Tempo decorrido com 8 processos: " + str(time.time()-start))
print("\n\n\n\n")
start = time.time()
busca(-1, randArrGlobal, 0, len(randArrGlobal)-1)
print("Tempo decorrido com 1 processo: " + str(time.time()-start))