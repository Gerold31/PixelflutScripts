#!/usr/bin/python3

import sys
import fileinput
import random
import time
import argparse

import font


from ledScreen import LedScreen

parser = argparse.ArgumentParser(description = "Send some text to a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("-fg", metavar="foreground", help="foreground color as RRGGBB, 'random' or 'fade'", default = "random")
parser.add_argument("-bg", metavar="background", help="background color as RRGGBB, 'random' or 'fade'", default = "000000")
parser.add_argument("-d", metavar="delay", help="delay between sending two characters, in ms", type=int, default = 10)
parser.add_argument("-n", metavar="fadesteps", help="steps between two fade colors", type=int, default = 50)

args = parser.parse_args()


def getRandomC():
	while True:
		r = random.randrange(0, 0xff)
		g = random.randrange(0, 0xff)
		b = random.randrange(0, 0xff)
		s = r+g+b
		if s > 0x60:
			return r << 16 | g << 8 | b
	
def fade(a, b, n):
	rA = (a >> 16) & 0xff
	gA = (a >>  8) & 0xff
	bA = (a      ) & 0xff
	rB = (b >> 16) & 0xff
	gB = (b >>  8) & 0xff
	bB = (b      ) & 0xff

	
	r = int(rA * (1-n) + rB * n)
	g = int(gA * (1-n) + gB * n)
	b = int(bA * (1-n) + bB * n)

	return r << 16 | g << 8 | b


screen = LedScreen(args.ip, args.port)

panel_x = screen.size_x
panel_y = screen.size_y

x = 0
y = 0

fadeF = False
fadeB = False

i = 0

if args.fg == "random":
	fg = getRandomC()
elif args.fg == "fade":
	fadeF = True
	fg = getRandomC()
else:
	fg = int(args.fg, 16)

if args.bg == "random":
	bg = getRandomC()
elif args.bg == "fade":
	fadeB = True
	bg = getRandomC()
else:
	bg = int(args.bg, 16)

lastF = fg
lastB = bg
i = args.n

while True:
	i += 1
	if i > args.n:
		i = 0
		if fadeF:
			lastF = fg
			fg = getRandomC()
		if fadeB:
			lastB = bg
			bg = getRandomC()


	c = sys.stdin.read(1)
	if c == '':
		break
	elif c == '\n':
		y += 1
		x = 0
	elif c == '\r':
		x = 0
	elif c == '\t':
		x += 2
	else:
		for dx in range(font.size_x):
			for dy in range(font.size_y):
				sx = x*font.size_x + dx
				sy = y*font.size_y + dy
				sc = fade(lastF, fg, i/args.n) if font.chars[c][dx][dy] == 1 else fade(lastB, bg, i/args.n)
				screen.set_px(sx, sy, sc, force=True)
		x += 1
	
	
	if (x+1)*font.size_x > panel_x:
		x = 0
		y += 1
	if (y+1)*font.size_y > panel_y:
		y = 0

	if args.d > 0:
		time.sleep(args.d/1000)
