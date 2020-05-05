#!/usr/bin/python3
# i think
import multiprocessing as mp
from time import sleep

t = []
processes = 16


def start():
    global t
    for i in range(int(processes)):
        t.append(mp.Process(target=leakMemory, daemon=True))  # stop when main process is stopped
        t[len(t) - 1].start()


def leakMemory():
    thing = [0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]
    while True:
        thing.extend(thing)


if __name__ == '__main__':
    start()
    while True:  # don't delete!!! without support it will all die!!!
        sleep(0xf)
