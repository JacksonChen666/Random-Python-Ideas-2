"""
All I do is move the mouse randomly


Dependencies
--------------
pynput, random, time


Possibilities
--------------
Moving the mouse so slightly that it can cause tooltips to not appear at all
Cause insanity to people who doesn't know what the heck is this


Variables
--------------
intensity 	-- How much pixels to move randomly
startInt	-- The starting number of intensity, only stored from the start
iMultiplier -- How much to multiply by intensity
"""

if __name__ == '__main__':
    from random import uniform
    from pynput.mouse import Controller
    from math import isinf

    mouse, intensity, iMultiplier = Controller(), 0.001, 1.00001
    startInt = intensity
    # increases by: intensity * iMultiplier
    try:
        while True:
            if isinf(intensity): intensity = startInt
            print("\r{0}\tpixels max/move".format(intensity), end="", flush=True)
            for i in range(5):
                mouse.move(uniform(-intensity, intensity), uniform(-intensity, intensity))
            intensity *= iMultiplier
    except KeyboardInterrupt:
        exit()
