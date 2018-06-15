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
		return self.minimumWidth(), self.minimumHeight()
	def minimumHeight(self): return 0
	def minimumWidth(self): return 0

	def maximumSize(self):
		return self.maximumWidth(), self.maximumHeight()
	def maximumHeight(self): return 1000000
	def maximumWidth(self):  return 1000000

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

	def count(self):
		return len(self._widgets)

	def itemAt(self, index):
		if index < len(self._widgets):
			return self._widgets[index]
		return 0

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

	def minimumWidth(self):
		''' process the widgets and get the min size '''
		minw = 0
		for widget in self._widgets:
			w1  = widget.minimumWidth()
			minw += w1
		return minw

	def minimumHeight(self):
		''' process the widgets and get the min size '''
		minh = CuLayout.minimumHeight(self)
		for widget in self._widgets:
			h1  = widget.minimumHeight()
			if h1 > minh : minh = h1
		return minh

	def maximumWidth(self):
		''' process the widgets and get the min size '''
		maxw = 0
		for widget in self._widgets:
			w1 = widget.maximumWidth()
			maxw += w1
		return maxw

	def maximumHeight(self):
		''' process the widgets and get the min size '''
		maxh = CuLayout.maximumHeight(self)
		for widget in self._widgets:
			h1  = widget.maximumHeight()
			if h1 < maxh : maxh = h1
		return maxh

	def update(self):
		x, y, w, h = self.geometry()
		numWidgets = len(self._widgets)
		leftWidgets = numWidgets
		freeWidth = w
		newx = x
		for widget in self._widgets:
			sliceSize = freeWidth//leftWidgets
			maxw = widget.maximumWidth()
			minw = widget.minimumWidth()
			if   sliceSize > maxw: sliceSize = maxw
			elif sliceSize < minw: sliceSize = minw
			widget.setGeometry(newx, y, sliceSize, h)
			newx += sliceSize
			freeWidth -= sliceSize
			leftWidgets -= 1


class CuVBoxLayout(CuLayout):
	def __init__(self):
		CuLayout.__init__(self)

	def minimumWidth(self):
		''' process the widgets and get the min size '''
		minw = CuLayout.minimumWidth(self)
		for widget in self._widgets:
			w1  = widget.minimumWidth()
			if w1 > minw : minw = w1
		return minw

	def minimumHeight(self):
		''' process the widgets and get the min size '''
		minh = 0
		for widget in self._widgets:
			h1  = widget.minimumHeight()
			minh += h1
		return minh

	def maximumWidth(self):
		''' process the widgets and get the min size '''
		maxw = CuLayout.maximumWidth(self)
		for widget in self._widgets:
			w1  = widget.maximumWidth()
			if w1 < maxw : maxw = w1
		return maxw

	def maximumHeight(self):
		''' process the widgets and get the min size '''
		maxh = 0
		for widget in self._widgets:
			h1 = widget.maximumHeight()
			maxh += h1
		return maxh

	def update(self):
		x, y, w, h = self.geometry()
		numWidgets = len(self._widgets)
		leftWidgets = numWidgets
		freeHeight = h
		newy = y
		for widget in self._widgets:
			sliceSize = freeHeight//leftWidgets
			maxh = widget.maximumHeight()
			minh = widget.minimumHeight()
			if   sliceSize > maxh: sliceSize = maxh
			elif sliceSize < minh: sliceSize = minh
			widget.setGeometry(x, newy, w, sliceSize)
			newy += sliceSize
			freeHeight -= sliceSize
			leftWidgets -= 1
