"""
macOS: 0.5 pixel sensitivity
Windows and Linux: 1 pixel sensitivity
macOS:
Trial and error
Windows notes:
Mouse definitely got slowed down (anti virus)
Linux notes:
Only top and left side of the screen
"""
import datetime
import tkinter as tk
from platform import system

from pynput import keyboard, mouse
from pynput.keyboard import Key

# The key combinations to check
# pixels away from side
# The currently active modifiers
# screen size to check for edge
COMBINATIONS, awayFrom, current, tNow, tCounter, = [{keyboard.Key.shift, keyboard.Key.esc}], \
                                                   3, set(), datetime.datetime.now(), 0
up, down, left, right = "↑", "↓", "←", "→"
screen_width, screen_height = tk.Tk().winfo_screenwidth(), tk.Tk().winfo_screenheight()
    

def to_left():
    mouse.Controller().move(-screen_width - awayFrom, 0)
    print(left, end=" ", flush=True)


def to_right():
    mouse.Controller().move(screen_width - awayFrom, 0)
    print(right, end=" ", flush=True)


def to_up():
    mouse.Controller().move(0, screen_height - awayFrom)
    print(up, end=" ", flush=True)


def to_down():
    mouse.Controller().move(0, -screen_height - awayFrom)
    print(down, end=" ", flush=True)


def exit_check(key):
    global current, COMBINATIONS
    # https://github.com/moses-palmer/pynput/issues/20#issuecomment-412714960
    if any([key in comb for comb in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in comb) for comb in COMBINATIONS):
            global tNow, tCounter
            tCounter += 1
            if datetime.datetime.now() - tNow < datetime.timedelta(seconds=1) and tCounter > 1:
                tCounter = 0
                print("\nUn-initialized")
                L.stop()
                return False
            else:
                tNow = datetime.datetime.now()
                current = set()


def move_to(x, y, pixelSen=1):
    if allowed:
        if -pixelSen <= x <= pixelSen:
            to_right()
        elif screen_width - pixelSen <= x < screen_width + pixelSen:
            to_left()
        elif -pixelSen <= y <= pixelSen:
            to_up()
        elif screen_height + pixelSen > y >= screen_height - pixelSen:
            to_down()


def on_release(key):
    global allowed
    if key == Key.ctrl_r or key == Key.cmd_r:
        allowed = not allowed
        if allowed:
            print("\nSoftware control gained")
        else:
            print("\nSoftware control lost")
    return exit_check(key)


def start(macOS=False):
    global L, COMBINATIONS
    if macOS: COMBINATIONS = [{keyboard.Key.ctrl, keyboard.Key.esc}, {keyboard.Key.alt, keyboard.Key.esc}]
    keyboard.Listener(on_release=on_release).start()
    with mouse.Listener(on_move=move_to) as L:
        L.join()


if __name__ == '__main__':
    allowed, text, sys, isMacOS = True, "Initialized\nUse right control/right command to pause/resume\nQuit " \
                                        "combination:", system(), False
    if sys == "Darwin":
        print("Mac, Stable\n{0}\nCtrl+Esc then Alt+Esc".format(text))
        isMacOS = True
    elif sys == "Windows":
        print("Windows\nThis is maybe unstable\n{0}\nShift+Esc".format(text))
    elif sys == "Linux":
        print("Linux\nUntested, unstable, and unfinished. It will not work yet\n{0}Shift+Esc".format(text))
    else:
        print("System unknown, this might not work properly. Using default\n{0}".format(text))
    start(macOS=isMacOS)
