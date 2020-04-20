# only need to install pynput but its automated already
# key comb: https://github.com/moses-palmer/pynput/issues/20#issuecomment-412714960
import datetime
import tkinter as tk
from platform import system

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
COMBINATIONS = [
    {keyboard.Key.ctrl, keyboard.Key.esc},
    {keyboard.Key.alt, keyboard.Key.esc}
]

# pixels away from side
awayFrom = 3

# The currently active modifiers
current = set()

tnow = datetime.datetime.now()
tcounter = 0

# screen size to check for edge
screen_width = tk.Tk().winfo_screenwidth()
screen_height = tk.Tk().winfo_screenheight()


def on_move(x, y):
    # print("{} {}".format(x, y))
    if allowed:  # well that happened
        if -0.5 <= x <= 0.5:
            mouse.Controller().move(screen_width - awayFrom, 0)
            print("->", end=" ")
        elif screen_width - 0.5 <= x < screen_width + 0.5:
            mouse.Controller().move(-screen_width - awayFrom, 0)
            print("<-", end=" ")
        elif -0.5 <= y <= 0.5:
            mouse.Controller().move(0, screen_height - awayFrom)
            print("^", end=" ")
        elif screen_height + 0.5 > y >= screen_height - 0.5:
            mouse.Controller().move(0, -screen_height - awayFrom)
            print("V", end=" ")


def on_press(key):
    pass


def on_release(key):
    global allowed, current
    if key == Key.ctrl_r or key == Key.cmd_r:
        allowed = not allowed
        if allowed:
            print("\nSoftware control gained")
        else:
            print("\nSoftware control lost")

    if any([key in comb for comb in COMBINATIONS]):  # LINE 2
        current.add(key)
        if any(all(k in current for k in comb) for comb in COMBINATIONS):
            global tnow, tcounter
            tcounter += 1
            if datetime.datetime.now() - tnow < datetime.timedelta(seconds=1):
                if tcounter > 1:
                    tcounter = 0
                    listener.stop()
                    print("\nUn-initialized")
            else:
                tnow = datetime.datetime.now()
                current = set()


def mac_on_move(x, y):  # mac and mainly for myself actually
    on_move(x, y)


def mac_on_press(key):
    on_press(key)


def mac_on_release(key):
    global allowed, current
    if key == Key.cmd_r:
        allowed = not allowed
        if allowed:
            print("\nSoftware control gained")
        else:
            print("\nSoftware control lost")

    if any([key in comb for comb in COMBINATIONS]):  # LINE 2
        current.add(key)
        if any(all(k in current for k in comb) for comb in COMBINATIONS):
            global tnow, tcounter
            tcounter += 1
            if datetime.datetime.now() - tnow < datetime.timedelta(seconds=1):
                if tcounter > 1:
                    tcounter = 0
                    listener.stop()
                    print("\nUn-initialized")
            else:
                tnow = datetime.datetime.now()
                current = set()


def win_on_move():  # windows version
    # print("{} {}".format(x, y))
    if allowed:  # well that happened
        if -1.0 <= x <= 1:
            mouse.Controller().move(screen_width - awayFrom, 0)
            print("->", end=" ")
        elif screen_width - 1 <= x < screen_width + 1:
            mouse.Controller().move(-screen_width - awayFrom, 0)
            print("<-", end=" ")
        elif -1.0 <= y <= 1:
            mouse.Controller().move(0, screen_height - awayFrom)
            print("^", end=" ")
        elif screen_height + 1 > y >= screen_height - 1:
            mouse.Controller().move(0, -screen_height - awayFrom)
            print("V", end=" ")


def win_on_press(key):
    on_press(key)


def win_on_release(key):
    global allowed, current
    COMBINATIONS = [
        {keyboard.Key.shift, keyboard.Key.esc}
    ]
    if key == Key.ctrl_r:
        allowed = not allowed
        if allowed:
            print("Software control gained")
        else:
            print("\nSoftware control lost")

    if any([key in comb for comb in COMBINATIONS]):  # LINE 2
        current.add(key)
        if any(all(k in current for k in comb) for comb in COMBINATIONS):
            global tnow, tcounter
            tcounter += 1
            if datetime.datetime.now() - tnow < datetime.timedelta(seconds=1):
                if tcounter > 1:
                    tcounter = 0
                    listener.stop()
                    print("\nUn-initialized")
            else:
                tnow = datetime.datetime.now()
                current = set()


def linux_on_move(x, y):  # linux version
    on_move(x, y)


def linux_on_press(key):
    on_press(key)


def linux_on_release(key):
    on_release(key)


def mac_ver():  # mainly designed for myself
    pass


def windows_ver():  # windows
    pass


def linux_ver():  # linux
    pass


if __name__ == '__main__':
    s = 1
    allowed = True
    text = "Initialized\nUse right control/right command to pause/resume\nQuit combination:"
    if system() == "Darwin":
        print("Mac, Stable\n{0}\nCtrl+Esc then Alt+Esc".format(text))
        listeners = keyboard.Listener(on_release=mac_on_release, on_press=mac_on_press)
        listeners.start()
        with mouse.Listener(on_move=mac_on_move) as listener:
            listener.join()
            pass
    elif system() == "Windows":
        print("Windows\nThis is unstable and may slow down your mouse harshly\n{0}\nShift+Esc".format(text))
        listeners = keyboard.Listener(on_release=windows_on_release, on_press=windows_on_press)
        listeners.start()
        with mouse.Listener(on_move=windows_on_move) as listener:
            listener.join()
    elif system() == "Linux":
        print("Linux\nUntested, unstable, and unfinished. It will not work yet\n{0}".format(text))
        listeners = keyboard.Listener(on_release=linux_on_release, on_press=linux_on_press)
        listeners.start()
        with mouse.Listener(on_move=linux_on_move) as listener:
            listener.join()
    else:
        print("System unknown, this might not work properly. Using default\n{0}".format(text))
        listeners = keyboard.Listener(on_release=on_release, on_press=on_press)
        listeners.start()
        with mouse.Listener(on_move=on_move) as listener:
            listener.join()
    # listeners = keyboard.Listener(on_release=on_release, on_press=on_press)
    # listeners.start()
    # with mouse.Listener(on_move=on_move) as listener:
    #     listener.join()
