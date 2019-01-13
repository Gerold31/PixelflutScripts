#!/usr/bin/python3

class Octree:
	def __init__(self, size, x = 0, y = 0, z = 0):
		self.size = size
		self.x = x
		self.y = y
		self.z = z
		self.nodes = [None] * 8

	def _get_idx(self, pos):
		idx = 0

		if pos[0] > self.x:
			idx |= 1
		if pos[1] > self.y:
			idx |= 2
		if pos[2] > self.z:
			idx |= 4

		return idx
	
	def _center_from_idx(self, idx):
		s = self.size/4
		x = self.x + (-s if idx & 1 == 0 else s)
		y = self.y + (-s if idx & 2 == 0 else s)
		z = self.z + (-s if idx & 4 == 0 else s)
		return (x, y, z)

	def _equal_pos(self, a, b):
		return a == b

	def _oob(self, pos):
		if (pos[0] >= -self.size/2+self.x and
		    pos[1] >= -self.size/2+self.y and
		    pos[2] >= -self.size/2+self.z and
		    pos[0] <= self.size/2+self.x and
		    pos[1] <= self.size/2+self.y and
		    pos[2] <= self.size/2+self.z):
			return False
		return True
		
	def _intersect(self, pos, dir, c, s):
		r = s/2
		min_t = []
		max_t = []
		for i in range(3):
			if dir[i] == 0:
				if pos[i] < c[i] - r or pos[i] > c[i] + r:
					return None
			else:
				t1 = (c[i] + r - pos[i]) / dir[i]
				t2 = (c[i] - r - pos[i]) / dir[i]
	
				min_t.append(min(t1, t2))
				max_t.append(max(t1, t2))

		if len(min_t) == 0:
			# dir == (0, 0, 0) hits nothing
			return None

		t = max(min_t)
		if t < 0 or t > min(max_t):
			return None

		return t

	def set(self, pos, data):
		assert self._oob(pos) == False, "%s is out of bound for cube with size %d at %s" % (pos, self.size, [self.x, self.y, self.z])

		idx = self._get_idx(pos)

		if self.nodes[idx] is None:
			self.nodes[idx] = (pos, data)
			return
		if not isinstance(self.nodes[idx], Octree):
			if self._equal_pos(self.nodes[idx][0], pos):
				self.nodes[idx] = (pos, data)
				return
			
			old = self.nodes[idx]
		
			x, y, z = self._center_from_idx(idx)	
			
			self.nodes[idx] = Octree(self.size/2, x, y, z)
	
			self.nodes[idx].set(old[0], old[1])
		
		self.nodes[idx].set(pos, data)
		
	
	def get(self, pos):
		if self._oob(pos):
			return None
		idx = self._get_idx(pos)
		if self.nodes[idx] is None:
			return None
		if not isinstance(self.nodes[idx], Octree):
			if self._equal_pos(self.nodes[idx][0], pos):
				return self.nodes[idx][1]
			return None
		return self.nodes[idx].get(pos)

	def trace(self, pos, dir):
		if self._intersect(pos, dir, [self.x, self.y, self.z], self.size) is None:
			return None, -1

		min_t = -1
		hit = None
		for i in range(len(self.nodes)):
			n = self.nodes[i]
			h = None

			if isinstance(n, Octree):
				h, t = n.trace(pos, dir)
			elif n is not None:
				t = self._intersect(pos, dir, [n[0][0] - 0.5, n[0][1] - 0.5, n[0][2] - 0.5], 1)
				#t = self._intersect(pos, dir, self._center_from_idx(i), self.size/2)
				if t is not None:
					h = n[1]
							
			if h is not None and (hit is None or t < min_t):
				min_t = t
				hit = h

		return hit, min_t

	def print(self, depth = 0):
		print("%s%s (%s, %f)" % ("  " * depth, "Tree", str([self.x, self.y, self.z]), self.size))
		for n in self.nodes:
			if n is None:
				print("%s%s" % ("  " * (depth+1), "None"))
			elif isinstance(n, Octree):
				n.print(depth+1)
			else:
				print("%s%s: %s" % ("  " * (depth+1), str(n[0]), str(n[1])))

	def count(self):
		c = 0
		for n in self.nodes:
			if n is None:
				continue
			elif isinstance(n, Octree):
				c += n.count()
			else:
				c += 1

		return c
