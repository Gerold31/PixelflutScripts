#!/usr/bin/python3

import threading

from ledMatrix import LedMatrix

class LedScreen(threading.Thread):

	def __init__(self, ip, port):
		threading.Thread.__init__(self)

		self._matrix = LedMatrix(ip, port)

		self.size_x = self._matrix.size_x		
		self.size_y = self._matrix.size_y
	
		self._clr_image = [ [0] * self.size_y for i in range(self.size_x)]
		self.image = [ [None] * self.size_y for i in range(self.size_x)]
		self.delta_image = {}
		self._work = [ [0] *self.size_y for i in range(self.size_x)]

		self._lock = threading.Lock()

		self.daemon = True
		self.start()
		
	def run(self):
		while True:
			r = self._matrix.recv_read()
			with self._lock:
				self._clr_image[r[0]][r[1]] = r[2]
				self._work[r[0]][r[1]] -= 1


	def _read_px(self, x, y):
		with self._lock:
			self._work[x][y] += 1
		self._matrix.schedule_read(x, y)

	def _fetch_read_result(self, x, y):
		while self._work[x][y] > 0:
			pass
		self.image[x][y] = self._clr_image[x][y]
		

	def read_screen(self):
		for x in range(self.size_x):
			for y in range(self.size_y):
				self._read_px(x, y)
		for x in range(self.size_x):
			for y in range(self.size_y):
				self._fetch_read_result(x, y)

	def get_px(self, x, y, local=True):
		if not local:
			self._read_px(x, y)
			self._fetch_read_result(x, y)

		return self.image[x][y]

	def set_px(self, x, y, c, clearable = False, force = False, immediate = True):
		x = int(x)
		y = int(y)
		if x < 0 or x >= self.size_x or y < 0 or y >= self.size_y:
			return
		if immediate:
			if self.image[x][y] == c and not force:
				return
			if clearable:
				self._read_px(x, y)
			self._matrix.send(x, y, c)
			self.image[x][y] = c

		else:
			if ((x, y) not in self.delta_image and self.image[x][y] == c) and not force:
				return
			self.delta_image[(x, y)] = c

	def send(self):
		for (x, y) in self.delta_image:
			self.set_px(x, y, self.delta_image[(x, y)])
		self.delta_image = {}

	
	def clr_px(self, x, y):
		while self._work[x][y] > 0:
			pass
		
		self.set_px(x, y, self._clr_image[x][y])

