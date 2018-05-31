#!/usr/bin/python3

import sys
import argparse

from PIL import Image

from ledMatrix import LedMatrix


parser = argparse.ArgumentParser(description = "Sends a image to a PixelFlut screen")
parser.add_argument("ip")
parser.add_argument("port")
parser.add_argument("img")
parser.add_argument("-i", action="store_true", help="Invert the image")

args = parser.parse_args()

LedMatrix = LedMatrix(args.ip, args.port)

size = LedMatrix.size_x, LedMatrix.size_y

try:
	im = Image.open(args.img)
	im.thumbnail(size, Image.ANTIALIAS)
	im = im.convert("RGB")

	off_x = (size[0] - im.size[0])//2
	off_y = (size[1] - im.size[1])//2

	for x in range(im.size[0]):
		for y in range(im.size[1]):
			c = im.getpixel((x, y))
			c = c[0] << 16 | c[1] << 8 | c[2]

			if args.i:
				c ^= 0xffffff

			LedMatrix.send(x+off_x, y+off_y, c)



except IOError:
    print("cannot create thumbnail for '%s'" % infile)

