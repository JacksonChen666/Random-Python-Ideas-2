#!/usr/bin/env python3
from random import shuffle
from time import sleep, time

def returnShuffle(lists):
    shuffle(lists)
    return lists


oList = [i for i in range(5)]
nList = returnShuffle(oList.copy())
iteration = 0
bestIter = 100 ** 100
timeTotal = 0
printPerIteration = 1000

print("List size: %s" % len(oList))
sleep(0.1)
while bestIter > 0:
    while oList != nList:
        t0 = time()
        shuffle(nList)
        t1 = time()
        timeTotal += (t1 - t0) * 1000
        iteration += 1
        if iteration % printPerIteration == 0: print(f"Iterations: {iteration} ", end="\r", flush=True)
    if iteration < bestIter:
        bestIter = iteration
        print(f"New best iterations: {bestIter} in {round(timeTotal, 2)}ms ", flush=True)
    iteration, timeTotal = 0, 0
    shuffle(nList)
