#!/usr/bin/python3
import multiprocessing as mp
import os
import sys
import threading as t
from time import sleep

P = []
amountOfProcesses = 1
amountOfRam = 1
dead = False


def start(amount=amountOfProcesses):
    global P
    for e in range(int(amount)):
        P.append(mp.Process(target=memoryOverflow, daemon=True))
        P[e].start()


def processesCheck():
    global dead, amountOfProcesses
    amountOfProcesses = int(amountOfProcesses)
    while True:
        deadProcesses = 0
        for q in P: deadProcesses = deadProcesses + 1 if not q.is_alive() else deadProcesses
        if deadProcesses >= amountOfProcesses:
            if not dead: sys.stderr.writelines("All of the processes are dead. Quitting")
            exit(1)


def memoryOverflow():
    d = "\x00" * (2 ** 30 * amountOfRam)
    # d = "\xf4\x8f\xbf\xbf" * (2 ** 30 * amountOfRam) / 4
    while True: sleep(1000000)


if __name__ == '__main__':
    if os.name == 'nt':
        import msvcrt
        def getch(): return msvcrt.g().decode()
    else:
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        def getch():
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
    amountOfRam, amountOfProcesses = sys.argv[1:]
    print(amountOfRam, amountOfProcesses, sys.argv)
    start()
    t.Thread(target=processesCheck, daemon=True).start()
    try: getch()  # life support - ends on user input
    except ValueError: pass
    sys.stdout.writelines("Terminating...")
    dead = True
    for i in P: i.terminate()
    exit()
