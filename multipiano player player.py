"""
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
import re
from time import sleep

from pynput.keyboard import Controller, Key


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
        if str(i).islower():
            k.type(i)
        else:
            k.press(Key.shift)
            k.type(i)
            k.release(Key.shift)
        sleep(0.25)


def hold(key, time, kba):
    kba.press(key)
    sleep(time)
    kba.release(key)


def delay(time):
    sleep(time)


def readFile():
    with open("Play.txt") as f:
        return f.read()


def recorder():
    pass


if __name__ == '__main__':
    main()
