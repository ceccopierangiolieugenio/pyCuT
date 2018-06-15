'''
    Widget
'''

import curses, curses.panel
import logging
import os

from .CuLayout import *
from .CuApplication import *


class CuWidget:
	def __init__(self, *args, **kwargs):
		if not CuApplication.is_initialized():
			print(self._data['__class__'].__name__ + ": Must construct a CuApplication before a CuWidget")
			os.abort()
		self._extra = {}
		self._data = {}
		if 'parent' in kwargs: self._data['_parent'] = kwargs['parent']
		else : self._data['_parent'] = None; CuApplication.setMainWidget(self)
		if 'name' in kwargs: self._data['_name'] = kwargs['name']
		else : self._data['_name'] = ''
		if 'x' in kwargs: self._data['_x'] = kwargs['x']
		else : self._data['_x'] = 0
		if 'y' in kwargs: self._data['_y'] = kwargs['y']
		else : self._data['_y'] = 0
		if 'w' in kwargs: self._data['_w'] = kwargs['w']
		else : self._data['_w'] = CuApplication.getW()
		if 'h' in kwargs: self._data['_h'] = kwargs['h']
		else : self._data['_h'] = CuApplication.getH()
		self._data['_childs'] = []
		self._data['_win'] = curses.newwin(self._data['_h'], self._data['_w'], self._data['_y'], self._data['_x'])
		self._data['_panel'] = curses.panel.new_panel(self._data['_win'])
		self._data['_layout'] = None
		self._data['_border'] = False

	def accessibleName(self):
		return self._data['_name']

	def setAccessibleName(self, name):
		self._data['_name'] = name


	def getPos(self):
		return self._data['_x'], self._data['_y']

	def move(self, x, y):
		# self._data['_win'].clear()
		# logging.debug(__name__ + "x:" + str(self._data['_x']) + " y:" + str(self._data['_y']))
		newx = x
		newy = y
		if newx < 0: newx=0
		if newy < 0: newy=0
		if newx+self._data['_w'] > CuApplication.getW() : newx=CuApplication.getW()-self._data['_w']
		if newy+self._data['_h'] > CuApplication.getH() : newy=CuApplication.getH()-self._data['_h']
		self._data['_x'] = newx
		self._data['_y'] = newy
		self._data['_panel'].move(self._data['_y'], self._data['_x'])

	def setBorder(self, bool):
		self._data['_border'] = bool
		if bool:
			self._data['_win'].box()
		else:
			self._data['_win'].clear()

	def resize(self, w, h):
		neww = w
		newh = h
		if neww < 0: neww=0
		if newh < 0: newh=0
		if neww+self._data['_x'] > CuApplication.getW() : neww=CuApplication.getW()-self._data['_x']
		if newh+self._data['_y'] > CuApplication.getH() : newh=CuApplication.getH()-self._data['_y']
		self._data['_w'] = neww
		self._data['_h'] = newh
		self._data['_win'].clear()
		self._data['_win'].resize(self._data['_h'],self._data['_w'])

		if self._data['_border']:
			self._data['_win'].box()

	def getWin(self):
		return self._data['_win']

	def paint(self):
		if self._data['_layout'] is not None:
			self._data['_layout'].paint()

	def event(self, evt):
		if self._data['_layout'] is not None:
			self._data['_layout'].event(evt)

	def setLayout(self, layout):
		if isinstance(layout, CuLayout):
			self._data['_layout'] = layout
			self._data['_layout'].setParent(self)
			if self._data['_border']:
				self._data['_layout'].setGeometry(self._data['_x']+1, self._data['_y']+1, self._data['_w']-2, self._data['_h']-2)
			else:
				self._data['_layout'].setGeometry(self._data['_x'], self._data['_y'], self._data['_w'], self._data['_h'])
			self._data['_layout'].update()
		else:
			raise Exception(str(layout) + ' not of type CuLayout')

	def layout(self): return self._data['_layout']

	def x(self): return self._data['_x']
	def y(self): return self._data['_y']
	def width(self):  return self._data['_w']
	def height(self): return self._data['_h']

	def setGeometry(self, x, y, w, h):
		# logging.debug("FROM:"+str({"SELF":self._data['_name'], "x":x,"y":y,"w":w,"h":h}))
		# logging.debug("TO:  "+str({"SELF":self._data['_name'], "x":self._data['_x'],"y":self._data['_y'],"w":self._data['_w'],"h":self._data['_h}']))
		if self._data['_w'] == w and self._data['_h'] == h:
			if self._data['_x'] != x or self._data['_y'] != y:
				self.move(x, y)
			else:
				return
		elif self._data['_x'] == x and self._data['_y'] == y:
			self.resize(w, h)
		elif self._data['_x'] + w < CuApplication.getW() and self._data['_y'] + h < CuApplication.getH():
			self.resize(w, h)
			self.move(x, y)
		else:
			# logging.debug("EXTRA:"+str({"SELF":self._data['_name'], "x":self._data['_x'],"y":self._data['_y'],"w":self._data['_w'],"h":self._data['_h}']))
			self._data['_x'] = x
			self._data['_y'] = y
			self._data['_w'] = w
			self._data['_h'] = h
			self.resize(w, h)
			self.move(x, y)

		if self._data['_layout'] is not None:
			if self._data['_border']:
				self._data['_layout'].setGeometry(self._data['_x']+1, self._data['_y']+1, self._data['_w']-2, self._data['_h']-2)
			else:
				self._data['_layout'].setGeometry(self._data['_x'], self._data['_y'], self._data['_w'], self._data['_h'])
			self._data['_layout'].update()

	#def setMaximumHeight(self, maxh: int) -> None :
	#	pass
	#def setMaximumWidth(self, maxw: int): pass
	#def setMinimumHeight(self, minh: int): pass
	#def setMinimumWidth(self, minw: int): pass

	#def setMaximumSize(self, maxw: int, maxh: int): pass
	#def setMinimumSize(self, minw: int, minh: int): pass


	def show(self):
		pass




class CuMainWindow(CuWidget):
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)

class CuPanel(CuWidget):
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)
