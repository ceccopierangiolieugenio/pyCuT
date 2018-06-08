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
		numWidgets = len(self._widgets)
		x, y, w, h = self.geometry()
		newx = x
		for widget in self._widgets:
			widget.resize(int(math.floor(w/numWidgets)),h)
			widget.move(newx,y)
			newx += int(math.floor(w/numWidgets))


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

	def __init__(self, parent=None, x=0, y=0, w=-1, h=-1):
		self._parent = parent
		self._x = x
		self._y = y
		if w == -1: self._w = GLBL['maxX']
		else:       self._w = w
		if h == -1: self._h = GLBL['maxY']
		else:       self._h = h
		self._childs = []
		self._win = curses.newwin(self._h, self._w, self._y, self._x)
		self._panel = curses.panel.new_panel(self._win)
		#self.panel.move(0, 0)

	def getPos(self):
		return self._x, self._y

	def move(self, x, y):
		self._x = x
		self._y = y
		# self._win.clear()
		# logging.debug(__name__ + "x:" + str(self._x) + " y:" + str(self._y))
		self._panel.move(self._y, self._x)

	def setBorder(self, bool):
		self._border = bool
		if bool:
			self._win.box()
		else:
			self._win.clear()

	def resize(self, w, h):
		self._w = w
		self._h = h
		self._win.clear()
		self._win.resize(h,w)
		if self._layout is not None:
			self._layout.setGeometry(self._x+1, self._y+1, self._w-2, self._h-2)
			self._layout.update()
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

	def show(self):
		pass




class CuMainWindow(CuWidget):
	def __init__(self, parent=None, x=0, y=0, w=-1, h=-1):
		CuWidget.__init__(self, parent=parent, x=x, y=y, w=w, h=h)





class CuTestInput(CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0
	_iterator = 0

	def __init__(self, parent=None, x=0, y=0, w=0, h=0):
		CuWidget.__init__(self, parent=parent, x=x, y=y, w=w, h=h)

	def paint(self):
		CuWidget.paint(self)
		# self.getWin().clear()
		self.getWin().addstr(3, 3, "CuTestInput... it: " + str(self._iterator))
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
					self.move(self._px+x-self._mx, self._py+y-self._my);




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

	mw = CuMainWindow()
	mw.setBorder(True)

	layout = CuHLayout()

	tw1 = CuTestInput(parent=mw, x=50, y=5, w=30, h=12)
	tw1.setBorder(True)
	layout.addWidget(tw1)

	tw2 = CuTestInput(parent=mw, x=30, y=20, w=30, h=12)
	tw2.setBorder(True)
	layout.addWidget(tw2)

	# mtw1 = CuMovableTestInput(parent=mw, x=20, y=15, w=30, h=12)
	# mtw1.setBorder(True)
	# layout.addWidget(mtw1)

	mw.setLayout(layout)
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

		if event == curses.ERR: break
		if event == ord("q"): break

		evt = None

		if event == curses.KEY_MOUSE:
			evt = CuMouseEvent()
		if event == curses.KEY_RESIZE:
			GLBL['maxY'], GLBL['maxX'] = screen.getmaxyx()
			mw.resize(GLBL['maxX'], GLBL['maxY'])

		mw.event(evt)

logging.basicConfig(filename='session.log',level=logging.DEBUG)

try:
	curses.wrapper(main)
finally:
	CuEnd()
