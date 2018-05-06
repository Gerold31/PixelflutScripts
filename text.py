#!/usr/bin/python3

import sys
import fileinput

import font

from ledScreen import LedScreen

screen = LedScreen(sys.argv[1], sys.argv[2])

panel_x = screen.size_x
panel_y = screen.size_y

x = 0
y = 0

bg = 0x000000
fg = 0xffffff

while True:
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
				sc = fg if font.chars[c][dx][dy] == 1 else bg
				screen.set_px(sx, sy, sc, force=True)
		x += 1
	
	
	if x*font.size_x > panel_x:
		x = 0
		y += 1
	if y*font.size_y > panel_y:
		y = 0


