#!/home/uncanny/miniconda3/envs/PPD/bin/python

import numpy as np
import threading
import multiprocessing
import sys
import time

def partition(arr,l,h):
    i = ( l - 1 )
    x = arr[h]
  
    for j in range(l , h):
        if   arr[j] <= x:
  
            # increment index of smaller element
            i = i+1
            arr[i],arr[j] = arr[j],arr[i]
  
    arr[i+1],arr[h] = arr[h],arr[i+1]
    return (i+1)
  
# Function to do Quick sort
# arr[] --> Array to be sorted,
# l  --> Starting index,
# h  --> Ending index
def quickSort(arr,l,h):
  
    # Create an auxiliary stack
    size = h - l + 1
    stack = [0] * (size)
  
    # initialize top of stack
    top = -1
  
    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h
  
    # Keep popping from stack while is not empty
    while top >= 0:
  
        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
  
        # Set pivot element at its correct position in
        # sorted array
        p = partition( arr, l, h )
  
        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
  
        # If there are elements on right side of pivot,
        # then push right side to stack
        if p+1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h

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


arrLenGlobal = 500000
nthreadsGlobal = 8
randArrGlobal = np.random.randint(1000000000, 2000000000, arrLenGlobal)
loHiArrGlobal = selectInterval(nthreadsGlobal, arrLenGlobal)

start = time.time()


############## MULTIPROCESSING ##############
jobs = []
for threadNum, interval in zip(range(0, nthreadsGlobal), loHiArrGlobal):
    lo, hi = interval
#     # print(f'Thread {threadNum} will be assigned to array {arr}')
    thread=multiprocessing.Process(target=quickSort, args=(randArrGlobal, lo, hi))
    jobs.append(thread)

for thr in jobs:
    thr.start()

for finishedThr in jobs:
    finishedThr.join()
############################################

# quickSort(randArr, 0, len(randArr)-1)
# print(randArr)

# quickSort(randArr, 0, (len(randArr)//2)-1)
# quickSort(randArr, (len(randArr)//2)-1, (len(randArr)-1))
# np.set_printoptions(threshold=sys.maxsize)

# for arr in spltArrGlobal:
#     print(arr)

print("Time eleapsed: " + str(time.time()-start))