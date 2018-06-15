'''
    Layout System
'''

import curses, curses.panel
import logging

class CuLayoutItem:
	_x, _y, _w, _h = 0, 0, 0, 0
	def __init__(self):
		pass

	def minimumSize(self):
		return 0, 0

	def geometry(self):
		return self._x, self._y, self._w, self._h

	def setGeometry(self, x, y, w, h):
		self._x = x
		self._y = y
		self._w = w
		self._h = h


class CuLayout(CuLayoutItem):
	def __init__(self):
		CuLayoutItem.__init__(self)
		self._widgets = []
		self._parent = None
		pass

	def setParent(self, parent):
		self._parent = parent

	def parentWidget(self):
		return self._parent

	def addWidget(self, widget):
		self._widgets.append(widget)

	def removeWidget(self, widget):
		self._widgets.remove(widget)

	def update(self):
		pass

	def paint(self):
		for widget in self._widgets:
			widget.paint()

	def event(self, evt):
		for widget in self._widgets:
			widget.event(evt)


class CuHBoxLayout(CuLayout):
	def __init__(self):
		CuLayout.__init__(self)

	def minimumSize(self):
		''' process the widgets and get the min size '''
		if len(self._widgets) == 0:
			return 0, 0
		w, h = (0, 100000)
		for widget in self._widgets:
			w1, h1  = widget.minimumSize()
			w += w1
			if h1 < h : h = h1
		return w, h

	def update(self):
		x, y, w, h = self.geometry()
		numWidgets = len(self._widgets)
		leftWidgets = numWidgets
		freeWidth = w
		newx = x
		for widget in self._widgets:
			sliceSize = freeWidth//leftWidgets
			widget.setGeometry(newx, y, sliceSize, h)
			newx += sliceSize
			freeWidth -= sliceSize
			leftWidgets -= 1

class CuVBoxLayout(CuLayout):
	def __init__(self):
		CuLayout.__init__(self)

	def minimumSize(self):
		''' process the widgets and get the min size '''
		if len(self._widgets) == 0:
			return 0, 0
		w, h = (100000, 0)
		for widget in self._widgets:
			w1, h1  = widget.minimumSize()
			h += h1
			if w1 < w : w = w1
		return w, h

	def update(self):
		x, y, w, h = self.geometry()
		numWidgets = len(self._widgets)
		leftWidgets = numWidgets
		freeHeight = h
		newy = y
		for widget in self._widgets:
			sliceSize = freeHeight//leftWidgets
			widget.setGeometry(x, newy, w, sliceSize)
			newy += sliceSize
			freeHeight -= sliceSize
			leftWidgets -= 1
