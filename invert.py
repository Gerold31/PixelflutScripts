#!/usr/bin/python3

import sys
import time
import random
import math

from ledScreen import LedScreen

screen = LedScreen(sys.argv[1], sys.argv[2])

panel_x = screen.size_x
panel_y = screen.size_y

screen.read_screen()


for x in range(panel_x):
	for y in range(panel_y):
		screen.set_px(x, y, 0xffffff ^ screen.image[x][y])


