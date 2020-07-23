#!/usr/bin/python3
from fcntl import fcntl, F_GETFL, F_SETFL
import logging.handlers
from multiprocessing import Process
from os import kill, getpid
from sys import argv, stdin
from termios import tcgetattr, ICANON, ECHO, TCSANOW, tcsetattr, TCSAFLUSH
from threading import Thread
from time import sleep

amountOfProcesses = argv[1] or 2
amountOfRam = argv[2] or 16
memOverflow = logging.getLogger("Memory Overflow")


def start(amount=amountOfProcesses):
    global P
    for e in range(int(amount)):
        P.append(Process(target=memoryOverflow, daemon=True))
        P[e].start()
        processes.debug(f"Started {P[e]}")


def processesCheck():
    global dead, amountOfProcesses
    amountOfProcesses = int(amountOfProcesses)
    deadProcesses = 0
    while deadProcesses < amountOfProcesses:
        deadProcesses = 0
        sleep(1)
        for q in P: deadProcesses = deadProcesses + 1 if not q.is_alive() else deadProcesses
    if not dead: processes.info("All of the processes are dead. Quitting")
    kill(getpid(), 9)


def memoryOverflow(ramLevel=amountOfRam):
    d = "\x00" * (2 ** 30 * int(ramLevel))
    memOverflow.info(f"Finished with {ramLevel}GB ram taken")
    while True: sleep(1000000)


if __name__ == '__main__':
    processes = logging.getLogger("Processes")
    logging.basicConfig(level=logging.DEBUG)
    dead = False
    P = []
    def getch():
        fd = stdin.fileno()
        oldterm, newattr, oldflags = tcgetattr(fd), tcgetattr(fd), fcntl(fd, F_GETFL)
        newattr[3] = newattr[3] & ~ICANON & ~ECHO
        tcsetattr(fd, TCSANOW, newattr)
        fcntl(fd, F_SETFL, oldflags)
        try:
            c = stdin.read(1)
        finally:
            tcsetattr(fd, TCSAFLUSH, oldterm)
            fcntl(fd, F_SETFL, oldflags)
        return c
    logging.debug(f"{amountOfRam} {amountOfProcesses} {argv}")
    start()
    Thread(target=processesCheck, daemon=True).start()
    try:
        getch()  # life support - ends on user input
    except ValueError:
        pass
    logging.info("Terminating...")
    dead = True
    for i in P: i.terminate()
    exit()
