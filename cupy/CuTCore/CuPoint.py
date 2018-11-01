class CuPoint:
	__slots__ = ('xp', 'yp')
	def __init__(self, xpos=0, ypos=0):
		self.xp = xpos
		self.yp = ypos

	def isNull(self):
		return self.xp ==0 and self.yp==0

	def x(self):
		return self.xp

	def y(self):
		return self.yp

	def setX(self, xpos):
		self.xp = xpos

	def setY(self, ypos):
		self.yp = ypos

	def __iadd__(self, p):
		self.xp += p.xp
		self.yp += p.yp
		return self

	def __isub__(self, p):
		self.xp += p.xp
		self.yp += p.yp
		return self

	def __add__(self, p):
		return CuPoint(self.xp + p.xp, self.yp + p.yp)

	def __sub__(self, p):
		return CuPoint(self.xp - p.xp, self.yp - p.yp)

class CuSize:
	__slots__ = ('wd', 'ht')
	def __init__(self, w=-1, h=-1):
		self.wd = w
		self.ht = h

	def isNull(self):
		return self.wd ==0 and self.ht==0

	def width(self):
		return self.wd

	def height(self):
		return self.ht

	def setWidth(self, w):
		self.wd = w

	def setHeight(self, h):
		self.ht = h

	def __iadd__(self, p):
		self.wd += p.xp
		self.ht += p.ht
		return self

	def __isub__(self, p):
		self.wd += p.xp
		self.ht += p.ht
		return self

	def __add__(self, p):
		return CuPoint(self.wd + p.wd, self.ht + p.ht)

	def __sub__(self, p):
		return CuPoint(self.wd - p.wd, self.ht - p.ht)