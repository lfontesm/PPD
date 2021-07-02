#!/home/uncanny/miniconda3/envs/PPD/bin/python

import numpy as np
import threading
import sys
import time

def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot
  
    for j in range(low, high):
  
        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:
  
            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
  
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
  
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)
  
        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

arrLenGlobal = 500000
nthreadsGlobal = 8
randArr = np.random.randint(1000000000, 2000000000, arrLenGlobal)
print(""" 
        ARRAY NOT SORTED
""")
print(randArr)

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

loHiArr = selectInterval(nthreadsGlobal,arrLenGlobal)
print(loHiArr)

print(""" 
        ARRAY SORTED
""")

start = time.time()


# while True:
jobs = []
for threadNum in range(0, nthreadsGlobal):
    lo, hi = loHiArr[threadNum]
    thread=threading.Thread(target=quickSort(randArr, lo, hi))
    jobs.append(thread)

for thr in jobs:
    thr.start()

for finishedThr in jobs:
    finishedThr.join()

# nthreadsGlobal = nthreadsGlobal//2
# if nthreadsGlobal >= 1:
#     loHiArr = selectInterval(nthreadsGlobal, arrLenGlobal)
#     print(nthreadsGlobal)
#     print(loHiArr)
# else:
#     break


# np.set_printoptions(threshold=sys.maxsize)
# print(randArr)
# print("Time eleapsed: " + str(time.time()-start))