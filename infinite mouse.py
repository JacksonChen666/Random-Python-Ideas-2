# only need to install pynput but its automated already
# key comb: https://github.com/moses-palmer/pynput/issues/20#issuecomment-412714960
import datetime
import tkinter as tk
from platform import system
from time import sleep

try:
    from pynput import mouse, keyboard
    from pynput.keyboard import Key
except ImportError:
    from subprocess import run

    print("If you have an antivirus, the library installation process maybe blocked or thrown sandbox to confirm it "
          "does not do any harm. If the installation process is blocked, please manually install the following "
          "libraries: pynput")
    try:
        print("Attempting to install library with pip...")
        run("pip install pynput", shell=True, check=True)
    except:
        print("Attempting to install library with pip3...")
        run("pip3 install pynput", shell=True, check=True)
    finally:
        from pynput import mouse, keyboard
        from pynput.keyboard import Key

        print("Done")

# The key combinations to check
COMBINATIONS = [{keyboard.Key.ctrl, keyboard.Key.esc}, {keyboard.Key.alt, keyboard.Key.esc}]

# pixels away from side
awayFrom = 3

# The currently active modifiers
current = set()

up, down, left, right = "↑", "↓", "←", "→"
tNow = datetime.datetime.now()
tCounter = 0

# screen size to check for edge
screen_width, screen_height = tk.Tk().winfo_screenwidth(), tk.Tk().winfo_screenheight()


def toLeft(): mouse.Controller().move(-screen_width - awayFrom, 0); print(left, end=" ")
def toRight(): mouse.Controller().move(screen_width - awayFrom, 0); print(right, end=" ")
def toUp(): mouse.Controller().move(0, screen_height - awayFrom); print(up, end=" ")
def toDown(): mouse.Controller().move(0, -screen_height - awayFrom); print(down, end=" ")


def exitCheck(key):
    global current, COMBINATIONS
    if any([key in comb for comb in COMBINATIONS]):  # LINE 2
        current.add(key)
        if any(all(k in current for k in comb) for comb in COMBINATIONS):
            global tNow, tCounter; tCounter += 1
            if datetime.datetime.now() - tNow < datetime.timedelta(seconds=1) and tCounter > 1: tCounter = 0; print("\nUn-initialized"); return False
            else: tNow = datetime.datetime.now(); current = set()


def moveTo(x, y, pixelSen=0.5):
    if allowed:
        if -pixelSen <= x <= pixelSen: toRight()
        elif screen_width - pixelSen <= x < screen_width + pixelSen: toLeft()
        elif -pixelSen <= y <= pixelSen: toUp()
        elif screen_height + pixelSen > y >= screen_height - pixelSen: toDown()


def on_move(x, y): moveTo(x, y)
def on_press(key): pass


def on_release(key):
    if key == Key.ctrl_r or key == Key.cmd_r:
        global allowed; allowed = not allowed
        if allowed: print("\nSoftware control gained")
        else: print("\nSoftware control lost")
    exitCheck(key)


def mac_on_release(key):
    if key == Key.cmd_r:
        global allowed; allowed = not allowed
        if allowed: print("\nSoftware control gained")
        else: print("\nSoftware control lost")
    exitCheck(key)


def win_on_move(x, y): moveTo(x, y, 1)
def win_on_press(key): on_press(key)


def win_on_release(key):
    global allowed, COMBINATIONS
    COMBINATIONS = [{keyboard.Key.shift, keyboard.Key.esc}]
    if key == Key.ctrl_r:
        allowed = not allowed
        if allowed: print("Software control gained")
        else: print("\nSoftware control lost")
    exitCheck(key)


def start(Windows=False, macOS=False, Linux=False):
    if Windows:
        keyboard.Listener(on_release=win_on_release, on_press=win_on_press).start()
        with mouse.Listener(on_move=win_on_move) as L: L.join()
    elif macOS:
        keyboard.Listener(on_release=mac_on_release, on_press=on_press).start()
        with mouse.Listener(on_move=on_move) as L: L.join()
    else:
        keyboard.Listener(on_release=on_release, on_press=on_press).start()
        with mouse.Listener(on_move=on_move) as L: L.join()


if __name__ == '__main__':
    s, allowed, text = 1, True, "Initialized\nUse right control/right command to pause/resume\nQuit combination:"
    if system() == "Darwin": print("Mac, Stable\n{0}\nCtrl+Esc then Alt+Esc".format(text)); start(macOS=True)
    elif system() == "Windows": print("Windows\nThis is unstable and may slow down your mouse harshly\n{0}\nShift+Esc".format(text)); start(Windows=True)
    elif system() == "Linux": print("Linux\nUntested, unstable, and unfinished. It will not work yet\n{0}".format(text)); start(Linux=True)
    else: print("System unknown, this might not work properly. Using default\n{0}".format(text)); start()
    while True: sleep(1000000)
