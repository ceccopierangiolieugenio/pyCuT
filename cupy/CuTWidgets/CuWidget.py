'''
    Widget
'''

import logging
import os
from CuT.CuTHelper import CuWrapper, CuHelper
from CuT.CuTCore import CuEvent, CuMouseEvent

from .CuLayout import *
from .CuApplication import *



class CuWidget:
	def __init__(self, *args, **kwargs):
		if not CuApplication.is_initialized():
			print(self.__class__.__name__ + ": Must construct a CuApplication before a CuWidget")
			os.abort()

		self._extra = {
				'maxw' : 100000,
				'maxh' : 100000,
				'minw' : 0,
				'minh' : 0,
			}
		self._data = {}

		self._data['parent'] = kwargs.get('parent', None )
		self._data['name'] = kwargs.get('name', '')
		self._data['x'] = kwargs.get('x', 0)
		self._data['y'] = kwargs.get('y', 0)
		self._data['w'] = kwargs.get('w', CuApplication.getW())
		self._data['h'] = kwargs.get('h', CuApplication.getH())

		if self._data['parent'] is None:
			CuApplication.setMainWidget(self)

		self._data['childs'] = []
		self._data['win'] = CuWrapper.newWin(self, self._data['x'], self._data['y'], self._data['w'], self._data['h'])
		self._data['layout'] = None
		self._data['mouse'] = {'underMouse':False}
		self.hide()

	def accessibleName(self):
		return self._data['name']

	def setAccessibleName(self, name):
		self._data['name'] = name

	def getWin(self):
		return self._data['win']

	def paintEvent(self, event): pass

	def underMouse(self):
		return self._data['mouse']['underMouse']

	def mouseDoubleClickEvent(self, evt): pass
	def mouseMoveEvent(self, evt): pass
	def mousePressEvent(self, evt): pass
	def mouseReleaseEvent(self, evt): pass
	def wheelEvent(self, evt): pass
	def enterEvent(self, evt): pass
	def leaveEvent(self, evt): pass

	@staticmethod
	def _broadcastLeaveEvent(evt, layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				if item.widget()._data['mouse']['underMouse']:
					item.widget()._data['mouse']['underMouse'] = False
					item.widget().leaveEvent(evt)
			elif isinstance(item, CuLayout):
				CuWidget._broadcastLeaveEvent(evt, item)

	@staticmethod
	def _eventLayoutHandle(evt, layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				widget = item.widget()
				wevt = None
				mouseEvent = False
				if isinstance(evt, CuMouseEvent):
					mouseEvent = True
					wx, wy = CuHelper.absPos(widget)
					ww, wh = widget.size()
					ewx, ewy = evt.windowPos()
					esx, esy = evt.screenPos()
					lx, ly = esx-wx, esy-wy
					# Skip the mouse event if outside this widget
					if lx >= 0 and ly >= 0 and lx < ww and ly < wh:
						# ex,  ey  = evt.pos()
						wevt = CuMouseEvent(
							type=evt.type(),
							localPos  = {'x':lx,  'y':ly},
							windowPos = {'x':ewx, 'y':ewy},
							screenPos = {'x':esx, 'y':esy},
							button=evt.button())
				if isinstance(evt, CuWheelEvent):
					mouseEvent = True
					wx, wy = CuHelper.absPos(widget)
					ww, wh = widget.size()
					egx, egy = evt.globalPos()
					lx, ly = egx-wx, egy-wy
					# Skip the mouse event if outside this widget
					if lx >= 0 and ly >= 0 and lx < ww and ly < wh:
						wevt = CuWheelEvent(
							type=evt.type(),
							pos  = {'x':lx,  'y':ly},
							globalPos = {'x':egx,     'y':egy},
							angleDelta=evt.angleDelta())
				if mouseEvent:
					if wevt is not None:
						if not widget._data['mouse']['underMouse']:
							widget._data['mouse']['underMouse'] = True
							widget.enterEvent(wevt)
						if widget.event(wevt):
							return True
					else:
						if widget._data['mouse']['underMouse']:
							widget._data['mouse']['underMouse'] = False
							widget.leaveEvent(evt)
						if widget._data['layout'] is not None:
							CuWidget._broadcastLeaveEvent(evt, widget._data['layout'])
					continue

				if widget.event(evt):
					return True
			elif isinstance(item, CuLayout):
				if CuWidget._eventLayoutHandle(evt, item):
					return True
		return False

	def event(self, evt):
		# handle own events
		if evt.type() == CuT.NoButton:
			if evt.button() == CuEvent.MouseMove:
				self.mouseMoveEvent(evt)
		elif evt.type() == CuT.LeftButton or evt.type() == CuT.RightButton or evt.type() == CuT.MidButton:
			if   evt.button() == CuEvent.MouseButtonRelease:
				self.mouseReleaseEvent(evt)
			elif evt.button() == CuEvent.MouseButtonPress:
				self.mousePressEvent(evt)
		elif evt.type() == CuT.ForwardButton:
			self.wheelEvent(evt)

		# Trigger this event to the childs
		if self._data['layout'] is not None:
			return CuWidget._eventLayoutHandle(evt, self._data['layout'])


	def setLayout(self, layout):
		if isinstance(layout, CuLayout):
			self._data['layout'] = layout
			self._data['layout'].setParent(self)
			self._data['layout'].setGeometry(0, 0, self.width(), self.height())
			self._data['layout'].update()
		else:
			raise Exception(str(layout) + ' not of type CuLayout')

	def layout(self): return self._data['layout']

	def setParent(self, parent):
		self._data['parent'] = parent
	def parentWidget(self):
		return self._data['parent']

	def x(self): return self._data['x']
	def y(self): return self._data['y']
	def width(self):  return self._data['w']
	def height(self): return self._data['h']

	def pos(self): return self._data['x'], self._data['y']
	def size(self):   return self._data['w'], self._data['h']

	def maximumSize(self):
		return self.maximumWidth(), self.maximumHeight()
	def maximumHeight(self):
		wMaxH = self._extra['maxh']
		lMaxH = 1000000
		if self._data['layout'] is not None:
			lMaxH = self._data['layout'].maximumHeight()
			if lMaxH < wMaxH:
				return lMaxH
		return wMaxH
	def maximumWidth(self):
		wMaxW = self._extra['maxw']
		lMaxW = 1000000
		if self._data['layout'] is not None:
			lMaxW = self._data['layout'].maximumWidth()
			if lMaxW < wMaxW:
				return lMaxW
		return wMaxW

	def minimumSize(self):
		return self.minimumWidth(), self.minimumHeight()
	def minimumHeight(self):
		wMinH = self._extra['minh']
		lMinH = 1000000
		if self._data['layout'] is not None:
			lMinH = self._data['layout'].minimumHeight()
			if lMinH > wMinH:
				return lMinH
		return wMinH
	def minimumWidth(self):
		wMinW = self._extra['minw']
		lMinW = 1000000
		if self._data['layout'] is not None:
			lMinW = self._data['layout'].minimumWidth()
			if lMinW > wMinW:
				return lMinW
		return wMinW

	def setMaximumSize(self, maxw, maxh): self._extra['maxw'] = maxw; self._extra['maxh'] = maxh
	def setMaximumHeight(self, maxh):     self._extra['maxh'] = maxh
	def setMaximumWidth(self, maxw):      self._extra['maxw'] = maxw

	def setMinimumSize(self, minw, minh): self._extra['minw'] = minw; self._extra['minh'] = minh
	def setMinimumHeight(self, minh):     self._extra['minh'] = minh
	def setMinimumWidth(self, minw):      self._extra['minw'] = minw

	def move(self, x, y):
		self._data['x'] = x
		self._data['y'] = y
		self._data['win'].move(self._data['x'], self._data['y'])
		if self._data['layout'] is not None:
			self._data['layout'].setGeometry(self._data['x'], self._data['y'], self._data['w'], self._data['h'])
		self.update()

	def resize(self, w, h):
		self._data['w'] = w
		self._data['h'] = h
		self._data['win'].resize(self._data['w'],self._data['h'])
		if self._data['layout'] is not None:
			self._data['layout'].setGeometry(self._data['x'], self._data['y'], self._data['w'], self._data['h'])
		self.update()

	def setGeometry(self, x, y, w, h):
		#logging.debug("FROM:"+str({"SELF":self._data['name'], "x":x,"y":y,"w":w,"h":h}))
		self.resize(w, h)
		self.move(x, y)

	@staticmethod
	def _showHandle(layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				item.widget().show()
			elif isinstance(item, CuLayout):
				CuWidget._showHandle(item)

	def show(self):
		self._data['win'].show()
		self._data['visible'] = True
		if self._data['layout'] is not None:
			CuWidget._showHandle(self._data['layout'])

	@staticmethod
	def _hideHandle(layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				item.widget().hide()
			elif isinstance(item, CuLayout):
				CuWidget._hideHandle(item)

	def hide(self):
		self._data['win'].hide()
		self._data['visible'] = False
		if self._data['layout'] is not None:
			CuWidget._hideHandle(self._data['layout'])

	def isVisible(self):
		return self._data['visible']

	def update(self):
		CuApplication.addUpdateWidget(self)
		if self._data['layout'] is not None:
			self._data['layout'].update()
