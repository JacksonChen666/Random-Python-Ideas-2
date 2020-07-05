from random import shuffle
from time import sleep, time
from sys import argv

def returnShuffle(lists):
    shuffle(lists)
    return lists

num = int(argv[1]) if len(argv) >= 2 else 5
oList = [i for i in range(num)]
nList = returnShuffle(oList.copy())
iteration = 0
bestIter = 100 ** 100
timeTotal = 0
printPerIteration = int(argv[2]) if len(argv) >= 3 and int(argv[2]) > 0 else 1000

print("List size: %s" % len(oList))
sleep(0.1)
while bestIter > 0:
    print(f"Iterations: {iteration}", end=" \r", flush=True)
    while oList != nList:
        t0 = time()
        shuffle(nList)
        t1 = time()
        timeTotal += (t1 - t0) * 1000
        iteration += 1
        if iteration % printPerIteration == 0: print(f"Iterations: {iteration}", end=" \r", flush=True)
    if iteration < bestIter:
        bestIter = iteration
        print(f"New best iterations: {bestIter} in {round(timeTotal, 2)}ms", end=" \n", flush=True)
    iteration, timeTotal = 0, 0
    shuffle(nList)
