#!/usr/bin/python3

import sys
import random
import time
import argparse
import math

from ledScreen import LedScreen

parser = argparse.ArgumentParser(description = "Firework animation for a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("-f", metavar="frequency", help="frequency of rockets", type=float, default = 5)

args = parser.parse_args()

GRAVITY_Y = 0.2

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


def clear_screen():
	for x in range(panel_x):
		for y in range(panel_y):
			screen.set_px(x, y, 0, immediate=False)


class Particle:
	def __init__(self, ttl, color, pos, vel):
		self.ttl = ttl
		self.age = 0
		self.color = color
		self.pos = pos
		self.vel = vel

	def step(self, dt):
		self.age += dt;
		self.pos[0] += self.vel[0] * dt
		self.pos[1] += self.vel[1] * dt
		self.vel[1] += GRAVITY_Y * dt

	def is_dead(self):
		return self.age > self.ttl

	def draw(self, screen):
		if not self.is_dead():
			# todo: trail
			screen.set_px(self.pos[0]*screen.size_x, self.pos[1]*screen.size_y, self.color, immediate=False)


class Rocket:
	def __init__(self):
		ttl = 2
		pos = [random.random(), 1];
		vel = [random.gauss(0.5-pos[0], 0.3)/3, -random.gauss(0.5, 0.2)]
		self.booster = Particle(ttl, rand_c(), pos, vel)
		self.particles = []

	def step(self, dt):
		if not self.booster.is_dead():
			self.booster.step(dt)
			if self.booster.is_dead():
				s = random.gauss(0.15, 0.05)
				c = rand_c()
				for x in range(random.randrange(20, 100)):
					a = random.random() * math.pi 
					b = random.random() * math.pi
					pos = [self.booster.pos[0], self.booster.pos[1]]
					vel = [math.cos(a)*s*math.sin(b), math.cos(b)*s]
					self.particles.append(Particle(1, c, pos, vel))

		for p in self.particles:
			p.step(dt)

		self.particles = [p for p in self.particles if not p.is_dead()]

	def is_dead(self):
		return self.booster.is_dead() and len(self.particles) == 0

	def draw(self, screen):
		self.booster.draw(screen)
		for p in self.particles:
			p.draw(screen)

rockets = []

last_update = time.time()
next_spawn = 0

while True:
	now = time.time()
	dt = now - last_update

	if now >= next_spawn:
		rockets.append(Rocket())
			
		next_spawn = now + random.gauss(1.0/args.f, 0.25/args.f)

	clear_screen()

	for rocket in rockets:
		rocket.step(dt)
		rocket.draw(screen)

	rockets = [r for r in rockets if not r.is_dead()]
	
	screen.send()

	last_update = now

			

