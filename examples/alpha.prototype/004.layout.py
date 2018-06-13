#!/usr/bin/python
'''
https://stackoverflow.com/questions/9254664/python-curses-getmouse?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
'''
import curses, curses.panel
import math
import logging

GLBL = {
	'maxY' : 0,
	'maxX' : 0,
	'screen' : None
	}

class CuEvent:
	ERR = 0
	KEY_MOUSE = 1

	def __init__(self, type=ERR):
		self.type = type;

class CuMouseEvent(CuEvent):
	_id, _x, _y, _z, _bstate = 0, 0, 0, 0, 0

	MOUSE_PRESSED = 1
	MOUSE_RELEASED = 2
	MOUSE_CLICKED = 3
	MOUSE_DOUBLE_CLICKED = 4
	MOUSE_TRIPLE_CLICKED = 5

	REPORT_MOUSE_POSITION = 1000

	def __init__(self):
		CuEvent.__init__(self,type=CuEvent.KEY_MOUSE)
		self._id, self._x, self._y, self._z, self._bstate = curses.getmouse()

	def getmouse(self):
		return self._id, self._x, self._y, self._z, self._bstate

	def globalPos(self):
		return self._x, self._y

	def getState(self):
		if self._bstate == curses.BUTTON1_PRESSED:        return CuMouseEvent.MOUSE_PRESSED
		if self._bstate == curses.BUTTON1_RELEASED:       return CuMouseEvent.MOUSE_RELEASED
		if self._bstate == curses.BUTTON1_CLICKED:        return CuMouseEvent.MOUSE_CLICKED
		if self._bstate == curses.BUTTON1_DOUBLE_CLICKED: return CuMouseEvent.MOUSE_DOUBLE_CLICKED
		if self._bstate == curses.BUTTON1_TRIPLE_CLICKED: return CuMouseEvent.MOUSE_TRIPLE_CLICKED
		if self._bstate == curses.REPORT_MOUSE_POSITION:  return CuMouseEvent.REPORT_MOUSE_POSITION
		return None

'''
    Layout System
'''

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


class CuHLayout(CuLayout):
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
			sliceSize = int(math.floor(freeWidth/leftWidgets))
			widget.setGeometry(newx, y, sliceSize, h)
			newx += sliceSize
			freeWidth -= sliceSize
			leftWidgets -= 1

class CuVLayout(CuLayout):
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
			sliceSize = int(math.floor(freeHeight/leftWidgets))
			widget.setGeometry(x, newy, w, sliceSize)
			newy += sliceSize
			freeHeight -= sliceSize
			leftWidgets -= 1



'''
    Widget
'''

class CuWidget:
	_win = None
	_panel = None
	_layout = None
	_x, _y, _w, _h = 0, 0, 0, 0
	_childs = None
	_parent = None
	_border = False

	def __init__(self, *args, **kwargs):
		logging.debug(str(kwargs))
		if 'parent' in kwargs: self._parent = kwargs['parent']
		else : self._parent = None
		if 'name' in kwargs: self._name = kwargs['name']
		else : self._name = ''
		if 'x' in kwargs: self._x = kwargs['x']
		else : self._x = 0
		if 'y' in kwargs: self._y = kwargs['y']
		else : self._y = 0
		if 'w' in kwargs: self._w = kwargs['w']
		else : self._w = GLBL['maxX']
		if 'h' in kwargs: self._h = kwargs['h']
		else : self._h = GLBL['maxY']
		self._childs = []
		self._win = curses.newwin(self._h, self._w, self._y, self._x)
		self._panel = curses.panel.new_panel(self._win)

	def getPos(self):
		return self._x, self._y

	def move(self, x, y):
		# self._win.clear()
		# logging.debug(__name__ + "x:" + str(self._x) + " y:" + str(self._y))
		newx = x
		newy = y
		if newx < 0: newx=0
		if newy < 0: newy=0
		if newx+self._w > GLBL['maxX'] : newx=GLBL['maxX']-self._w
		if newy+self._h > GLBL['maxY'] : newy=GLBL['maxY']-self._h
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
		if neww+self._x > GLBL['maxX'] : neww=GLBL['maxX']-self._x
		if newh+self._y > GLBL['maxY'] : newh=GLBL['maxY']-self._y
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
			self._layout.setGeometry(self._x+1, self._y+1, self._w-2, self._h-2)
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
		elif self._x + w < GLBL['maxX'] and self._y + h < GLBL['maxY']:
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



class CuTestInput(CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0
	_iterator = 0

	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)

	def paint(self):
		CuWidget.paint(self)
		# self.getWin().clear()
		self.getWin().addstr(3, 3, "CuTestInput... [" + self._name + "] it: " + str(self._iterator))
		self.getWin().addstr(4, 3, "    id: " + str(self._id))
		self.getWin().addstr(5, 3, "     x: " + str(self._ix))
		self.getWin().addstr(6, 3, "     y: " + str(self._iy))
		self.getWin().addstr(7, 3, "     z: " + str(self._iz))
		self.getWin().addstr(8, 3, "bstate: " + str(self._bstate) + "        ")
		self.getWin().addstr(9, 3, "childs: " + str(len(self._childs)))

	def event(self, evt):
		if isinstance(evt, CuMouseEvent):
			self._id, self._ix, self._iy, self._iz, self._bstate = evt.getmouse()

	def setIterator(self, it):
		self._iterator = it;

class CuMovableTestInput(CuTestInput):
	_state = None
	_px, _py = 0, 0
	_mx, _my = 0, 0

	def paint(self):
		CuTestInput.paint(self)
		self.getWin().addstr(2, 3, "[MOVABLE] " + str(self._state) + "    ")

	def event(self, evt):
		CuTestInput.event(self, evt)
		if isinstance(evt, CuMouseEvent):
			x, y = evt.globalPos()
			if evt.getState() == evt.MOUSE_CLICKED:
				self._state = "Clicked"
			elif evt.getState() == evt.MOUSE_PRESSED:
				self._state = "Pressed"
				self._px, self._py = self.getPos()
				self._mx, self._my = x, y
			elif evt.getState() == evt.MOUSE_RELEASED:
				self._state = None
			elif evt.getState() == evt.REPORT_MOUSE_POSITION:
				if self._state == "Pressed":
					newx = self._px+x-self._mx
					newy = self._py+y-self._my
					if newx < 0: newx=0
					if newy < 0: newy=0
					if newx+self._w > GLBL['maxX'] : newx=GLBL['maxX']-self._w
					if newy+self._h > GLBL['maxY'] : newy=GLBL['maxY']-self._h
					self.move(newx, newy);




def CuInit(screen):
	#screen = curses.initscr()
	#curses.noecho()
	curses.curs_set(0)
	screen.keypad(1)
	curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
	curses.mouseinterval(0)

	GLBL['maxY'], GLBL['maxX'] = screen.getmaxyx()
	#printf("\033[?1003h\n"); // Makes the terminal report mouse movement events
	#print('\033[?1000h')
	#print('\033[?1001h')
	#print('\033[?1002h')
	print('\033[?1003h')
	#print('\033[?1004h')
	#print('\033[?1005h')
	#print('\033[?1006h')
	#print('\033[?1015h')

def CuEnd():
	# Reset (disable) the terminal report mouse movement events
	#rint('\033[?1000l')
	#rint('\033[?1001l')
	#rint('\033[?1002l')
	print('\033[?1003l')
	#rint('\033[?1004l')
	#rint('\033[?1005l')
	#rint('\033[?1006l')
	#rint('\033[?1015l')



def main(screen):
	GLBL['screen'] = screen;
	CuInit(screen)
	logging.debug("GLBL: " +  str(GLBL))

	mw = CuMainWindow()
	mw.setBorder(True)

	layout = CuHLayout()

	tw1 = CuTestInput(parent=mw, name='tw1')
	tw1.setBorder(True)
	layout.addWidget(tw1)

	tw2 = CuTestInput(parent=mw, name='tw2')
	tw2.setBorder(True)
	layout.addWidget(tw2)

	vlayout = CuVLayout()
	p1 = CuPanel(parent=mw, name='p1')
	p1.setBorder(True)
	layout.addWidget(p1)

	tw4 = CuTestInput(parent=mw, name='tw4')
	tw4.setBorder(True)
	layout.addWidget(tw4)

	tw3 = CuTestInput(parent=p1, name='tw3')
	tw3.setBorder(True)
	vlayout.addWidget(tw3)

	mtw1 = CuMovableTestInput(parent=p1, name='mtw1')
	mtw1.setBorder(True)
	vlayout.addWidget(mtw1)

	mw.setLayout(layout)
	p1.setLayout(vlayout)
	mw.show()


	it = 0
	event = 0
	#curses.ungetch(0)
	#curses.ungetmouse(0, 0, 0, 0, curses.REPORT_MOUSE_POSITION)

	while True:
		mw.paint()

		curses.panel.update_panels()
		screen.refresh()

		event = screen.getch()

		# This is just for debugging purposes
		it += 1
		tw1.setIterator(it)
		tw2.setIterator(it)
		tw3.setIterator(it)
		# mtv1.setIterator(it)

		if event == curses.ERR: break
		if event == ord("q"): break

		evt = None

		if event == curses.KEY_MOUSE:
			evt = CuMouseEvent()
		if event == curses.KEY_RESIZE:
			GLBL['maxY'], GLBL['maxX'] = screen.getmaxyx()
			logging.debug("RESIZE: " +  str(GLBL))
			mw.setGeometry(0,0,GLBL['maxX'], GLBL['maxY'])
			mw.paint()

		mw.event(evt)

logging.basicConfig(filename='session.log',level=logging.DEBUG)

try:
	curses.wrapper(main)
finally:
	CuEnd()
