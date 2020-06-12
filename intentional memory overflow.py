#!/usr/bin/python3
import fcntl
import logging.handlers
import multiprocessing
import os
import sys
import termios
import threading
from time import sleep

amountOfProcesses = sys.argv[1] or 2
amountOfRam = sys.argv[2] or 16
memOverflow = logging.getLogger("Memory Overflow")

def start(amount=amountOfProcesses):
    global P
    for e in range(int(amount)):
        P.append(multiprocessing.Process(target=memoryOverflow, daemon=True))
        P[e].start()
        processes.debug(f"Started {P[e]}")


def processesCheck():
    global dead, amountOfProcesses
    amountOfProcesses = int(amountOfProcesses)
    deadProcesses = 0
    while deadProcesses < amountOfProcesses:
        deadProcesses = 0
        for q in P: deadProcesses = deadProcesses + 1 if not q.is_alive() else deadProcesses
    if not dead: processes.info("All of the processes are dead. Quitting")
    os.kill(os.getpid(), 15)


def memoryOverflow(ramLevel=amountOfRam):
    global finished
    d = "\x00" * (2 ** 30 * int(ramLevel))
    memOverflow.info(f"Finished with {ramLevel}GB ram taken")
    while True: sleep(1000000)


if __name__ == '__main__':
    processes = logging.getLogger("Processes")
    logging.basicConfig(level=logging.DEBUG)
    dead = False
    P = []
    def getch():
        fd = sys.stdin.fileno()
        oldterm, newattr, oldflags = termios.tcgetattr(fd), termios.tcgetattr(fd), fcntl.fcntl(fd, fcntl.F_GETFL)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        try:
            c = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return c
    logging.debug(f"{amountOfRam} {amountOfProcesses} {sys.argv}")
    start()
    threading.Thread(target=processesCheck, daemon=True).start()
    try:
        getch()  # life support - ends on user input
    except ValueError:
        pass
    logging.info("Terminating...")
    dead = True
    for i in P: i.terminate()
    exit()
