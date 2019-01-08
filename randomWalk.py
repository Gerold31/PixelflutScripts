#!/usr/bin/python3

import sys
import random
import time
import argparse
import math

from ledScreen import LedScreen

parser = argparse.ArgumentParser(description = "Random Walk animation for a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("-s", metavar="sleep", help="delay between steps", type=float, default = 0)
parser.add_argument("-c", help="limit the field by a circle", action='store_true')

args = parser.parse_args()


def rand_c():
	while True:
		r = random.randrange(0, 0xff)
		g = random.randrange(0, 0xff)
		b = random.randrange(0, 0xff)
		s = r+g+b
		if s > 0x60:
			return r << 16 | g << 8 | b
	

screen = LedScreen(args.ip, args.port)

panel_x = screen.size_x
panel_y = screen.size_y

x = panel_x // 2
y = panel_y // 2
c = rand_c()
steps = 0

r2 = min(x, y)**2

while True:
	dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
	x += dx
	y += dy
	steps += 1
	
	if (args.c and ((panel_x//2-x)**2)+((panel_y//2-y)**2) > r2) or (x < 0 or x >= panel_x or y < 0 or y >= panel_y):
		print(steps)
		x = panel_x // 2
		y = panel_y // 2
		c = rand_c()
		steps = 0
	
	screen.set_px(x, y, c)
	
	time.sleep(args.s)
			

