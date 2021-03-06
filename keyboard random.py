from pynput.keyboard import Controller, Key, Listener

keyboard = Controller()


def on_press(key):
    if key == Key.esc:
        return False


def on_release(key):
    if key == Key.esc:
        return False


with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
