#!/usr/bin/python3

import sys
import time
import random
import math

from ledMatrix import LedMatrix

LedMatrix = LedMatrix(sys.argv[1], sys.argv[2])

panel_x = LedMatrix.size_x
panel_y = LedMatrix.size_y

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
		LedMatrix.send(x, y, 0)
	#time.sleep(0.05)
