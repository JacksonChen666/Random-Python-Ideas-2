"""
Replacement:
https://web.archive.org/web/20160726001324/https://dl.dropboxusercontent.com/u/62490156/MPPMidiPlayer.jar

valid keys:
1245789-=qwertyuiop[]asfgjkl'zxcvbnm,./!@$%&*(_+QWERTYUIOP{}ASFGJKL"ZXCVBNM<>?
invalid keys:
360dh;#^)_|DH:/space//newline/ and everything else outside of the qwerty keyboard
a presses a that's all
a[150] hold key a for 150ms
a [150] a then delay 150ms
(as) together notes
ctrl{a s} play normally with control held down or cap locks on
shift{a s} play with shift (cap characters are possible, but it can break)
the recorder records key presses and delays between each key and the hold time then saves to list then writes them down
"""
import random
import re

from time import sleep
from pynput.keyboard import Controller, Key, Listener

bpm = 100
minHoldTime = 0.01
maxHoldTime = 0.1


def main():
    global notes
    notes = readFile()
    parsedNotes = parser(notes)
    player(parsedNotes)


def parser(file):
    allKeys = re.findall("(?:[^360\\\dh;#^)_|DH:{}\n])", file)
    return allKeys


def player(notesList):
    k = Controller()
    s = sleep
    ru = random.uniform
    s(1)
    for i in notesList:
        if str(i) == " ":
            pass
        elif re.search("[,./'\[\]]+", i) or str(i).islower() or int(i):
            hold(i, ru(minHoldTime, maxHoldTime), k)
        elif not str(i).islower():
            k.press(Key.shift)
            hold(i, ru(minHoldTime, maxHoldTime), k)
            k.release(Key.shift)
        print(i, end="")
        s(1 / bpm)
    return True


def hold(key, time, kba):
    kba.press(key)
    sleep(time)
    kba.release(key)


def readFile():
    try:
        with open("Play.txt") as f:
            return f.read()
    except FileNotFoundError:
        print("File not found, make sure your file is named \"Play.txt\". Using default notes.")
        return "b b., m j jj, jvb bu7u7u b bu7u7u ccccbbbbvvvvmmmm,,,,,,,,,,,,b c"


def recorder():
    with open("Play.txt", "w"): pass
    print("Recording...")
    with Listener(on_release=writeToFile) as h: h.join()


def writeToFile(text):
    with open("Play.txt", "a") as append:
        try:
            if re.search("(?:[^360\\\dh;#^)_|DH:{}\n])", text.char): append.write(str(text.char))
        except AttributeError:
            if text == Key.space:
                append.write(" ")
            elif text == Key.backspace:
                with open("Play.txt", "r+") as rewrite:
                    rewrite.write(rewrite.read()[:-1])
            elif text == Key.enter:
                append.write("\n")
            elif text == Key.esc:
                return False  # stop listener
            else:
                print("Oops, invalid character, character is {}".format(str(text)))


if __name__ == '__main__':
    recorder()
