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
	from time import sleep
	from pynput.mouse import Controller
	from math import isinf
	mouse = Controller()
	intensity = 0.001
	startInt = intensity
	iMultiplier = 1.001
	# increases by: intensity * iMultiplier
	try:
		while True:
			if isinf(intensity):
				intensity = startInt
			print("\r{0}	pixels max/move".format(intensity), end="")
			for i in range(5):
				mouse.move(uniform(-intensity, intensity), uniform(-intensity, intensity))
				sleep(uniform(0.1, 0.0001))
			intensity *= iMultiplier
	except KeyboardInterrupt:
		exit()
