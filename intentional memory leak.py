#!/usr/bin/python3
# i think
import multiprocessing as mp


def start():
    t = []
    for i in range(8):
        t.append(mp.Process(target=leakMemory))
        t[i].start()


def leakMemory():
    thing = [0xffffffffffffffffffffffffffffffff]  # 16 to the power of how many f in the list (32)
    while True:
        thing.extend(thing)


if __name__ == '__main__':
    start()
