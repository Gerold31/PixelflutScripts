#!/usr/bin/python3

import sys
import time
import random
import math
import colorsys

from ledScreen import LedScreen



def pick_color(v):
	if v == 1 or v < 0.1:
		return 0
	rgb = colorsys.hsv_to_rgb(v+2/3, 1, 1)

	r = int(rgb[0] * 0xff)
	g = int(rgb[1] * 0xff)
	b = int(rgb[2] * 0xff)

	
	return r << 16 | g << 8 | b


def mandel(x, y):
	x2 = x*x
	y2 = y*y
	xy = x*y
	
	z = x2 + y2
	i = 0
	max_i = 100	
	while z < 100 and i < max_i:
		i += 1
		nx = x2 - y2 + x
		ny = xy + xy + y
		x2 = nx * nx
		y2 = ny * ny
		xy = nx * ny
		
		z = x2 + y2
	
	return pick_color(i/max_i)


screen = LedScreen(sys.argv[1], sys.argv[2])

panel_x = screen.size_x
panel_y = screen.size_y


pois = [(-0.170337,-1.06506), (0.42884,-0.231345), (-1.62917,-0.0203968), (-0.761574,-0.0847596)]
center = random.choice(pois)


scale = 1/10
center_x = center[0]
center_y = center[1]

speed = 0.99
interval = 0.05  
t0 = time.time()
while True:
	for x in range(panel_x):
		for y in range(panel_y):
			mx = (x-panel_x//2)*scale + center_x
			my = (y-panel_y//2)*scale + center_y

			color = mandel(mx, my)
			screen.set_px(x, y, color)
	scale = speed*scale

	time.sleep(interval - ((time.time() - t0) % interval))


