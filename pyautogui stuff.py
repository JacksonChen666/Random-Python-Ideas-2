#!/usr/bin/env python3
from pyautogui import *

width, height = size()
x, y = position()
try:
    loc = locateOnScreen("calc simple.png")
except ImageNotFoundException:
    try:
        loc = locateOnScreen("calc advanced.png")
    except ImageNotFoundException:
        print("Calculator not found")
print(width, height, x, y)
