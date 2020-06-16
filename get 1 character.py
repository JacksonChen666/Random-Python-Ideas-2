#!/usr/bin/env python3
import os

if os.name == 'nt':
    import msvcrt
    def g(): return msvcrt.g().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    try: old_settings = termios.tcgetattr(fd)
    except termios.error: print("Cannot get input, so idk")
    def g():
        try: tty.setraw(sys.stdin.fileno()); ch = sys.stdin.read(1)
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        s = ch
        return s

while True:
    print(ord(g()))
