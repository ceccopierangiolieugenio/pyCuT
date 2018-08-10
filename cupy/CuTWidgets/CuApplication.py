'''
    Application
'''

import curses, curses.panel
import logging

from CuT.CuTCore import  CuT
from CuT.CuTCore import CuEvent, CuMouseEvent, CuWheelEvent
from CuT.CuTHelper import CuWrapper, CuHelper

class CuApplication:
	def __init__(self, screen, argv):
		CuHelper.__CuInit__(screen)

	def exec_(self):
		event = 0
		CuHelper.refreshMain()
		CuHelper.paintAll()
		while True:
			if CuHelper.GLBL['mainWidget'].isVisible():
				# CuHelper.GLBL['mainWidget'].paintEvent(None)
				#CuHelper.GLBL['mainWidget'].update()
				CuHelper.paintAll()

			try:
				event = CuHelper.GLBL['screen'].getch()
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

			# logging.debug(__name__ + "  event: " + hex(event))

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

				mwx, mwy = CuHelper.GLBL['mainWidget'].pos()
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

				CuHelper.GLBL['mainWidget'].event(mouse_evt)

			elif event == curses.KEY_RESIZE:
				CuHelper.refreshMain()

			else:
				# key pressed
				logging.debug(__name__ + "  Pressed key " + str(event)) #, "("+keyname(event)+")")
				if event == ord("q"): break




		return 0
