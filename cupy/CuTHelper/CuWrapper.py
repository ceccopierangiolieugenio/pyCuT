# -*- coding: utf-8 -*-

import curses, curses.panel
import locale

from CuT import CuTCore
from CuT.CuTCore import  CuT, CuPoint, cuDebug

#from .urwid.util import (MetaSuper, decompose_tagmarkup, calc_width,
#    is_wide_char, move_prev_char, move_next_char)


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
		self._bufPaint = {'move':None, 'resize':None, 'erase':[], 'string':[], 'box':False}

	def box(self):
		self._bufPaint['box']=True

	def move(self, x, y):
		npos = CuHelper.absParentPos(self._widget)
		# CuTCore.cuDebug("Move: x:"+str(nx+x)+" y:"+str(ny+y))
		self._bufPaint['move']={'x':npos.x()+x, 'y':npos.y()+y}
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

	def setWinColor(self, fg, bg):
		self._win.bkgd(' ',curses.color_pair(CuWrapper.colorIdx(fg, bg)))

	def drawString(self, x, y, strg, fg, bg):
		self._bufPaint['string'].append({'x':x, 'y':y, 'str':strg, 'fg':fg, 'bg':bg})
		CuHelper.addPaintBuffer(self)

	def eraseRect(self, x, y, w, h):
		self._bufPaint['erase'].append({'x':x, 'y':y, 'w':w, 'h':h})
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

		for es in self._bufPaint['erase']:
			for y in range(es['h']):
				for x in range(es['w']):
					self._win.delch(y+es['y'], x+es['x'])

		for ds in self._bufPaint['string']:
			x = ds['x']
			y = ds['y']
			strg = ds['str']
			fg = ds['fg']
			bg = ds['bg']
			fgc = CuWrapper.WR_COL_WHITE
			bgc = CuWrapper.WR_COL_BLACK
			mod = 0
			c = curses.color_pair(0)
			c = curses.color_pair(CuWrapper.colorIdx(fgc, bgc))
			if   fg == CuT.color0:    pass
			elif fg == CuT.color1:    pass
			elif fg == CuT.black:     pass
			elif fg == CuT.white:     pass
			elif fg == CuT.darkGray:    fgc = CuWrapper.WR_COL_BLACK   ; mod |= curses.A_BOLD
			elif fg == CuT.gray:        fgc = CuWrapper.WR_COL_BLACK   ; mod |= curses.A_BOLD
			elif fg == CuT.lightGray:   fgc = CuWrapper.WR_COL_BLACK   ; mod |= curses.A_BOLD
			elif fg == CuT.red:         fgc = CuWrapper.WR_COL_RED
			elif fg == CuT.green:       fgc = CuWrapper.WR_COL_GREEN
			elif fg == CuT.blue:        fgc = CuWrapper.WR_COL_BLUE
			elif fg == CuT.cyan:        fgc = CuWrapper.WR_COL_CYAN
			elif fg == CuT.magenta:     fgc = CuWrapper.WR_COL_MAGENTA
			elif fg == CuT.yellow:      fgc = CuWrapper.WR_COL_YELLOW
			elif fg == CuT.darkRed:     fgc = CuWrapper.WR_COL_RED     ; mod |= curses.A_DIM
			elif fg == CuT.darkGreen:   fgc = CuWrapper.WR_COL_GREEN   ; mod |= curses.A_DIM
			elif fg == CuT.darkBlue:    fgc = CuWrapper.WR_COL_BLUE    ; mod |= curses.A_DIM
			elif fg == CuT.darkCyan:    fgc = CuWrapper.WR_COL_CYAN    ; mod |= curses.A_DIM
			elif fg == CuT.darkMagenta: fgc = CuWrapper.WR_COL_MAGENTA ; mod |= curses.A_DIM
			elif fg == CuT.darkYellow:  fgc = CuWrapper.WR_COL_YELLOW  ; mod |= curses.A_DIM
			elif fg == CuT.transparent: pass

			if   bg == CuT.color0:    pass
			elif bg == CuT.color1:    pass
			elif bg == CuT.black:     pass
			elif bg == CuT.white:     pass
			elif bg == CuT.darkGray:    bgc = fgc ; fgc = CuWrapper.WR_COL_BLACK ; mod |= curses.A_BOLD | curses.A_REVERSE
			elif bg == CuT.gray:        bgc = fgc ; fgc = CuWrapper.WR_COL_BLACK ; mod |= curses.A_BOLD | curses.A_REVERSE
			elif bg == CuT.lightGray:   bgc = fgc ; fgc = CuWrapper.WR_COL_BLACK ; mod |= curses.A_BOLD | curses.A_REVERSE
			elif bg == CuT.red:         bgc = CuWrapper.WR_COL_RED
			elif bg == CuT.green:       bgc = CuWrapper.WR_COL_GREEN
			elif bg == CuT.blue:        bgc = CuWrapper.WR_COL_BLUE
			elif bg == CuT.cyan:        bgc = CuWrapper.WR_COL_CYAN
			elif bg == CuT.magenta:     bgc = CuWrapper.WR_COL_MAGENTA
			elif bg == CuT.yellow:      bgc = CuWrapper.WR_COL_YELLOW
			elif bg == CuT.darkRed:     bgc = CuWrapper.WR_COL_RED
			elif bg == CuT.darkGreen:   bgc = CuWrapper.WR_COL_GREEN
			elif bg == CuT.darkBlue:    bgc = CuWrapper.WR_COL_BLUE
			elif bg == CuT.darkCyan:    bgc = CuWrapper.WR_COL_CYAN
			elif bg == CuT.darkMagenta: bgc = CuWrapper.WR_COL_MAGENTA
			elif bg == CuT.darkYellow:  bgc = CuWrapper.WR_COL_YELLOW
			elif bg == CuT.transparent: pass

			c = curses.color_pair(CuWrapper.colorIdx(fgc, bgc)) | mod

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

	class CursorType(int): pass
	disabledCursor = 0
	insertCursor   = 1
	replaceCursor  = 2
	@staticmethod
	def enableCursor(t=insertCursor):
		try:
			curses.curs_set(t)
		except Exception as e:
			curses.curs_set(CuHelper.insertCursor)

	@staticmethod
	def disableCursor():
		curses.curs_set(False)

	@staticmethod
	def moveCursor(x=0, y=0, widget=None):
		if widget is not None:
			npos = CuHelper.absPos(widget)
			x += npos.x()
			y += npos.y()
		CuHelper.GLBL['screen'].move(y,x)

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
	def setWidgetColor(widget, fg, bg):
		widget._data['win'].setWinColor(fg, bg)

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
		pos = CuHelper.absParentPos(widget)
		return widget.pos() + pos

	@staticmethod
	def absParentPos(widget):
		if widget.parentWidget() is None:
			return CuPoint()
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
		locale.setlocale(locale.LC_ALL,"")
		# curses.curs_set(False)
		# curses.curs_set(1)
		CuHelper.disableCursor()
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

	# WR_COL_DEFAULT  = 0
	WR_COL_BLACK    = 0
	WR_COL_RED      = 1
	WR_COL_GREEN    = 2
	WR_COL_YELLOW   = 3
	WR_COL_BLUE     = 4
	WR_COL_MAGENTA  = 5
	WR_COL_CYAN     = 6
	WR_COL_WHITE    = 7

	@staticmethod
	def colorIdx(fg, bg):
		return ( (fg) + (bg) * 8 ) + 1

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
				idx = CuWrapper.colorIdx(fg, bg)
				# cuDebug('idx:'+str(idx)+' fg:'+str(fg)+' bg:'+str(bg))
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
