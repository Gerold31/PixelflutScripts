#!/usr/bin/python3

import shutil
import sys
import argparse

parser = argparse.ArgumentParser(description = "Generates an ASCII Barchart from data from stdin")
parser.add_argument("-cols", metavar="columns", help="overwrite the number of columns", type=int, default = None)
parser.add_argument("-rows", metavar="rows", help="overwrite the number of rows", type=int, default=None)

args = parser.parse_args()

cols, rows = shutil.get_terminal_size()

if args.cols:
	cols = args.cols
if args.rows:
	rows = args.rows


vals = []
min_v = 0
max_v = 0

for line in sys.stdin:
	v = float(line)
	vals.append(v)
	if v < min_v or len(vals) == 1:
		min_v = v
	if v > max_v or len(vals) == 1:
		max_v = v

if min_v == max_v:
	print("All values are the same: %f (%d timeis)" % (min_v, len(vals)))
	sys.exit(1)

vals = sorted(vals)

chart_rows = rows - 3
chart_cols = cols - 8

bucket_width = (max_v - min_v) / (chart_cols-1)

buckets = [0] * chart_cols

for v in vals:
	# not the most efficient way
	i = int((v - min_v) / bucket_width)

	buckets[i] += 1


min_b = buckets[0]
max_b = buckets[0]
for b in buckets:
	if b < min_b:
		min_b = b
	if b > max_b:
		max_b = b

for r in range(chart_rows):
	h = max_b - int((max_b - min_b) / chart_rows * r)
	if r == chart_rows-1:
		h = max(min_b, 1)
	line = ""
	for b in buckets:
		if b >= h:
			line += '#'
		else:
			line += ' '

	print("%7d|%s" % (h, line))

print("%s+%s" % (' '*7, '-'*chart_cols))

x_axis = "^%-4.f   " % (min_v)
x_axis_end = "%-4.f^" % (max_v)
while True:
	b = len(x_axis) - 1
	label = "^%-4.f   " % (b * bucket_width + min_b)
	l = len(x_axis + x_axis_end)
	space = chart_cols - l
	if len(label) <= space:
		x_axis += label
	else:
		x_axis += ' ' * space + x_axis_end
		break

print("%s%s" % (' '*8, x_axis))





