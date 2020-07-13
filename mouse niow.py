from time import sleep

from pynput.keyboard import (
    Controller as kController,
    Listener as kListener
)
from pynput.mouse import (
    Controller as mController,
    Listener as mListener
)

mouse = mController()
keyboard = kController()


def on_move(x, y):
    print(x, y)
    if x >= 1679.0:
        print("from right to left")
        mouse.move(-1679, 0)
        sleep(0.5)
    elif x <= 0.0:
        print("from left to right")
        mouse.move(1679, 0)
        sleep(0.5)


def on_click(x, y, q, w):
    print(x, y, q, w)


def on_press(key):
    pass


def on_release(key):
    pass


try:
    with mListener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_click):
        mListener.start()
    with kListener(
            on_press=on_press,
            on_release=on_keyboard):
        kListener.start()
except KeyboardInterrupt:
    pass
