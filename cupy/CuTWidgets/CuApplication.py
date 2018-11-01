# -*- coding: utf-8 -*-

'''
    Application
'''

import curses, curses.panel
import sys
import struct

from CuT import CuTCore
from CuT.CuTCore import  CuT, CuPoint
from CuT.CuTCore import CuEvent, CuMouseEvent, CuWheelEvent, CuKeyEvent
from CuT.CuTHelper import CuWrapper, CuHelper
from CuT.CuTHelper.urwid.compat import bytes3

class CuApplication:
	def __init__(self, screen, argv):
		CuHelper.__CuInit__(screen)

	@staticmethod
	def wheelScrollLines():
		return 4

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
						angleDelta = CuPoint(0,120)
						btype = CuEvent.Wheel
				elif bstate == 0x200000: # Mouse Wheel DOWN
						angleDelta = CuPoint(0,-120)
						btype = CuEvent.Wheel

				# if bstate == curses.BUTTON1_DOUBLE_CLICKED: event =  CuEvent.MouseButtonDblClick
				# if bstate == curses.BUTTON1_TRIPLE_CLICKED: event =  CuEvent.MouseButtonPress
				curpos = CuPoint(x,y)
				mwpos = CuHelper.GLBL['mainWidget'].pos()
				if btype == CuEvent.Wheel:
					mouse_evt = CuWheelEvent(
						type=btype,
						pos  = curpos + mwpos,
						globalPos = curpos,
						angleDelta=angleDelta)
				else:
					mouse_evt = CuMouseEvent(
						type=btype,
						localPos  = curpos + mwpos,
						windowPos = curpos + mwpos,
						screenPos = curpos,
						button=button)

				CuHelper.GLBL['mainWidget'].event(mouse_evt)

			elif event == curses.KEY_RESIZE:
				CuHelper.refreshMain()
			else:
				# key pressed
				# CuTCore.cuDebug("  Pressed key "+str(event)+" "+hex(event)+" "+oct(event)) #, "("+keyname(event)+")")
				if event == ord("q"): break
				focusWidget = CuHelper.getFocus()
				if focusWidget is not None:
					ktype, key, text = 0, 0, ''
					if event < 127:
						if event == ord('\t'):
							CuTCore.cuDebug("Tab Pressed")
						if event == ord('\n'):
							CuTCore.cuDebug("Enter Pressed (Event TBD)")
							continue
						ktype = CuEvent.KeyRelease
						if event >= ord('a') and event <= ord('z'):
							# Remove the case feom the alphabet
							key = event - 0x20
						else:
							key = event
						if (sys.version_info > (3, 0)):
							text = str(chr(event))
						else:
							text = str(unichr(event))
					elif event > 127 and event < 256:
						# utf-8 char
						#
						# from: https://en.wikipedia.org/wiki/UTF-8
						#
						# Number
						# of                             Byte 1      Byte 2      Byte 3      Byte 4
						# Bytes
						# 1      7    U+0000   U+007F    0xxxxxxx
						# 2      11   U+0080   U+07FF    110xxxxx    10xxxxxx
						# 3      16   U+0800   U+FFFF    1110xxxx    10xxxxxx    10xxxxxx
						# 4      21   U+10000  U+10FFFF  11110xxx    10xxxxxx    10xxxxxx    10xxxxxx

						# Check 2 bytes 110xxxxx -> 0xE0 = 11100000 , 0xC0 = 11000000
						if   event & 0xE0 == 0xC0: by = 2
						# Check 3 bytes 1110xxxx -> 0xF0 = 11110000 , 0xE0 = 11100000
						elif event & 0xF0 == 0xE0: by = 3
						# Check 4 bytes 11110xxx -> 0xF8 = 11111000 , 0xF0 = 11110000
						elif event & 0xF8 == 0xF0: by = 4
						# This should never happen
						else: continue
						a = [event-256]
						while by>1:
							by -= 1
							try:
								ch = CuHelper.GLBL['screen'].getch()
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
							if ch > 127:
								a.append(ch-256)
							else:
								a.append(ch)
							CuTCore.cuDebug(" Next Unicode "+str(ch)+" "+hex(ch)+" "+oct(ch))
						ktype = CuEvent.KeyRelease
						text = struct.pack("b"*len(a),*a).decode('utf-8')
					else:
						#
						# Key Command
						# # elif event == curses.KEY_CODE_YES:    CuTCore.cuDebug("  KEY_CODE_YES")   # (0400)  A wchar_t contains a key code
						# elif event == curses.KEY_MIN:         CuTCore.cuDebug("  KEY_MIN")        # (0401)  Minimum curses key
						# elif event == curses.KEY_BREAK:       CuTCore.cuDebug("  KEY_BREAK")      # (0401)  Break key (unreliable)
						# elif event == curses.KEY_SRESET:      CuTCore.cuDebug("  KEY_SRESET")     # (0530)  Soft (partial) reset (unreliable)
						# elif event == curses.KEY_RESET:       CuTCore.cuDebug("  KEY_RESET")      # (0531)  Reset or hard reset (unreliable)
						if   event == curses.KEY_DOWN:        key = CuT.Key_Down      #; CuTCore.cuDebug("  KEY_DOWN")       # (0402)  down-arrow key
						elif event == curses.KEY_UP:          key = CuT.Key_Up        #; CuTCore.cuDebug("  KEY_UP")         # (0403)  up-arrow key
						elif event == curses.KEY_LEFT:        key = CuT.Key_Left      #; CuTCore.cuDebug("  KEY_LEFT")       # (0404)  left-arrow key
						elif event == curses.KEY_RIGHT:       key = CuT.Key_Right     #; CuTCore.cuDebug("  KEY_RIGHT")      # (0405)  right-arrow key
						elif event == curses.KEY_HOME:        key = CuT.Key_Home      #; CuTCore.cuDebug("  KEY_HOME")       # (0406)  home key
						elif event == 0x7f:                   key = CuT.Key_Backspace #; CuTCore.cuDebug("  KEY_BACKSPACE")  # (0x7f)  backspace key
						elif event == curses.KEY_BACKSPACE:   key = CuT.Key_Backspace #; CuTCore.cuDebug("  KEY_BACKSPACE")  # (0407)  backspace key
						# elif event == curses.KEY_F0:          CuTCore.cuDebug("  KEY_F0")         # (0410)  Function keys.  Space for 64
						elif event == curses.KEY_F0+ 1:       key = CuT.Key_F1       #; CuTCore.cuDebug("  KEY_F1 ")        # (KEY_F0+ 1)  Value of function key  1
						elif event == curses.KEY_F0+ 2:       key = CuT.Key_F2       #; CuTCore.cuDebug("  KEY_F2 ")        # (KEY_F0+ 2)  Value of function key  2
						elif event == curses.KEY_F0+ 3:       key = CuT.Key_F3       #; CuTCore.cuDebug("  KEY_F3 ")        # (KEY_F0+ 3)  Value of function key  3
						elif event == curses.KEY_F0+ 4:       key = CuT.Key_F4       #; CuTCore.cuDebug("  KEY_F4 ")        # (KEY_F0+ 4)  Value of function key  4
						elif event == curses.KEY_F0+ 5:       key = CuT.Key_F5       #; CuTCore.cuDebug("  KEY_F5 ")        # (KEY_F0+ 5)  Value of function key  5
						elif event == curses.KEY_F0+ 6:       key = CuT.Key_F6       #; CuTCore.cuDebug("  KEY_F6 ")        # (KEY_F0+ 6)  Value of function key  6
						elif event == curses.KEY_F0+ 7:       key = CuT.Key_F7       #; CuTCore.cuDebug("  KEY_F7 ")        # (KEY_F0+ 7)  Value of function key  7
						elif event == curses.KEY_F0+ 8:       key = CuT.Key_F8       #; CuTCore.cuDebug("  KEY_F8 ")        # (KEY_F0+ 8)  Value of function key  8
						elif event == curses.KEY_F0+ 9:       key = CuT.Key_F9       #; CuTCore.cuDebug("  KEY_F9 ")        # (KEY_F0+ 9)  Value of function key  9
						elif event == curses.KEY_F0+10:       key = CuT.Key_F10      #; CuTCore.cuDebug("  KEY_F10")        # (KEY_F0+10)  Value of function key 10
						elif event == curses.KEY_F0+11:       key = CuT.Key_F11      #; CuTCore.cuDebug("  KEY_F11")        # (KEY_F0+11)  Value of function key 11
						elif event == curses.KEY_F0+12:       key = CuT.Key_F12      #; CuTCore.cuDebug("  KEY_F12")        # (KEY_F0+12)  Value of function key 12
						# elif event == curses.KEY_DL:          CuTCore.cuDebug("  KEY_DL")         # (0510)  delete-line key
						# elif event == curses.KEY_IL:          CuTCore.cuDebug("  KEY_IL")         # (0511)  insert-line key
						elif event == curses.KEY_DC:          key = CuT.Key_Delete   ; CuTCore.cuDebug("  KEY_DC")         # (0512)  delete-character key
						elif event == curses.KEY_IC:          key = CuT.Key_Insert   ; CuTCore.cuDebug("  KEY_IC")         # (0513)  insert-character key
						# elif event == curses.KEY_EIC:         CuTCore.cuDebug("  KEY_EIC")        # (0514)  sent by rmir or smir in insert mode
						# elif event == curses.KEY_CLEAR:       CuTCore.cuDebug("  KEY_CLEAR")      # (0515)  clear-screen or erase key
						# elif event == curses.KEY_EOS:         CuTCore.cuDebug("  KEY_EOS")        # (0516)  clear-to-end-of-screen key
						# elif event == curses.KEY_EOL:         CuTCore.cuDebug("  KEY_EOL")        # (0517)  clear-to-end-of-line key
						# elif event == curses.KEY_SF:          CuTCore.cuDebug("  KEY_SF")         # (0520)  scroll-forward key
						# elif event == curses.KEY_SR:          CuTCore.cuDebug("  KEY_SR")         # (0521)  scroll-backward key
						elif event == curses.KEY_NPAGE:       key = CuT.Key_PageDown ; CuTCore.cuDebug("  KEY_NPAGE")      # (0522)  next-page key
						elif event == curses.KEY_PPAGE:       key = CuT.Key_PageUp   ; CuTCore.cuDebug("  KEY_PPAGE")      # (0523)  previous-page key
						# elif event == curses.KEY_STAB:        CuTCore.cuDebug("  KEY_STAB")       # (0524)  set-tab key
						# elif event == curses.KEY_CTAB:        CuTCore.cuDebug("  KEY_CTAB")       # (0525)  clear-tab key
						# elif event == curses.KEY_CATAB:       CuTCore.cuDebug("  KEY_CATAB")      # (0526)  clear-all-tabs key
						# elif event == curses.KEY_ENTER:       CuTCore.cuDebug("  KEY_ENTER")      # (0527)  enter/send key
						# elif event == curses.KEY_PRINT:       CuTCore.cuDebug("  KEY_PRINT")      # (0532)  print key
						# elif event == curses.KEY_LL:          CuTCore.cuDebug("  KEY_LL")         # (0533)  lower-left key (home down)
						# elif event == curses.KEY_A1:          CuTCore.cuDebug("  KEY_A1")         # (0534)  upper left of keypad
						# elif event == curses.KEY_A3:          CuTCore.cuDebug("  KEY_A3")         # (0535)  upper right of keypad
						# elif event == curses.KEY_B2:          CuTCore.cuDebug("  KEY_B2")         # (0536)  center of keypad
						# elif event == curses.KEY_C1:          CuTCore.cuDebug("  KEY_C1")         # (0537)  lower left of keypad
						# elif event == curses.KEY_C3:          CuTCore.cuDebug("  KEY_C3")         # (0540)  lower right of keypad
						# elif event == curses.KEY_BTAB:        CuTCore.cuDebug("  KEY_BTAB")       # (0541)  back-tab key
						# elif event == curses.KEY_BEG:         CuTCore.cuDebug("  KEY_BEG")        # (0542)  begin key
						# elif event == curses.KEY_CANCEL:      CuTCore.cuDebug("  KEY_CANCEL")     # (0543)  cancel key
						# elif event == curses.KEY_CLOSE:       CuTCore.cuDebug("  KEY_CLOSE")      # (0544)  close key
						# elif event == curses.KEY_COMMAND:     CuTCore.cuDebug("  KEY_COMMAND")    # (0545)  command key
						# elif event == curses.KEY_COPY:        CuTCore.cuDebug("  KEY_COPY")       # (0546)  copy key
						# elif event == curses.KEY_CREATE:      CuTCore.cuDebug("  KEY_CREATE")     # (0547)  create key
						elif event == curses.KEY_END:         key = CuT.Key_End      ; CuTCore.cuDebug("  KEY_END")        # (0550)  end key
						# elif event == curses.KEY_EXIT:        CuTCore.cuDebug("  KEY_EXIT")       # (0551)  exit key
						# elif event == curses.KEY_FIND:        CuTCore.cuDebug("  KEY_FIND")       # (0552)  find key
						# elif event == curses.KEY_HELP:        CuTCore.cuDebug("  KEY_HELP")       # (0553)  help key
						# elif event == curses.KEY_MARK:        CuTCore.cuDebug("  KEY_MARK")       # (0554)  mark key
						# elif event == curses.KEY_MESSAGE:     CuTCore.cuDebug("  KEY_MESSAGE")    # (0555)  message key
						# elif event == curses.KEY_MOVE:        CuTCore.cuDebug("  KEY_MOVE")       # (0556)  move key
						# elif event == curses.KEY_NEXT:        CuTCore.cuDebug("  KEY_NEXT")       # (0557)  next key
						# elif event == curses.KEY_OPEN:        CuTCore.cuDebug("  KEY_OPEN")       # (0560)  open key
						# elif event == curses.KEY_OPTIONS:     CuTCore.cuDebug("  KEY_OPTIONS")    # (0561)  options key
						# elif event == curses.KEY_PREVIOUS:    CuTCore.cuDebug("  KEY_PREVIOUS")   # (0562)  previous key
						# elif event == curses.KEY_REDO:        CuTCore.cuDebug("  KEY_REDO")       # (0563)  redo key
						# elif event == curses.KEY_REFERENCE:   CuTCore.cuDebug("  KEY_REFERENCE")  # (0564)  reference key
						# elif event == curses.KEY_REFRESH:     CuTCore.cuDebug("  KEY_REFRESH")    # (0565)  refresh key
						# elif event == curses.KEY_REPLACE:     CuTCore.cuDebug("  KEY_REPLACE")    # (0566)  replace key
						# elif event == curses.KEY_RESTART:     CuTCore.cuDebug("  KEY_RESTART")    # (0567)  restart key
						# elif event == curses.KEY_RESUME:      CuTCore.cuDebug("  KEY_RESUME")     # (0570)  resume key
						# elif event == curses.KEY_SAVE:        CuTCore.cuDebug("  KEY_SAVE")       # (0571)  save key
						# elif event == curses.KEY_SBEG:        CuTCore.cuDebug("  KEY_SBEG")       # (0572)  shifted begin key
						# elif event == curses.KEY_SCANCEL:     CuTCore.cuDebug("  KEY_SCANCEL")    # (0573)  shifted cancel key
						# elif event == curses.KEY_SCOMMAND:    CuTCore.cuDebug("  KEY_SCOMMAND")   # (0574)  shifted command key
						# elif event == curses.KEY_SCOPY:       CuTCore.cuDebug("  KEY_SCOPY")      # (0575)  shifted copy key
						# elif event == curses.KEY_SCREATE:     CuTCore.cuDebug("  KEY_SCREATE")    # (0576)  shifted create key
						# elif event == curses.KEY_SDC:         CuTCore.cuDebug("  KEY_SDC")        # (0577)  shifted delete-character key
						# elif event == curses.KEY_SDL:         CuTCore.cuDebug("  KEY_SDL")        # (0600)  shifted delete-line key
						# elif event == curses.KEY_SELECT:      CuTCore.cuDebug("  KEY_SELECT")     # (0601)  select key
						# elif event == curses.KEY_SEND:        CuTCore.cuDebug("  KEY_SEND")       # (0602)  shifted end key
						# elif event == curses.KEY_SEOL:        CuTCore.cuDebug("  KEY_SEOL")       # (0603)  shifted clear-to-end-of-line key
						# elif event == curses.KEY_SEXIT:       CuTCore.cuDebug("  KEY_SEXIT")      # (0604)  shifted exit key
						# elif event == curses.KEY_SFIND:       CuTCore.cuDebug("  KEY_SFIND")      # (0605)  shifted find key
						# elif event == curses.KEY_SHELP:       CuTCore.cuDebug("  KEY_SHELP")      # (0606)  shifted help key
						# elif event == curses.KEY_SHOME:       CuTCore.cuDebug("  KEY_SHOME")      # (0607)  shifted home key
						# elif event == curses.KEY_SIC:         CuTCore.cuDebug("  KEY_SIC")        # (0610)  shifted insert-character key
						# elif event == curses.KEY_SLEFT:       CuTCore.cuDebug("  KEY_SLEFT")      # (0611)  shifted left-arrow key
						# elif event == curses.KEY_SMESSAGE:    CuTCore.cuDebug("  KEY_SMESSAGE")   # (0612)  shifted message key
						# elif event == curses.KEY_SMOVE:       CuTCore.cuDebug("  KEY_SMOVE")      # (0613)  shifted move key
						# elif event == curses.KEY_SNEXT:       CuTCore.cuDebug("  KEY_SNEXT")      # (0614)  shifted next key
						# elif event == curses.KEY_SOPTIONS:    CuTCore.cuDebug("  KEY_SOPTIONS")   # (0615)  shifted options key
						# elif event == curses.KEY_SPREVIOUS:   CuTCore.cuDebug("  KEY_SPREVIOUS")  # (0616)  shifted previous key
						# elif event == curses.KEY_SPRINT:      CuTCore.cuDebug("  KEY_SPRINT")     # (0617)  shifted print key
						# elif event == curses.KEY_SREDO:       CuTCore.cuDebug("  KEY_SREDO")      # (0620)  shifted redo key
						# elif event == curses.KEY_SREPLACE:    CuTCore.cuDebug("  KEY_SREPLACE")   # (0621)  shifted replace key
						# elif event == curses.KEY_SRIGHT:      CuTCore.cuDebug("  KEY_SRIGHT")     # (0622)  shifted right-arrow key
						# elif event == curses.KEY_SRSUME:      CuTCore.cuDebug("  KEY_SRSUME")     # (0623)  shifted resume key
						# elif event == curses.KEY_SSAVE:       CuTCore.cuDebug("  KEY_SSAVE")      # (0624)  shifted save key
						# elif event == curses.KEY_SSUSPEND:    CuTCore.cuDebug("  KEY_SSUSPEND")   # (0625)  shifted suspend key
						# elif event == curses.KEY_SUNDO:       CuTCore.cuDebug("  KEY_SUNDO")      # (0626)  shifted undo key
						# elif event == curses.KEY_SUSPEND:     CuTCore.cuDebug("  KEY_SUSPEND")    # (0627)  suspend key
						# elif event == curses.KEY_UNDO:        CuTCore.cuDebug("  KEY_UNDO")       # (0630)  undo key
						# elif event == curses.KEY_MOUSE:       CuTCore.cuDebug("  KEY_MOUSE")      # (0631)  Mouse event has occurred
						# elif event == curses.KEY_RESIZE:      CuTCore.cuDebug("  KEY_RESIZE")     # (0632)  Terminal resize event
						# elif event == curses.KEY_EVENT:       CuTCore.cuDebug("  KEY_EVENT")      # (0633)  We were interrupted by an event
						# elif event == curses.KEY_MAX:         CuTCore.cuDebug("  KEY_MAX")        # (0777)  Maximum key value is 0633
						if key != 0:
							ktype = CuEvent.KeyRelease
					if ktype != 0:
						key_evt = CuKeyEvent(
								type = ktype,
								key  = key,
								text = text)
						focusWidget.event(key_evt)







		return 0
