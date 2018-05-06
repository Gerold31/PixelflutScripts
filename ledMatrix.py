#!/usr/bin/python3

import telnetlib

class LedMatrix:
	def __init__(self, ip, port):
		self._tn = telnetlib.Telnet(ip, port)
		self._write("SIZE\n")
		s = self._read_line().split(' ')
		self.size_x = int(s[1])
		self.size_y = int(s[2])

	def _write(self, msg):
		#print(msg, end="")
		self._tn.write(msg.encode('ascii'))

	def _read_line(self):
		msg = self._tn.read_until('\n'.encode('ascii')).decode('ascii')
		#print(msg, end="")
		return msg

	def send(self, x, y, c):
		self._write("PX %d %d %06x\n" % (int(x), int(y), int(c)))

	def schedule_read(self, x, y):
		self._write("PX %d %d\n" % (int(x), int(y)))

	def recv_read(self):
		line = self._read_line().split(' ')
		x = int(line[1])
		y = int(line[2])
		c = int(line[3], 16)
		return (x, y, c)
		
	def read(self, x, y):
		self.schedule_read(x, y)
		return self.recv_read()[2]


