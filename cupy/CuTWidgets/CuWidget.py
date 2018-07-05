'''
    Widget
'''

import logging
import os
from CuT.CuTHelper import CuWrapper
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

		if 'parent' in kwargs: self._data['parent'] = kwargs['parent']
		else : self._data['parent'] = None; CuApplication.setMainWidget(self)
		if 'name' in kwargs: self._data['name'] = kwargs['name']
		else : self._data['name'] = ''
		if 'x' in kwargs: self._data['x'] = kwargs['x']
		else : self._data['x'] = 0
		if 'y' in kwargs: self._data['y'] = kwargs['y']
		else : self._data['y'] = 0
		if 'w' in kwargs: self._data['w'] = kwargs['w']
		else : self._data['w'] = CuApplication.getW()
		if 'h' in kwargs: self._data['h'] = kwargs['h']
		else : self._data['h'] = CuApplication.getH()
		self._data['childs'] = []
		self._data['win'] = CuWrapper.newWin(self._data['x'], self._data['y'], self._data['w'], self._data['h'])
		self._data['layout'] = None
		self._data['border'] = False
		self._data['borderSize'] = 0
		self.hide()

	def accessibleName(self):
		return self._data['name']

	def setAccessibleName(self, name):
		self._data['name'] = name


	def border(self):
		return self._data['border']

	def setBorder(self, bool):
		self._data['border'] = bool
		if bool:
			self._data['borderSize'] = 1
			self._data['win'].box()
		else:
			self._data['borderSize'] = 0
			self._data['win'].clear()

	def getWin(self):
		return self._data['win']

	def paintEvent(self, event):
		if self._data['layout'] is not None:
			self._data['layout'].paintEvent(event)

	def mouseDoubleClickEvent(self, evt): pass
	def mouseMoveEvent(self, evt): pass
	def mousePressEvent(self, evt): pass
	def mouseReleaseEvent(self, evt): pass

	def event(self, evt):
		# handle own events
		if evt.type() == CuT.LeftButton or evt.type() == CuT.RightButton or evt.type() == CuT.MidButton:
			if   evt.button() == CuEvent.MouseButtonRelease:
				self.mouseReleaseEvent(evt)
			elif evt.button() == CuEvent.MouseButtonPress:
				self.mousePressEvent(evt)
		if evt.type() == CuT.NoButton:
			if evt.button() == CuEvent.MouseMove:
				self.mouseMoveEvent(evt)

		# Trigger this event to the childs
		if self._data['layout'] is not None:
			for i in range(self._data['layout'].count()):
				item = self._data['layout'].itemAt(i)
				if isinstance(item, CuWidgetItem) and not item.isEmpty():
					widget = item.widget()
					if isinstance(evt, CuMouseEvent):
						wx, wy = widget.pos()
						ww, wh = widget.size()
						ewx, ewy = evt.windowPos()
						esx, esy = evt.screenPos()
						lx, ly = esx-wx, esy-wy
						if lx >= 0 and ly >= 0 and lx < ww and ly < wh:
							# ex,  ey  = evt.pos()
							wevt = CuMouseEvent(
								type=evt.type(),
								localPos  = {'x':lx,  'y':ly},
								windowPos = {'x':ewx, 'y':ewy},
								screenPos = {'x':esx, 'y':esy},
								button=evt.button())
							if widget.event(wevt): return True
						continue
					if widget.event(evt): return True


	def setLayout(self, layout):
		if isinstance(layout, CuLayout):
			self._data['layout'] = layout
			self._data['layout'].setParent(self)
			bs = self._data['borderSize']
			self._data['layout'].setGeometry(self._data['x']+bs, self._data['y']+bs, self.width(), self.height())
			self._data['layout'].update()
		else:
			raise Exception(str(layout) + ' not of type CuLayout')

	def layout(self): return self._data['layout']

	def x(self): return self._data['x']
	def y(self): return self._data['y']
	def width(self):  return self._data['w']
	def height(self): return self._data['h']

	def pos(self): return self._data['x'], self._data['y']
	def size(self):   return self._data['w'], self._data['h']

	def maximumSize(self):
		return self.maximumWidth(), self.maximumHeight()
	def maximumHeight(self):
		wMaxH = self._extra['maxh'] + 2*self._data['borderSize']
		lMaxH = 1000000
		if self._data['layout'] is not None:
			lMaxH = self._data['layout'].maximumHeight() + 2*self._data['borderSize']
			if lMaxH < wMaxH:
				return lMaxH
		return wMaxH
	def maximumWidth(self):
		wMaxW = self._extra['maxw'] + 2*self._data['borderSize']
		lMaxW = 1000000
		if self._data['layout'] is not None:
			lMaxW = self._data['layout'].maximumWidth() + 2*self._data['borderSize']
			if lMaxW < wMaxW:
				return lMaxW
		return wMaxW

	def minimumSize(self):
		return self.minimumWidth(), self.minimumHeight()
	def minimumHeight(self):
		wMinH = self._extra['minh'] + 2*self._data['borderSize']
		lMinH = 1000000
		if self._data['layout'] is not None:
			lMinH = self._data['layout'].minimumHeight() + 2*self._data['borderSize']
			if lMinH > wMinH:
				return lMinH
		return wMinH
	def minimumWidth(self):
		wMinW = self._extra['minw'] + 2*self._data['borderSize']
		lMinW = 1000000
		if self._data['layout'] is not None:
			lMinW = self._data['layout'].minimumWidth() + 2*self._data['borderSize']
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
		# self._data['win'].clear()
		# logging.debug(__name__ + "x:" + str(self._data['x']) + " y:" + str(self._data['y']))
		newx = x
		newy = y
		if newx < 0: newx=0
		if newy < 0: newy=0
		if newx+self._data['w'] > CuApplication.getW() : newx=CuApplication.getW()-self._data['w']
		if newy+self._data['h'] > CuApplication.getH() : newy=CuApplication.getH()-self._data['h']
		self._data['x'] = newx
		self._data['y'] = newy
		# logging.debug(__name__ + "  Visible:    " + str(self._data['visible']))
		# logging.debug(__name__ + "  Move:    " + str((self._data['x'], self._data['y'],self._data['h'],self._data['w'])))
		self._data['win'].move(self._data['x'], self._data['y'])

	def resize(self, w, h):
		neww = w
		newh = h
		if neww < 0: neww=0
		if newh < 0: newh=0
		if neww+self._data['x'] > CuApplication.getW() : neww=CuApplication.getW()-self._data['x']
		if newh+self._data['y'] > CuApplication.getH() : newh=CuApplication.getH()-self._data['y']
		self._data['w'] = neww
		self._data['h'] = newh
		self._data['win'].clear()
		self._data['win'].resize(self._data['w'],self._data['h'])

		if self._data['border']:
			self._data['win'].box()

	def setGeometry(self, x, y, w, h):
		# logging.debug("FROM:"+str({"SELF":self._data['name'], "x":x,"y":y,"w":w,"h":h}))
		# logging.debug("TO:  "+str({"SELF":self._data['name'], "x":self._data['x'],"y":self._data['y'],"w":self._data['w'],"h":self._data['h}']))
		if self._data['w'] == w and self._data['h'] == h:
			if self._data['x'] != x or self._data['y'] != y:
				'''
					Little Hack to avoid a crash if exiting from the "Too Small Menu"
					self._data['visible']

				'''
				self.resize(w, h)
				self.move(x, y)
			else:
				return
		elif self._data['x'] == x and self._data['y'] == y:
			self.resize(w, h)
		elif self._data['x'] + w < CuApplication.getW() and self._data['y'] + h < CuApplication.getH():
			self.resize(w, h)
			self.move(x, y)
		else:
			# logging.debug("EXTRA:"+str({"SELF":self._data['name'], "x":self._data['x'],"y":self._data['y'],"w":self._data['w'],"h":self._data['h}']))
			self._data['x'] = x
			self._data['y'] = y
			self._data['w'] = w
			self._data['h'] = h
			self.resize(w, h)
			self.move(x, y)

		if self._data['layout'] is not None:
			bs = self._data['borderSize']
			self._data['layout'].setGeometry(self._data['x']+bs, self._data['y']+bs, self._data['w']-2*bs, self._data['h']-2*bs)
			self._data['layout'].update()

	#def setMaximumSize(self, maxw: int, maxh: int): pass
	#def setMinimumSize(self, minw: int, minh: int): pass

	def show(self):
		self._data['win'].show()
		self._data['visible'] = True
		if self._data['layout'] is not None:
			for i in range(self._data['layout'].count()):
				item = self._data['layout'].itemAt(i)
				if isinstance(item, CuWidgetItem) and not item.isEmpty():
					item.widget().show()

	def hide(self):
		self._data['win'].hide()
		self._data['visible'] = False
		if self._data['layout'] is not None:
			for i in range(self._data['layout'].count()):
				item = self._data['layout'].itemAt(i)
				if isinstance(item, CuWidgetItem) and not item.isEmpty():
					item.widget().hide()

	def isVisible(self):
		return self._data['visible']

	def update(self):
		CuApplication.addUpdateWidget(self)
		if self._data['layout'] is not None:
			self._data['layout'].update()


class CuMainWindow(CuWidget):
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)

class CuPanel(CuWidget):
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)
