"""
Also, i quit doing this from today to today because theres a thing

valid keys:
1245789-=qwertyuiop[]asfgjkl'zxcvbnm,./!@$%&*(_+QWERTYUIOP{}ASFGJKL"ZXCVBNM<>?
invalid keys:
360dh;#^)_|DH:/space//newline/ and everything else outside of the qwerty keyboard
default delay 10ms
default delay with space 20ms
a presses a that's all
a[150] press a, and hold it for 150ms
(as) is grouped notes that play together
ctrl{a s} play normally with control held down or cap locks on
shift{a s} play with shift (caps won’t work cause detection)
the recorder records key presses and delays between each key and the hold time then saves to list
"""
import random
import re
from time import sleep

from pynput.keyboard import Controller, Key

bpm = 100  # tf it's opposite i can't math


def main():
    global notes
    notes = readFile()
    parsedNotes = parser(notes)
    player(parsedNotes)


def parser(file):
    global allKeys
    allKeys = re.findall("(?:[^360\\\dh;#^)_|DH:{}\n])", file)
    return allKeys


def player(notes):
    sleep(1)
    k = Controller()
    for i in notes:
        if str(i) == " ":
            pass
        elif re.search("[,./'\[\]]+", i) or str(i).islower() or int(i):
            k.press(i)
            sleep(random.uniform(0.025, 0.050))
            k.release(i)
        elif not str(i).islower():
            k.press(Key.shift)
            sleep(random.uniform(0.025, 0.050))
            k.press(i)
            sleep(random.uniform(0.025, 0.050))
            k.release(i)
            sleep(random.uniform(0.025, 0.050))
            k.release(Key.shift)
        print(i, end="")
        sleep(bpm / 60 / 10)
    return True


def hold(key, time, kba):
    kba.press(key)
    sleep(time)
    kba.release(key)


def delay(time):
    sleep(time)


def readFile():
    try:
        with open("Play.txt") as f:
            return f.read()
    except FileNotFoundError:
        print("File not found, make sure your file is named \"Play.txt\". Using default notes.")
        return "b b., m j jj, jvb bu7u7u b bu7u7u ccccbbbbvvvvmmmm,,,,,,,,,,,,b c"


def recorder():
    pass


if __name__ == '__main__':
    main()
