#!/usr/bin/python3

import sys
import time
import random
import math

from ledScreen import LedScreen

screen = LedScreen(sys.argv[1], sys.argv[2])

panel_x = screen.size_x
panel_y = screen.size_y

f = (panel_x+panel_y)/(math.pi/2)

for da in range(int(f * 2*math.pi)):
	a = da/f
	for d in range(panel_x):
		x = panel_x/2 + d*math.sin(a)		
		y = panel_y/2 + d*math.cos(a)		
		if x < 0 or x >= panel_x:
			break
		if y < 0 or y >= panel_y:
			break
		screen.set_px(x, y, 0)
	#time.sleep(0.05)
