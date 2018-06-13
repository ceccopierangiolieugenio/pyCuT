'''
    Widget
'''

import curses, curses.panel
import logging
import os

from CuLayout import *
from CuApplication import *


class CuWidget:
	_win = None
	_panel = None
	_layout = None
	_x, _y, _w, _h = 0, 0, 0, 0
	_childs = None
	_parent = None
	_border = False

	def __init__(self, *args, **kwargs):
		if not CuApplication.is_initialized():
			print(self.__class__.__name__ + ": Must construct a CuApplication before a CuWidget")
			os.abort()
		# logging.debug(str(kwargs))
		if 'parent' in kwargs: self._parent = kwargs['parent']
		else : self._parent = None; CuApplication.setMainWidget(self)
		if 'name' in kwargs: self._name = kwargs['name']
		else : self._name = ''
		if 'x' in kwargs: self._x = kwargs['x']
		else : self._x = 0
		if 'y' in kwargs: self._y = kwargs['y']
		else : self._y = 0
		if 'w' in kwargs: self._w = kwargs['w']
		else : self._w = CuApplication.getW()
		if 'h' in kwargs: self._h = kwargs['h']
		else : self._h = CuApplication.getH()
		self._childs = []
		self._win = curses.newwin(self._h, self._w, self._y, self._x)
		self._panel = curses.panel.new_panel(self._win)

	def accessibleName(self):
		return self._name

	def setAccessibleName(self, name):
		self._name = name


	def getPos(self):
		return self._x, self._y

	def move(self, x, y):
		# self._win.clear()
		# logging.debug(__name__ + "x:" + str(self._x) + " y:" + str(self._y))
		newx = x
		newy = y
		if newx < 0: newx=0
		if newy < 0: newy=0
		if newx+self._w > CuApplication.getW() : newx=CuApplication.getW()-self._w
		if newy+self._h > CuApplication.getH() : newy=CuApplication.getH()-self._h
		self._x = newx
		self._y = newy
		self._panel.move(self._y, self._x)

	def setBorder(self, bool):
		self._border = bool
		if bool:
			self._win.box()
		else:
			self._win.clear()

	def resize(self, w, h):
		neww = w
		newh = h
		if neww < 0: neww=0
		if newh < 0: newh=0
		if neww+self._x > CuApplication.getW() : neww=CuApplication.getW()-self._x
		if newh+self._y > CuApplication.getH() : newh=CuApplication.getH()-self._y
		self._w = neww
		self._h = newh
		self._win.clear()
		self._win.resize(self._h,self._w)

		if self._border:
			self._win.box()

	def getWin(self):
		return self._win

	def paint(self):
		if self._layout is not None:
			self._layout.paint()

	def event(self, evt):
		if self._layout is not None:
			self._layout.event(evt)

	def setLayout(self, layout):
		if isinstance(layout, CuLayout):
			self._layout = layout
			self._layout.setParent(self)
			if self._border:
				self._layout.setGeometry(self._x+1, self._y+1, self._w-2, self._h-2)
			else:
				self._layout.setGeometry(self._x, self._y, self._w, self._h)
			self._layout.update()
		else:
			raise Exception(str(layout) + ' not of type CuLayout')

	def layout(self):
		return self._layout

	def setGeometry(self, x, y, w, h):
		# logging.debug("FROM:"+str({"SELF":self._name, "x":x,"y":y,"w":w,"h":h}))
		# logging.debug("TO:  "+str({"SELF":self._name, "x":self._x,"y":self._y,"w":self._w,"h":self._h}))
		if self._w == w and self._h == h:
			if self._x != x or self._y != y:
				self.move(x, y)
			else:
				return
		elif self._x == x and self._y == y:
			self.resize(w, h)
		elif self._x + w < CuApplication.getW() and self._y + h < CuApplication.getH():
			self.resize(w, h)
			self.move(x, y)
		else:
			# logging.debug("EXTRA:"+str({"SELF":self._name, "x":self._x,"y":self._y,"w":self._w,"h":self._h}))
			self._x = x
			self._y = y
			self._w = w
			self._h = h
			self.resize(w, h)
			self.move(x, y)

		if self._layout is not None:
			if self._border:
				self._layout.setGeometry(self._x+1, self._y+1, self._w-2, self._h-2)
			else:
				self._layout.setGeometry(self._x, self._y, self._w, self._h)
			self._layout.update()

	def show(self):
		pass




class CuMainWindow(CuWidget):
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)

class CuPanel(CuWidget):
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)
