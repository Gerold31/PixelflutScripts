#!/usr/bin/python3


from PIL import Image

img = Image.open("font.png")

print("#!/usr/bin/python\n\nchars = ", end = "")

size_x = 6
size_y = 8

chars = {}
for i in range(96):
	c = []
	for dx in range(size_x):
		c.append([])
		for dy in range(size_y):
			x = (i % 16)*size_x + dx
			y = (i //16)*size_y + dy
			if img.getpixel((x, y))[0] == 0:
				c[-1].append(1)
			else:
				c[-1].append(0)
	chars[chr(i + ord(' '))] = c

print(chars)

print("size_x = %d" % size_x)
print("size_y = %d" % size_y)
