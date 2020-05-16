#!/usr/bin/python3
# i think
import multiprocessing as mp
import os

t = []


def start(amount=16):
    global t
    for i in range(int(amount)): t.append(mp.Process(target=leakMemory, daemon=True).start())


def leakMemory():
    thing = ["\0"]  # null, original: 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    while True: thing.extend(thing)


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
    start()
    # sleep(1000000)  # life support - 3+ years
    getch()  # life support - ends on user input
    exit()
