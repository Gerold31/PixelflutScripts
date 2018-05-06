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

class Ball:
	def __init__(self, x, y, r, c):
		self.x = x
		self.y = y
		self.r = r
		self.c = c
		self.vx = 0
		self.vy = 0

	def collides(self, other):
		dx = self.x - other.x
		dy = self.y - other.y
		r = self.r + other.r
		return dx * dx + dy * dy < r * r		

	def resolveCollision(self, other):
		d = ((other.x - self.x)**2 + (other.y - self.y)**2)**0.5
		if d == 0:
			nx = 0
			ny = 1
		else: 
			nx = (other.x - self.x)/d
			ny = (other.y - self.y)/d
		rvx = other.vx - self.vx
		rvy = other.vy - self.vy
		v = rvx * nx + rvy * ny
		if v > 0:
			return
		
		f = -0.7*v / (1/self.r + 1/other.r)
		ix = f * nx
		iy = f * ny
		self.vx -= 1/self.r * ix
		self.vy -= 1/self.r * iy
		other.vx += 1/other.r * ix
		other.vy += 1/other.r * iy

	def bounce(self, max_x, max_y):
		while self.x < 0 or self.x >= max_x:
			if self.x < 0:
				self.x = -self.x*0.7
				self.vx = -self.vx * 0.7
			elif self.x >= max_x:
				self.x = (max_x - 1) - (self.x - max_x - 1)*0.7
				self.vx = -self.vx * 0.7
		while self.y < 0 or self.y >= max_y:
			if self.y < 0:
				self.y = -self.y*0.7
				self.vy = -self.vy * 0.7
			elif self.y >= max_y:
				self.y = (max_y - 1) - (self.y - max_y - 1)*0.7
				self.vy = -self.vy * 0.7
			
	
balls = []

pballs = [ [[]] * panel_x for i in range(panel_y) ]

cx = 0
cy = 0
s = 0

for x in range(panel_x):
	for y in range(panel_y):
		c = screen.image[x][y]
		r = ((c & 0xff) + ((c >> 8) & 0xff) + ((c >> 16) & 0xff)) / (3*0x100)
		if r > 0.01:
			b = Ball(x, y, r, c)
			balls.append(b)
			pballs[x][y].append(b)

			cx += x * r
			cy += y * r
			s += r

if s != 0:
	cx /= s
	cy /= s

if len(sys.argv) == 4:
	for b in balls:
		dx = b.x - cx
		dy = b.y - cy
		d = (dx * dx + dy * dy)**0.5
		if dx != 0:
			b.vx = 50*dx/d
		if dy != 0:
			b.vy = 50*dy/d

def step(t):
	global pballs
	for b in balls:	
		for dx in range(-1, 1):
			for dy in range(-1, 1):
				for o in pballs[int(b.x) + dx][int(b.y) + dy]:
					if o == b:
						continue
					if b.collides(o):
						b.resolveCollision(o)
	newpballs = [ [[]] * panel_x for i in range(panel_y) ]
	for b in balls:
		b.x += b.vx*t
		b.y += b.vy*t
		b.vy += 9.81
		
		b.bounce(panel_x, panel_y)
		newpballs[int(b.x)][int(b.y)].append(b)
	pballs = newpballs

def clear():
	for b in balls:
		screen.set_px(b.x, b.y, 0, immediate = False)

def draw():
	for b in balls:
		screen.set_px(b.x, b.y, b.c, immediate = False)
	screen.send()

t0 = time.time()
while True:
	clear()
	t = time.time()
	print(t - t0)
	step(t - t0)
	t0 = t
	draw()
	#time.sleep(0.1)



