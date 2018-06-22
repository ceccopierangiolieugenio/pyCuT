'''
    Application
'''

import curses, curses.panel
import logging

from CuT.CuTCore import CuMouseEvent
from CuT.CuTHelper import CuWrapper

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

		CuWrapper.initWrapper()
		CuWrapper.__CuInit__()

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


	_updateWidget = []
	@staticmethod
	def addUpdateWidget(widget):
		if widget not in CuApplication._updateWidget:
			CuApplication._updateWidget.append(widget)

	@staticmethod
	def paintAll():
		#CuApplication.GLBL['mainWidget'].paintEvent(None)
		for widget in CuApplication._updateWidget:
			widget.paintEvent(None)
		CuApplication._updateWidget = []
		curses.panel.update_panels()
		CuApplication.GLBL['screen'].refresh()

	@staticmethod
	def refreshMain():
		x, y = 0, 0
		CuApplication.GLBL['maxY'], CuApplication.GLBL['maxX'] = CuApplication.GLBL['screen'].getmaxyx()
		maxw, maxh = CuApplication.GLBL['mainWidget'].maximumSize()
		minw, minh = CuApplication.GLBL['mainWidget'].minimumSize()

		#logging.debug(__name__ + "  screen: " + str((CuApplication.GLBL['maxX'], CuApplication.GLBL['maxY'])))
		#logging.debug(__name__ + "  min:    " + str(CuApplication.GLBL['mainWidget'].minimumSize()))
		#logging.debug(__name__ + "  max:    " + str(CuApplication.GLBL['mainWidget'].maximumSize()))

		if ( CuApplication.GLBL['maxX'] < minw ) or ( CuApplication.GLBL['maxY'] < minh ):
			logging.debug(__name__ + "HIDE!!!")
			CuApplication.GLBL['mainWidget'].hide()
			CuApplication.GLBL['screen'].addstr(1, 1, "The Terminal Size")
			CuApplication.GLBL['screen'].addstr(2, 1, "is too small...")
			return
		if not CuApplication.GLBL['mainWidget'].isVisible():
			logging.debug(__name__ + "SHOW!!!")
			CuApplication.GLBL['screen'].clear()

		if CuApplication.GLBL['maxX'] > maxw : x = (CuApplication.GLBL['maxX']-maxw )//2
		else: maxw = CuApplication.GLBL['maxX']

		if CuApplication.GLBL['maxY'] > maxh : y = (CuApplication.GLBL['maxY']-maxh )//2
		else: maxh = CuApplication.GLBL['maxX']

		CuApplication.GLBL['mainWidget'].setGeometry(x, y, maxw, maxh)
		CuApplication.GLBL['mainWidget'].show()

	def exec_(self):
		event = 0
		CuApplication.refreshMain()
		CuApplication.paintAll()
		while True:
			if CuApplication.GLBL['mainWidget'].isVisible():
				# CuApplication.GLBL['mainWidget'].paintEvent(None)
				#CuApplication.GLBL['mainWidget'].update()
				CuApplication.paintAll()

			event = CuApplication.GLBL['screen'].getch()

			if event == curses.ERR: break
			if event == ord("q"): break

			evt = None

			if event == curses.KEY_MOUSE:
				evt = CuMouseEvent()

			if event == curses.KEY_RESIZE:
				CuApplication.refreshMain()

			CuApplication.GLBL['mainWidget'].event(evt)
		return 0
