'''
    Application
'''

import curses, curses.panel
import logging

from CuT.CuTCore import CuMouseEvent


class CuApplication:
	GLBL = {
		'maxY' : 0,
		'maxX' : 0,
		'screen' : None,
		'mainWidget' : None
	}

	def __init__(self, screen, argv):
		CuApplication.__CuInit__(screen)

	@staticmethod
	def __CuInit__(screen):
		logging.basicConfig(filename='session.log',level=logging.DEBUG)
		curses.curs_set(0)
		screen.keypad(1)
		curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
		curses.mouseinterval(0)
		CuApplication.GLBL['screen'] = screen
		CuApplication.GLBL['maxY'], CuApplication.GLBL['maxX'] = screen.getmaxyx()
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
	def setMainWidget(widget):
		CuApplication.GLBL['mainWidget'] = widget

	@staticmethod
	def getW():
		return CuApplication.GLBL['maxX']

	@staticmethod
	def getH():
		return CuApplication.GLBL['maxY']

	@staticmethod
	def getScreen():
		return CuApplication.GLBL['screen']

	@staticmethod
	def is_initialized():
		return CuApplication.GLBL['screen'] != None

	def exec_(self):
		event = 0
		while True:
			CuApplication.GLBL['mainWidget'].paint()

			curses.panel.update_panels()
			CuApplication.GLBL['screen'].refresh()

			event = CuApplication.GLBL['screen'].getch()

			if event == curses.ERR: break
			if event == ord("q"): break

			evt = None

			if event == curses.KEY_MOUSE:
				evt = CuMouseEvent()
			if event == curses.KEY_RESIZE:
				CuApplication.GLBL['maxY'], CuApplication.GLBL['maxX'] = CuApplication.GLBL['screen'].getmaxyx()
				CuApplication.GLBL['mainWidget'].setGeometry(0, 0, CuApplication.GLBL['maxX'], CuApplication.GLBL['maxY'])
				CuApplication.GLBL['mainWidget'].paint()

			CuApplication.GLBL['mainWidget'].event(evt)
		return 0
