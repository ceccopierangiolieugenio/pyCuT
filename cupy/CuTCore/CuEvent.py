'''
    Event
'''

import curses, curses.panel
import logging

class CuEvent:
	ERR = 0
	KEY_MOUSE = 1

	def __init__(self, type=ERR):
		self.type = type;

class CuMouseEvent(CuEvent):
	_id, _x, _y, _z, _bstate = 0, 0, 0, 0, 0

	MOUSE_PRESSED = 1
	MOUSE_RELEASED = 2
	MOUSE_CLICKED = 3
	MOUSE_DOUBLE_CLICKED = 4
	MOUSE_TRIPLE_CLICKED = 5

	REPORT_MOUSE_POSITION = 1000

	def __init__(self):
		CuEvent.__init__(self,type=CuEvent.KEY_MOUSE)
		self._id, self._x, self._y, self._z, self._bstate = curses.getmouse()

	def getmouse(self):
		return self._id, self._x, self._y, self._z, self._bstate

	def globalPos(self):
		return self._x, self._y

	def getState(self):
		if self._bstate == curses.BUTTON1_PRESSED:        return CuMouseEvent.MOUSE_PRESSED
		if self._bstate == curses.BUTTON1_RELEASED:       return CuMouseEvent.MOUSE_RELEASED
		if self._bstate == curses.BUTTON1_CLICKED:        return CuMouseEvent.MOUSE_CLICKED
		if self._bstate == curses.BUTTON1_DOUBLE_CLICKED: return CuMouseEvent.MOUSE_DOUBLE_CLICKED
		if self._bstate == curses.BUTTON1_TRIPLE_CLICKED: return CuMouseEvent.MOUSE_TRIPLE_CLICKED
		if self._bstate == curses.REPORT_MOUSE_POSITION:  return CuMouseEvent.REPORT_MOUSE_POSITION
		return None
