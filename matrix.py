#!/usr/bin/python3

import sys
import random
import time
import argparse
import math
import string

import font

from ledScreen import LedScreen

parser = argparse.ArgumentParser(description = "Matrix animation for a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("-d", metavar="duration", help="duration of animation (s)", type=float, default = -1)
parser.add_argument("-t", metavar="text", help="text to print", type=str, default=None)

args = parser.parse_args()


def rand_c():
	while True:
		r = random.randrange(0, 0x7f)
		g = random.randrange(0x80, 0xff)
		b = random.randrange(0, 0x7f)
		s = r+g+b
		if s > 0x60:
			return r << 16 | g << 8 | b
	

screen = LedScreen(args.ip, args.port)

panel_x = screen.size_x
panel_y = screen.size_y

final_text = None
if args.t:
	lines = args.t.split("\\n")
	max_lines = panel_y // font.size_y
	max_length = panel_x // font.size_x
	if len(lines) > max_lines:
		print("Error: text has too many lines, max " + str(max_lines))
		sys.exit(-1)
	final_text = {}
	off_y = max_lines // 2 - len(lines) // 2
	for l in range(len(lines)):
		line = lines[l]
		if len(line) > max_length:
			print("Error: line " + str(l) + "(\"" + line + "\") is too long, max " + str(max_length))
			sys.exit(-1)
		off_x = max_length // 2 - len(line) // 2
		for i in range(len(line)):
			final_text[(off_x + i, off_y + l)] = {"char": line[i], "drawn": False}
			
	

def clear_screen():
	for x in range(panel_x):
		for y in range(panel_y):
			screen.set_px(x, y, 0, immediate=False)

def draw_char(pos, char, color):
	for dx in range(font.size_x):
		for dy in range(font.size_y):
			sx = pos[0] + dx
			sy = pos[1] + dy
			sc = color if font.chars[char][dx][dy] == 1 else 0
			screen.set_px(sx, sy, sc, immediate=False)

class Particle:
	def __init__(self, ttl, color, pos, toggle, char):
		self.ttl = ttl
		self.age = 0
		self.color = color
		self.pos = pos
		self.toggle = toggle
		self.char = char

	def step(self, dt):
		self.age += dt;

	def is_dead(self):
		return self.age > self.ttl and self.ttl >= 0

	def draw(self, screen):
		if not self.is_dead():
			draw_char(self.pos, self.char, 0xffffff if self.age < self.toggle else self.color)
		else:
			draw_char(self.pos, ' ', 0x000000)

class Trail:
	def __init__(self):
		self.lenght = random.randrange(3, 2 * panel_y//font.size_y // 3)
		self.pos_x = random.randrange(0, panel_x//font.size_x) * font.size_x
		self.speed = panel_y / random.uniform(1, 5)
		self.pos_y = 0
		self.toggle = font.size_y / self.speed
		self.ttl = self.toggle * self.lenght
		self.particles = []
		self._add_particle(0)

	def step(self, dt):
		old_y = self.pos_y
		self.pos_y += dt * self.speed
		for y in range(int(old_y) // font.size_y, int(min(self.pos_y, panel_y)) // font.size_y): 
			self._add_particle(y * font.size_y)
						
		self.particles = [p for p in self.particles if not p.is_dead()]
		
		for p in self.particles:
			p.step(dt)


	def is_dead(self):
		return len(self.particles) == 0

	def draw(self, screen):
		for p in self.particles:
			p.draw(screen)

	def _add_particle(self, y):
		char_x = self.pos_x // font.size_x
		char_y = y // font.size_y
		
		char = random.choice(string.ascii_letters + string.digits + string.punctuation)
		col = rand_c()
		ttl = self.ttl

		if (char_x, char_y) in final_text and random.randrange(3) < 1:
			f = final_text[(char_x, char_y)]
			char = f["char"]
			f["drawn"] = True
			ttl = -1
			col = 0xffffff
			
		self.particles.append(Particle(ttl, col, [self.pos_x, y], self.toggle, char))

trails = []

last_update = time.time()
start = last_update
next_spawn = 0

f = panel_x / font.size_x * 2 / 3

def is_dead():
	if final_text:
		for f in final_text:
			if not final_text[f]["drawn"]:
				return False
		return True
	return args.d > 0 and time.time() - start > args.d

while True:
	now = time.time()
	dt = now - last_update

	if now >= next_spawn and not is_dead():
		trails.append(Trail())
			
		next_spawn = now + random.gauss(1.0/f, 0.25/f)

	for trail in trails:
		trail.step(dt)
		trail.draw(screen)

	trails = [r for r in trails if not r.is_dead()]
	
	screen.send()

	last_update = now

	if is_dead() and len(trails) == 0:
		break

			

