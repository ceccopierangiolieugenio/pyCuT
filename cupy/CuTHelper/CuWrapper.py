

import curses, curses.panel

from CuT.CuTCore import  CuT


class CuWin:
	def __init__(self, x, y, w, h):
		self._win = curses.newwin(h, w, y, x)
		self._panel = curses.panel.new_panel(self._win)

	def box(self):
		self._win.box()

	def move(self, x, y):
		self._panel.move(y, x)

	def clear(self):
		self._win.clear()

	def resize(self, w, h):
		self._win.resize(h, w)

	def hide(self):
		self._panel.hide()

	def show(self):
		self._panel.show()

	def addstr(self, x, y, str):
		self._win.addstr(y, x, str)

	def drawString(self, x, y, str, fg, bg):
		c = curses.color_pair(0)
		if   fg == CuT.color0:    pass
		elif fg == CuT.color1:    pass
		elif fg == CuT.black:     pass
		elif fg == CuT.white:       c = curses.color_pair(0)
		elif fg == CuT.darkGray:    c = curses.color_pair(1 + curses.COLOR_BLACK   + curses.COLOR_BLACK * 8) | curses.A_BOLD 
		elif fg == CuT.gray:        c = curses.color_pair(1 + curses.COLOR_BLACK   + curses.COLOR_BLACK * 8) | curses.A_BOLD
		elif fg == CuT.lightGray:   c = curses.color_pair(1 + curses.COLOR_BLACK   + curses.COLOR_BLACK * 8) | curses.A_BOLD
		elif fg == CuT.red:         c = curses.color_pair(1 + curses.COLOR_RED     + curses.COLOR_BLACK * 8)
		elif fg == CuT.green:       c = curses.color_pair(1 + curses.COLOR_GREEN   + curses.COLOR_BLACK * 8)
		elif fg == CuT.blue:        c = curses.color_pair(1 + curses.COLOR_BLUE    + curses.COLOR_BLACK * 8)
		elif fg == CuT.cyan:        c = curses.color_pair(1 + curses.COLOR_CYAN    + curses.COLOR_BLACK * 8)
		elif fg == CuT.magenta:     c = curses.color_pair(1 + curses.COLOR_MAGENTA + curses.COLOR_BLACK * 8)
		elif fg == CuT.yellow:      c = curses.color_pair(1 + curses.COLOR_YELLOW  + curses.COLOR_BLACK * 8)
		elif fg == CuT.darkRed:     c = curses.color_pair(1 + curses.COLOR_RED     + curses.COLOR_BLACK * 8) | curses.A_DIM
		elif fg == CuT.darkGreen:   c = curses.color_pair(1 + curses.COLOR_GREEN   + curses.COLOR_BLACK * 8) | curses.A_DIM
		elif fg == CuT.darkBlue:    c = curses.color_pair(1 + curses.COLOR_BLUE    + curses.COLOR_BLACK * 8) | curses.A_DIM
		elif fg == CuT.darkCyan:    c = curses.color_pair(1 + curses.COLOR_CYAN    + curses.COLOR_BLACK * 8) | curses.A_DIM
		elif fg == CuT.darkMagenta: c = curses.color_pair(1 + curses.COLOR_MAGENTA + curses.COLOR_BLACK * 8) | curses.A_DIM
		elif fg == CuT.darkYellow:  c = curses.color_pair(1 + curses.COLOR_YELLOW  + curses.COLOR_BLACK * 8) | curses.A_DIM
		elif fg == CuT.transparent: pass
		''' Corner case:
			if the last character of the string goes in the end
			of the window (lower right edge), the cursor goes "off screen"
			and NCurses return an error
		'''
		h,w = self._win.getmaxyx()
		strlen = len(str)
		if y == h-1:
			self._win.addnstr(y, x, str[:strlen-2], strlen,c)
			self._win.addch(y,x+strlen-2,str[strlen-1],c)
			self._win.insch(y,x+strlen-2,str[strlen-2],c)
		else:
			self._win.addstr(y, x, str, c)


class CuWrapper:
	@staticmethod
	def init(func):
		try:
			curses.wrapper(func)
		finally:
			CuWrapper.__CuEnd__()

	@staticmethod
	def __CuInit__():
		''' Init terminal '''
		#printf("\033[?1003h\n"); // Makes the terminal report mouse movement events
		#print('\033[?1000h')
		#print('\033[?1001h')
		#print('\033[?1002h')
		print('\033[?1003h')
		#print('\033[?1004h')
		#print('\033[?1005h')
		#print('\033[?1006h')
		#print('\033[?1015h')


	@staticmethod
	def __CuEnd__():
		# Reset (disable) the terminal report mouse movement events
		#rint('\033[?1000l')
		#rint('\033[?1001l')
		#rint('\033[?1002l')
		print('\033[?1003l')
		#rint('\033[?1004l')
		#rint('\033[?1005l')
		#rint('\033[?1006l')
		#rint('\033[?1015l')

	@staticmethod
	def newWin(x, y, w, h):
		return CuWin(x, y, w, h)

	@staticmethod
	def initWrapper():
		''' Init Colors 
			/* colors */
			#define COLOR_BLACK     0
			#define COLOR_RED       1
			#define COLOR_GREEN     2
			#define COLOR_YELLOW    3
			#define COLOR_BLUE      4
			#define COLOR_MAGENTA   5
			#define COLOR_CYAN      6
			#define COLOR_WHITE     7
		'''
		curses.start_color()
		for bg in range(8):
			for fg in range(8):
				idx = ( fg + bg * 8 ) + 1
				curses.init_pair(idx, fg, bg)

		# CuT.color0 = 1 # type: 'Qt.GlobalColor'
		# CuT.color1 = 2
		# CuT.black = 3
		# CuT.white = 4
		# CuT.darkGray = 5
		# CuT.gray = 6
		# CuT.lightGray = 7
		# CuT.red = 8
		# CuT.green = 9
		# CuT.blue = 10
		# CuT.cyan = 11
		# CuT.magenta = 12
		# CuT.yellow = 13
		# CuT.darkRed = 14
		# CuT.darkGreen = 15
		# CuT.darkBlue = 16
		# CuT.darkCyan = 17
		# CuT.darkMagenta = 18
		# CuT.darkYellow = 19
		# CuT.transparent = 20
