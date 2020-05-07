#!/usr/bin/python3
# used for testing purposes, like what kill signal does what
import multiprocessing as mp
from time import sleep


def doNothing():
    while True:
        sleep(0xffffff)  # which equals to TOO MANY SECONDS


def startProcesses():
    t = []  # shut up about being t
    for i in range(32 - 1):
        t.append(mp.Process(target=doNothing))
        t[i].start()
    doNothing()


if __name__ == '__main__':
    startProcesses()
