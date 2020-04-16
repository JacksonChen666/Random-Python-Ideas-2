# only need to install pynput but its automated already
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


def on_move(x, y):
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


def on_release(key):
    if key == Key.esc:
        listener.stop()
        print("\nOff")


if __name__ == '__main__':
    screen_width = tk.Tk().winfo_screenwidth()
    screen_height = tk.Tk().winfo_screenheight()
    listeners = keyboard.Listener(on_release=on_release, onpress=on_release)
    listeners.start()
    print("On")
    with mouse.Listener(on_move=on_move) as listener:
        listener.join()
