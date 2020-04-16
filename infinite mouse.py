# only need to install pynput but its automated already
# key comb: https://github.com/moses-palmer/pynput/issues/20#issuecomment-412714960
import datetime
import tkinter as tk

try:
    from pynput import mouse, keyboard
    from pynput.keyboard import Key
except ImportError:
    from subprocess import run

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

# The currently active modifiers
current = set()

tnow = datetime.datetime.now()
tcounter = 0


def on_move(x, y):
    if allowed:  # well that happened
        if 0.0 <= x <= 0.5:
            mouse.Controller().move(10000, 0)
            print("->", end=" ")
        elif screen_width - 1 <= x < screen_width:
            mouse.Controller().move(-10000, 0)
            print("<-", end=" ")
        elif 0.0 <= y <= 0.5:
            mouse.Controller().move(0, 10000)
            print("^", end=" ")
        elif screen_height > y >= screen_height - 1:
            mouse.Controller().move(0, -10000)
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


if __name__ == '__main__':
    s = 1
    allowed = True
    screen_width = tk.Tk().winfo_screenwidth()
    screen_height = tk.Tk().winfo_screenheight()
    listeners = keyboard.Listener(on_release=on_release, on_press=on_press)
    listeners.start()
    print("Initialized\nUse right control/right command to pause/resume\nQuit combination:\nCtrl+Esc then Alt+Esc")
    with mouse.Listener(on_move=on_move) as listener:
        listener.join()
