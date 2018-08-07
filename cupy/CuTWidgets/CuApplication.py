'''
    Application
'''

import curses, curses.panel
import logging

from CuT.CuTCore import  CuT
from CuT.CuTCore import CuEvent, CuMouseEvent, CuWheelEvent
from CuT.CuTHelper import CuWrapper, CuHelper

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
		logging.debug("SCREEN: W:"+str(CuApplication.GLBL['maxX'])+" H:"+str(CuApplication.GLBL['maxY']))


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
		CuHelper.execPaint(CuApplication.getW(),CuApplication.getH())
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
		else: maxh = CuApplication.GLBL['maxY']

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

			try:
				event = CuApplication.GLBL['screen'].getch()
			except KeyboardInterrupt as e:
				# print "getch: " + str(e)
				logging.debug(__name__ + " KI getch: " + str(e))
				event = curses.ERR
				continue
			except Exception as e:
				# print "getch: " + str(e)
				logging.debug(__name__ + " Exc getch: " + str(e))
				event = curses.ERR
				continue

			logging.debug(__name__ + "  event: " + hex(event))

			if event == -1: continue

			if event == curses.ERR: break

			if event == curses.KEY_MOUSE:
				mouse_evt = None
				# Mouse event
				idm, x, y, z, bstate = curses.getmouse()
				btype   = CuT.NoButton
				button = None
				# logging.debug(__name__ + "  mouse evt: " + str((idm, x, y, z, bstate)))
				# logging.debug(__name__ + "  mouse evt: " + str(curses.BUTTON1_PRESSED))

				if bstate == curses.REPORT_MOUSE_POSITION:
						button = CuEvent.MouseMove
						btype = CuT.NoButton

				elif bstate == curses.BUTTON1_PRESSED:
						button = CuEvent.MouseButtonPress
						btype = CuT.LeftButton
				elif bstate == curses.BUTTON1_RELEASED:
						button = CuEvent.MouseButtonRelease
						btype = CuT.LeftButton
				elif bstate == curses.BUTTON1_CLICKED:
						button = CuEvent.MouseButtonPress
						btype = CuT.LeftButton

				elif bstate == curses.BUTTON2_PRESSED:
						button = CuEvent.MouseButtonPress
						btype = CuT.RightButton
				elif bstate == curses.BUTTON2_RELEASED:
						button = CuEvent.MouseButtonRelease
						btype = CuT.RightButton
				elif bstate == curses.BUTTON2_CLICKED:
						button = CuEvent.MouseButtonPress
						btype = CuT.RightButton

				elif bstate == curses.BUTTON3_PRESSED:
						button = CuEvent.MouseButtonPress
						btype = CuT.MidButton
				elif bstate == curses.BUTTON3_RELEASED:
						button = CuEvent.MouseButtonRelease
						btype = CuT.MidButton
				elif bstate == curses.BUTTON3_CLICKED:
						button = CuEvent.MouseButtonPress
						btype = CuT.MidButton

				elif bstate == 0x010000: # Mouse Wheel UP
						angleDelta = 120
						btype = CuT.ForwardButton
				elif bstate == 0x200000: # Mouse Wheel DOWN
						angleDelta = -120
						btype = CuT.ForwardButton

				# if bstate == curses.BUTTON1_DOUBLE_CLICKED: event =  CuEvent.MouseButtonDblClick
				# if bstate == curses.BUTTON1_TRIPLE_CLICKED: event =  CuEvent.MouseButtonPress

				mwx, mwy = CuApplication.GLBL['mainWidget'].pos()
				if btype == CuT.ForwardButton:
					mouse_evt = CuWheelEvent(
						type=btype,
						pos  = {'x':x-mwx, 'y':y-mwy},
						globalPos = {'x':x,     'y':y},
						angleDelta=angleDelta)
				else:
					mouse_evt = CuMouseEvent(
						type=btype,
						localPos  = {'x':x-mwx, 'y':y-mwy},
						windowPos = {'x':x-mwx, 'y':y-mwy},
						screenPos = {'x':x,     'y':y},
						button=button)

				CuApplication.GLBL['mainWidget'].event(mouse_evt)

			elif event == curses.KEY_RESIZE:
				CuApplication.refreshMain()

			else:
				# key pressed
				logging.debug(__name__ + "  Pressed key " + str(event)) #, "("+keyname(event)+")")
				if event == ord("q"): break




		return 0
