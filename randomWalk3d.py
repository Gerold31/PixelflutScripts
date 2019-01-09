#!/usr/bin/python3

import sys
import random
import time
import argparse
import math

from ledScreen import LedScreen

parser = argparse.ArgumentParser(description = "3D Random Walk animation for a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("-s", metavar="sleep", help="delay between steps", type=float, default = 0)
parser.add_argument("-r", metavar="radius", help="radius of the sphere", type=int, default = 500)
parser.add_argument("-fov", metavar="", help="field of view of the camera", type=int, default = 45)

args = parser.parse_args()

if args.fov <= 0 or args.fov >= 180:
	print("Error: fov must be in (0; 180)")
	sys.exit(1)

fov_tan = math.tan(args.fov/2*math.pi/180)
cam_r = 1.1*args.r/math.sin(args.fov/2*math.pi/180)

t = time.time() 

map = {}

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

def add(a, b):
	c = []
	for i in range(len(a)):
		c.append(a[i] + b[i])
	return c
	
def mul(a, s):
	c = []
	for i in range(len(a)):
		c.append(a[i] * s)
	return c
	
def neg(a):
	return mul(a, -1)

def vlen(a):
	c = 0
	for i in range(len(a)):
		c += a[i]**2
	return math.sqrt(c)

def norm(a):
	return mul(a, 1/vlen(a))

def rot_x(v, a):
	s = math.sin(a)
	c = math.cos(a)
	return [v[0], v[1] * c - v[2] * s, v[1] * s + v[2] * c]

def rot_y(v, a):
	s = math.sin(a)
	c = math.cos(a)
	return [v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]

def rot_z(v, a):
	s = math.sin(a)
	c = math.cos(a)
	return [v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[z]]

def render(a):
	f = 1

	cam_pos = mul([math.sin(a), 0, math.cos(a)], cam_r)
	#cam_pos = [0, 0, cam_r]

	d = min(panel_x, panel_y)/fov_tan

	aspect = panel_x/panel_y

	for x in range(panel_x):
		print("%5.2f%%" % (x/panel_x*100), end = '\r')
		dx = (2 * ((x+0.5) / panel_x) - 1) * fov_tan * aspect
		for y in range(panel_y):
			dy = (1 - 2 * ((y+0.5) / panel_y)) * fov_tan
			
			ray_d = rot_y(norm([dx, dy, -1]), a)

			hit = False
			for i in range(2*args.r):
				k = i + cam_r-args.r
				p = add(cam_pos, mul(ray_d, k))

				mx = int(p[0])
				my = int(p[1])
				mz = int(p[2])
				if mx in map and my in map[mx] and mz in map[mx][my] and map[mx][my][mz] != 0:
					screen.set_px(x, y, map[mx][my][mz], immediate=False)
					hit=True
					break
	
			if not hit:
				screen.set_px(x, y, 0, immediate=False)

	screen.send()

c = rand_c()
steps = 0

x = 0
y = 0
z = 0

#render()

num = 0

while True:
	if x not in map:
		map[x] = {}
	if y not in map[x]:
		map[x][y] = {}

	map[x][y][z] = c

	dx, dy, dz = random.choice([(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)])
	x += dx
	y += dy
	z += dz
	steps += 1

	if x*x + y*y + z*z > args.r**2:
		print(steps)
		x = 0
		y = 0
		z = 0
		steps = 0
		c = rand_c()
		#render()
		num += 1
		if num >= 10:
			break
	
	#if time.time() - t > 0.1:
		#t = time.time()
		#render()

#	time.sleep(0.001)			


for i in range(360):
	render(i*5/180*math.pi)




