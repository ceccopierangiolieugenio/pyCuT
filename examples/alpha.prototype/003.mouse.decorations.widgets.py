'''
https://stackoverflow.com/questions/9254664/python-curses-getmouse?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
'''
import curses, curses.panel

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





class CuWidget:
	_win = None
	_panel = None
	_childs = None

	def __init__(self, parent=None, x=0, y=0, w=0, h=0):
		self._parent = parent
		self._x = x
		self._y = y
		self._childs = []
		if w == 0: self._w = GLBL['maxX']
		else:      self._w = w
		if h == 0: self._h = GLBL['maxY']
		else:      self._h = h
		self._win = curses.newwin(self._h, self._w, self._y, self._x)
		self._panel = curses.panel.new_panel(self._win)
		#self.panel.move(0, 0)

	def addChild(self, child):
		self._childs.append(child)

	def childAt(self, x, y):
		pass

	def getPos(self):
		return self._x, self._y

	def move(self, x, y):
		self._x = x
		self._y = y
		#self._win.clear()
		self._panel.move(self._y, self._x)

	def drawBorder(self):
		self._win.box()

	def resize(self, w, h):
		self._w = w
		self._h = h
		self._win.resize(h,w)
		self._win.clear()

	def getWin(self):
		return self._win

	def paint(self):
		for child in self._childs:
			child.paint()

	def event(self, evt):
		for child in self._childs:
			child.event(evt)






class CuMainWindow(CuWidget):
	def __init__(self, parent=None, x=0, y=0, w=0, h=0):
		CuWidget.__init__(self, parent=parent, x=x, y=y, w=w, h=h)





class CuTestInput(CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0

	def __init__(self, parent=None, x=0, y=0, w=0, h=0):
		CuWidget.__init__(self, parent=parent, x=x, y=y, w=w, h=h)

	def paint(self):		
		CuWidget.paint(self)
		# self.getWin().clear()
		self.getWin().addstr(3, 3, "CuTestInput...")
		self.getWin().addstr(4, 3, "    id: " + str(self._id))
		self.getWin().addstr(5, 3, "     x: " + str(self._ix))
		self.getWin().addstr(6, 3, "     y: " + str(self._iy))
		self.getWin().addstr(7, 3, "     z: " + str(self._iz))
		self.getWin().addstr(8, 3, "bstate: " + str(self._bstate) + "        ")
		self.getWin().addstr(9, 3, "childs: " + str(len(self._childs)))

	def event(self, evt):
		if isinstance(evt, CuMouseEvent):
			self._id, self._ix, self._iy, self._iz, self._bstate = evt.getmouse()



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

	screen.addstr(3,3,"This is a Sample Curses Script\n\n")
	GLBL['maxY'], GLBL['maxX'] = screen.getmaxyx()
	# printf("\033[?1003h\n"); // Makes the terminal report mouse movement events
	print('\033[?1003h')

def main(screen):
	GLBL['screen'] = screen;
	CuInit(screen)

	mw = CuMainWindow(None)
	mw.drawBorder()

	tw1 = CuTestInput(parent=mw, x=50, y=5, w=30, h=12)
	tw1.drawBorder()
	mw.addChild(tw1)

	tw2 = CuTestInput(parent=mw, x=30, y=20, w=30, h=12)
	tw2.drawBorder()
	mw.addChild(tw2)

	mtw1 = CuMovableTestInput(parent=mw, x=20, y=15, w=30, h=12)
	mtw1.drawBorder()
	mw.addChild(mtw1)


	it = 1
	event = 0

	while True:
		mw.getWin().addstr(8, 10, "Iteration:" + str(it))
		it += 1
		mw.getWin().addstr(9, 10, "Event:" + str(event))

		mw.paint()

		curses.panel.update_panels()
		screen.refresh()

		event = screen.getch()

		if event == curses.ERR: break
		if event == ord("q"): break

		evt = None

		if event == curses.KEY_MOUSE:
			# _, mx, my, _, _ = curses.getmouse()
			# y, x = screen.getyx()
			evt = CuMouseEvent()
			mw.getWin().addstr(10, 10, "pippo")
			mw.getWin().addstr(11, 10, str(evt.getmouse()))
		if event == curses.KEY_RESIZE:
			GLBL['maxY'], GLBL['maxX'] = screen.getmaxyx()
			mw.resize(GLBL['maxX'], GLBL['maxY'])
			mw.drawBorder()
			mw.getWin().addstr(13, 10, "---RESIZE---")

		mw.event(evt)

try:
	curses.wrapper(main)
finally:
	# Reset (disable) the terminal report mouse movement events
	print('\033[?1003l')