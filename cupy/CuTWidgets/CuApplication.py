'''
    Application
'''

import curses, curses.panel

from CuT import CuTCore
from CuT.CuTCore import  CuT
from CuT.CuTCore import CuEvent, CuMouseEvent, CuWheelEvent, CuKeyEvent
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
				CuTCore.cuDebug(" KI getch: " + str(e))
				event = curses.ERR
				continue
			except Exception as e:
				# print "getch: " + str(e)
				CuTCore.cuDebug(" Exc getch: " + str(e))
				event = curses.ERR
				continue

			# CuTCore.cuDebug("  event: " + hex(event))

			if event == -1: continue

			if event == curses.ERR: break

			if event == curses.KEY_MOUSE:
				mouse_evt = None
				# Mouse event
				idm, x, y, z, bstate = curses.getmouse()
				btype   = CuT.NoButton
				button = None
				# CuTCore.cuDebug("  mouse evt: " + str((idm, x, y, z, bstate)))
				# CuTCore.cuDebug("  mouse evt: " + str(curses.BUTTON1_PRESSED))

				if bstate == curses.REPORT_MOUSE_POSITION:
						btype = CuEvent.MouseMove
						button = CuT.NoButton

				elif bstate == curses.BUTTON1_PRESSED:
						btype = CuEvent.MouseButtonPress
						button = CuT.LeftButton
				elif bstate == curses.BUTTON1_RELEASED:
						btype = CuEvent.MouseButtonRelease
						button = CuT.LeftButton
				elif bstate == curses.BUTTON1_CLICKED:
						btype = CuEvent.MouseButtonPress
						button = CuT.LeftButton

				elif bstate == curses.BUTTON2_PRESSED:
						btype = CuEvent.MouseButtonPress
						button = CuT.RightButton
				elif bstate == curses.BUTTON2_RELEASED:
						btype = CuEvent.MouseButtonRelease
						button = CuT.RightButton
				elif bstate == curses.BUTTON2_CLICKED:
						btype = CuEvent.MouseButtonPress
						button = CuT.RightButton

				elif bstate == curses.BUTTON3_PRESSED:
						btype = CuEvent.MouseButtonPress
						button = CuT.MidButton
				elif bstate == curses.BUTTON3_RELEASED:
						btype = CuEvent.MouseButtonRelease
						button = CuT.MidButton
				elif bstate == curses.BUTTON3_CLICKED:
						btype = CuEvent.MouseButtonPress
						button = CuT.MidButton

				elif bstate == 0x010000: # Mouse Wheel UP
						angleDelta = 120
						btype = CuEvent.Wheel
				elif bstate == 0x200000: # Mouse Wheel DOWN
						angleDelta = -120
						btype = CuEvent.Wheel

				# if bstate == curses.BUTTON1_DOUBLE_CLICKED: event =  CuEvent.MouseButtonDblClick
				# if bstate == curses.BUTTON1_TRIPLE_CLICKED: event =  CuEvent.MouseButtonPress

				mwx, mwy = CuHelper.GLBL['mainWidget'].pos()
				if btype == CuEvent.Wheel:
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
				CuTCore.cuDebug("  Pressed key " + str(event)) #, "("+keyname(event)+")")
				if event == ord("q"): break
				focusWidget = CuHelper.getFocus()
				if focusWidget is not None and event < 128:
					key_evt = CuKeyEvent(
						type = CuEvent.KeyPress,
						key  = event,
						text = str(unichr(event)))
					focusWidget.event(key_evt)





		return 0
