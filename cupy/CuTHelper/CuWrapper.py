# -*- coding: utf-8 -*-

import curses, curses.panel

from CuT import CuTCore
from CuT.CuTCore import  CuT

class CuWin:
	__slots__ = ('_widget', '_win', '_panel', '_bufPaint')
	def __init__(self, widget, x, y, w, h):
		self._widget = widget
		self._win = curses.newwin(h, w, y, x)
		self._panel = curses.panel.new_panel(self._win)
		self.resetBufPaint()

	def zTop(self):
		self._panel.top()

	def resetBufPaint(self):
		self._bufPaint = {'move':None, 'resize':None, 'string':[], 'box':False}

	def box(self):
		self._bufPaint['box']=True

	def move(self, x, y):
		nx, ny = CuHelper.absParentPos(self._widget)
		# CuTCore.cuDebug("Move: x:"+str(nx+x)+" y:"+str(ny+y))
		self._bufPaint['move']={'x':nx+x, 'y':ny+y}
		CuHelper.addPaintBuffer(self)

	def clear(self):
		self._bufPaint['box']=False
		self.resetBufPaint()
		self._win.clear()

	def resize(self, w, h):
		# CuTCore.cuDebug("resize: w:"+str(w)+" h:"+str(h))
		self._bufPaint['resize']={'w':w, 'h':h}
		CuHelper.addPaintBuffer(self)

	def hide(self):
		self._panel.hide()

	def show(self):
		self._panel.show()

	def drawString(self, x, y, strg, fg, bg):
		self._bufPaint['string'].append({'x':x, 'y':y, 'str':strg, 'fg':fg, 'bg':bg})
		CuHelper.addPaintBuffer(self)

	def execPaint(self, winw, winh):
		# self._win.box()
		h,w = self._win.getmaxyx()
		if self._bufPaint['resize'] is not None:
			# Avoid the panel outside the terminal
			self._win.clear()
			if self._bufPaint['resize']['w'] > winw: w = winw
			else: w = self._bufPaint['resize']['w']
			if self._bufPaint['resize']['h'] > winh: h = winh
			else: h = self._bufPaint['resize']['h']
			# CuTCore.cuDebug('resize(h, w):' + str([h,w]) )
			if h > 0 and w > 0:
				self._win.resize(h, w)
			else:
				self._panel.hide()
				return

		if self._bufPaint['move'] is not None:
			# Avoid the panel outside the terminal
			if self._bufPaint['move']['x']+w > winw: x = winw-w-1
			else: x = self._bufPaint['move']['x']
			if self._bufPaint['move']['y']+h > winh: y = winh-h-1
			else: y = self._bufPaint['move']['y']
			# CuTCore.cuDebug('move(y, x):' + str([x,y]) )
			self._panel.move(y, x)

		if self._bufPaint['box']:
			# # self._win.box()
			# Rectangle drawing routine from:
			# /usr/lib/python2.7/curses/textpad.py
			uly, ulx = 0, 0
			lry, lrx = h-1, w-1
			self._win.vline(uly+1, ulx, curses.ACS_VLINE, lry - uly - 1)
			self._win.hline(uly, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
			self._win.hline(lry, ulx+1, curses.ACS_HLINE, lrx - ulx - 1)
			self._win.vline(uly+1, lrx, curses.ACS_VLINE, lry - uly - 1)
			self._win.addch(uly, ulx, curses.ACS_ULCORNER)
			self._win.addch(uly, lrx, curses.ACS_URCORNER)
			self._win.insch(lry, lrx, curses.ACS_LRCORNER)
			self._win.addch(lry, ulx, curses.ACS_LLCORNER)
			# CuTCore.cuDebug("boxch:" + u'わ'+ hex(curses.ACS_LLCORNER) )


		for ds in self._bufPaint['string']:
			x = ds['x']
			y = ds['y']
			strg = ds['str']
			fg = ds['fg']
			bg = ds['bg']
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
			strlen = len(strg)
			#ww, wh = self._widget.size()
			if (y<0) or (y>h-1) or (x>w-1) or (x+strlen<0):
				continue
			if (x+strlen>w):
				strg = strg[:(w-x)]
			if y == h-1 and (x+strlen)>=w :
				self._win.insstr(y, x, strg, c)
			else:
				self._win.addstr(y, x, strg, c)
		self.resetBufPaint()

class CuHelper:
	GLBL = {
		'maxY' : 0,
		'maxX' : 0,
		'screen' : None,
		'mainWidget' : None,
		'focusWidget' : None
	}

	@staticmethod
	def setFocus(widget):
		CuHelper.GLBL['focusWidget'] = widget

	@staticmethod
	def getFocus():
		return CuHelper.GLBL['focusWidget']

	@staticmethod
	def clearFocus():
		CuHelper.GLBL['focusWidget'] = None

	@staticmethod
	def setMainWidget(widget):
		CuHelper.GLBL['mainWidget'] = widget

	@staticmethod
	def getW():
		return CuHelper.GLBL['maxX']

	@staticmethod
	def getH():
		return CuHelper.GLBL['maxY']

	_updateWidget = []
	@staticmethod
	def addUpdateWidget(widget):
		if widget not in CuHelper._updateWidget:
			CuHelper._updateWidget.append(widget)

	@staticmethod
	def absPos(widget):
		px, py = CuHelper.absParentPos(widget)
		return widget.x()+px, widget.y()+py

	@staticmethod
	def absParentPos(widget):
		if widget.parentWidget() is None:
			return 0, 0
		return CuHelper.absPos(widget.parentWidget())

	_paintBuffer = []
	@staticmethod
	def addPaintBuffer(win):
		if win not in CuHelper._paintBuffer:
			CuHelper._paintBuffer.append(win)

	@staticmethod
	def execPaint(winw, winh):
		#CuHelper.GLBL['mainWidget'].paintEvent(None)
		for win in CuHelper._paintBuffer:
			win.execPaint(winw, winh)
		CuHelper._paintBuffer = []

	@staticmethod
	def __CuInit__(screen):
		curses.curs_set(False)
		# curses.curs_set(1)
		screen.keypad(1)
		curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
		curses.mouseinterval(0)
		CuHelper.GLBL['screen'] = screen
		CuHelper.GLBL['maxY'], CuHelper.GLBL['maxX'] = screen.getmaxyx()
		CuTCore.cuDebug("SCREEN: W:"+str(CuHelper.GLBL['maxX'])+" H:"+str(CuHelper.GLBL['maxY']))

		CuWrapper.initWrapper()
		CuWrapper.__CuInit__()

	@staticmethod
	def getScreen():
		return CuHelper.GLBL['screen']

	@staticmethod
	def app_initialized():
		return CuHelper.GLBL['screen'] != None

	@staticmethod
	def paintAll():
		#CuHelper.GLBL['mainWidget'].paintEvent(None)
		for widget in CuHelper._updateWidget:
			widget.paintEvent(None)
		CuHelper._updateWidget = []
		CuHelper.execPaint(CuHelper.getW(),CuHelper.getH())
		curses.panel.update_panels()
		CuHelper.GLBL['screen'].refresh()

	@staticmethod
	def refreshMain():
		x, y = 0, 0
		CuHelper.GLBL['maxY'], CuHelper.GLBL['maxX'] = CuHelper.GLBL['screen'].getmaxyx()
		maxw, maxh = CuHelper.GLBL['mainWidget'].maximumSize()
		minw, minh = CuHelper.GLBL['mainWidget'].minimumSize()

		#CuTCore.cuDebug("  screen: " + str((CuHelper.GLBL['maxX'], CuHelper.GLBL['maxY'])))
		#CuTCore.cuDebug("  min:    " + str(CuHelper.GLBL['mainWidget'].minimumSize()))
		#CuTCore.cuDebug("  max:    " + str(CuHelper.GLBL['mainWidget'].maximumSize()))

		if ( CuHelper.GLBL['maxX'] < minw ) or ( CuHelper.GLBL['maxY'] < minh ):
			CuTCore.cuDebug("HIDE!!!")
			CuHelper.GLBL['mainWidget'].hide()
			CuHelper.GLBL['screen'].addstr(1, 1, "The Terminal Size")
			CuHelper.GLBL['screen'].addstr(2, 1, "is too small...")
			return
		if not CuHelper.GLBL['mainWidget'].isVisible():
			CuTCore.cuDebug("SHOW!!!")
			CuHelper.GLBL['screen'].clear()

		if CuHelper.GLBL['maxX'] > maxw : x = (CuHelper.GLBL['maxX']-maxw )//2
		else: maxw = CuHelper.GLBL['maxX']

		if CuHelper.GLBL['maxY'] > maxh : y = (CuHelper.GLBL['maxY']-maxh )//2
		else: maxh = CuHelper.GLBL['maxY']

		CuHelper.GLBL['mainWidget'].setGeometry(x, y, maxw, maxh)
		CuHelper.GLBL['mainWidget'].show()

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
	def newWin(widget, x, y, w, h):
		return CuWin(widget, x, y, w, h)

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
