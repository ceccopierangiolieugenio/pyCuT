'''
    Layout System
'''

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
		self._items = []
		self._parent = None
		pass

	def children(self):
		return self._items

	def count(self):
		return len(self._items)

	def itemAt(self, index):
		if index < len(self._items):
			return self._items[index]
		return 0

	def setParent(self, parent):
		self._parent = parent

	def parentWidget(self):
		return self._parent

	def addItem(self, item):
		self._items.append(item)

	def addWidget(self, widget):
		self.addItem(CuWidgetItem(widget))

	def removeWidget(self, widget):
		for i in self._items:
			if i.widget() == widget:
				self._items.remove(i)
				return

	def update(self):
		for i in self.children():
			if isinstance(i, CuWidgetItem) and not i.isEmpty():
				i.widget().update()
			elif isinstance(i, CuLayout):
				i.update()

	def paintEvent(self, event):
		for i in self.children():
			if isinstance(i, CuWidgetItem) and not i.isEmpty():
				i.widget().paintEvent(event)
			elif isinstance(i, CuLayout):
					i.paintEvent(event)

class CuWidgetItem(CuLayoutItem):
	def __init__(self, widget):
		CuLayoutItem.__init__(self)
		self._widget = widget

	def widget(self):
		return self._widget

	def isEmpty(self): return self._widget is None

	def minimumSize(self):   return self._widget.minimumSize()
	def minimumHeight(self): return self._widget.minimumHeight()
	def minimumWidth(self):  return self._widget.minimumWidth()
	def maximumSize(self):   return self._widget.maximumSize()
	def maximumHeight(self): return self._widget.maximumHeight()
	def maximumWidth(self):  return self._widget.maximumWidth()

	def geometry(self):      return self._widget.geometry()

	def setGeometry(self, x, y, w, h):
		self._widget.setGeometry(x, y, w, h)



class CuHBoxLayout(CuLayout):
	def __init__(self):
		CuLayout.__init__(self)

	def minimumWidth(self):
		''' process the widgets and get the min size '''
		minw = 0
		for widget in self._items:
			w1  = widget.minimumWidth()
			minw += w1
		return minw

	def minimumHeight(self):
		''' process the widgets and get the min size '''
		minh = CuLayout.minimumHeight(self)
		for widget in self._items:
			h1  = widget.minimumHeight()
			if h1 > minh : minh = h1
		return minh

	def maximumWidth(self):
		''' process the widgets and get the min size '''
		maxw = 0
		for widget in self._items:
			w1 = widget.maximumWidth()
			maxw += w1
		return maxw

	def maximumHeight(self):
		''' process the widgets and get the min size '''
		maxh = CuLayout.maximumHeight(self)
		for widget in self._items:
			h1  = widget.maximumHeight()
			if h1 < maxh : maxh = h1
		return maxh

	def update(self):
		x, y, w, h = self.geometry()
		numWidgets = self.count()
		leftWidgets = numWidgets
		freeWidth = w
		newx = x
		for item in self.children():
			sliceSize = freeWidth//leftWidgets
			maxw = item.maximumWidth()
			minw = item.minimumWidth()
			if   sliceSize > maxw: sliceSize = maxw
			elif sliceSize < minw: sliceSize = minw
			item.setGeometry(newx, y, sliceSize, h)
			newx += sliceSize
			freeWidth -= sliceSize
			leftWidgets -= 1
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				item.widget().update()
			elif isinstance(item, CuLayout):
				item.update()


class CuVBoxLayout(CuLayout):
	def __init__(self):
		CuLayout.__init__(self)

	def minimumWidth(self):
		''' process the widgets and get the min size '''
		minw = CuLayout.minimumWidth(self)
		for widget in self._items:
			w1  = widget.minimumWidth()
			if w1 > minw : minw = w1
		return minw

	def minimumHeight(self):
		''' process the widgets and get the min size '''
		minh = 0
		for widget in self._items:
			h1  = widget.minimumHeight()
			minh += h1
		return minh

	def maximumWidth(self):
		''' process the widgets and get the min size '''
		maxw = CuLayout.maximumWidth(self)
		for widget in self._items:
			w1  = widget.maximumWidth()
			if w1 < maxw : maxw = w1
		return maxw

	def maximumHeight(self):
		''' process the widgets and get the min size '''
		maxh = 0
		for widget in self._items:
			h1 = widget.maximumHeight()
			maxh += h1
		return maxh

	def update(self):
		x, y, w, h = self.geometry()
		numWidgets = self.count()
		leftWidgets = numWidgets
		freeHeight = h
		newy = y
		for item in self.children():
			sliceSize = freeHeight//leftWidgets
			maxh = item.maximumHeight()
			minh = item.minimumHeight()
			if   sliceSize > maxh: sliceSize = maxh
			elif sliceSize < minh: sliceSize = minh
			item.setGeometry(x, newy, w, sliceSize)
			newy += sliceSize
			freeHeight -= sliceSize
			leftWidgets -= 1
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				item.widget().update()
			elif isinstance(item, CuLayout):
				item.update()
