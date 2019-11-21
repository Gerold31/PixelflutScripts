#!/usr/bin/python3

import sys
import argparse

from PIL import Image, ImageSequence

from ledScreen import LedScreen


parser = argparse.ArgumentParser(description = "Sends a image to a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("img")
parser.add_argument("-i", action="store_true", help="Invert the image")
parser.add_argument("-l", action="store_true", help="Loop the image sequence (gif)")

args = parser.parse_args()

screen = LedScreen(args.ip, args.port)

size = screen.size_x, screen.size_y


try:
	seq = Image.open(args.img)
	while True:
		for im in ImageSequence.Iterator(seq):
			temp = im.copy()
			temp.thumbnail(size, Image.ANTIALIAS)
			temp = temp.convert("RGB")

			off_x = (size[0] - temp.size[0])//2
			off_y = (size[1] - temp.size[1])//2
	
			for x in range(temp.size[0]):
				for y in range(temp.size[1]):
					c = temp.getpixel((x, y))
					c = c[0] << 16 | c[1] << 8 | c[2]

					if args.i:
						c ^= 0xffffff

					screen.set_px(x+off_x, y+off_y, c, immediate = False)

			screen.send()
		
		if not args.l:
			break


except IOError:
    print("cannot create thumbnail for '%s'" % infile)

