'''
https://stackoverflow.com/questions/9254664/python-curses-getmouse?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
'''
import curses, curses.panel

GLBL = {
	'maxY' : 0,
	'maxX' : 0,
	'screen' : None
	}

class CuWidget:
	win = None
	panel = None

	def __init__(self, parent=None, x=0, y=0, w=0, h=0):
		self.parent = parent
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.win = curses.newwin(GLBL['maxY'], GLBL['maxX'], 0, 0)
		self.panel = curses.panel.new_panel(self.win)
		self.panel.move(0, 0)

	def drawBorder(self):
		self.win.box()

	def resize(self, w, h):
		self.w = w
		self.h = h
		self.win.resize(h,w)
		self.win.clear()

	def getWin(self):
		return self.win

class CuMainWindow(CuWidget):
	def __init__(self,parent):
		CuWidget.__init__(self,parent=parent)


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

	it = 1
	event = 0

	while True:
		mw.getWin().addstr(8, 10, "Iteration:" + str(it))
		it += 1
		mw.getWin().addstr(9, 10, "Event:" + str(event))

		curses.panel.update_panels()
		screen.refresh()

		event = screen.getch()

		if event == curses.ERR: break
		if event == ord("q"): break 
		if event == curses.KEY_MOUSE:
			# _, mx, my, _, _ = curses.getmouse()
			# y, x = screen.getyx()
			mw.getWin().addstr(10, 10, "pippo")
			mw.getWin().addstr(11, 10, str(curses.getmouse()) + "                      ")
		if event == curses.KEY_RESIZE:
			GLBL['maxY'], GLBL['maxX'] = screen.getmaxyx()
			mw.resize(GLBL['maxX'], GLBL['maxY'])
			mw.drawBorder()
			mw.getWin().addstr(13, 10, "---RESIZE---")

try:
	curses.wrapper(main)
finally:
	# Reset (disable) the terminal report mouse movement events
	print('\033[?1003l')