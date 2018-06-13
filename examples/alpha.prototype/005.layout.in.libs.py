#!/usr/bin/python

import sys

from CuT import CuTCore, CuTWidgets

class CuTestInput(CuTWidgets.CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0
	_iterator = 0

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)




	def paint(self):
		CuTWidgets.CuWidget.paint(self)
		# self.getWin().clear()
		self.getWin().addstr(3, 3, "CuTestInput... [" + self._name + "] it: " + str(self._iterator))
		self.getWin().addstr(4, 3, "    id: " + str(self._id))
		self.getWin().addstr(5, 3, "     x: " + str(self._ix))
		self.getWin().addstr(6, 3, "     y: " + str(self._iy))
		self.getWin().addstr(7, 3, "     z: " + str(self._iz))
		self.getWin().addstr(8, 3, "bstate: " + str(self._bstate) + "        ")
		self.getWin().addstr(9, 3, "childs: " + str(len(self._childs)))

	def event(self, evt):
		if isinstance(evt, CuTCore.CuMouseEvent):
			self._id, self._ix, self._iy, self._iz, self._bstate = evt.getmouse()

	def setIterator(self, it):
		self._iterator = it;

class CuMovableTestInput(CuTestInput):
	_state = None
	_px, _py = 0, 0
	_mx, _my = 0, 0

	def paint(self):
		CuTestInput.paint(self)
		self.getWin().addstr(2, 3, "[MOVABLE] " + str(self._state) + "    ")

	def event(self, evt):
		CuTestInput.event(self, evt)
		if isinstance(evt, CuTCore.CuMouseEvent):
			x, y = evt.globalPos()
			if evt.getState() == evt.MOUSE_CLICKED:
				self._state = "Clicked"
			elif evt.getState() == evt.MOUSE_PRESSED:
				self._state = "Pressed"
				self._px, self._py = self.getPos()
				self._mx, self._my = x, y
			elif evt.getState() == evt.MOUSE_RELEASED:
				self._state = None
			elif evt.getState() == evt.REPORT_MOUSE_POSITION:
				if self._state == "Pressed":
					newx = self._px+x-self._mx
					newy = self._py+y-self._my
					if newx < 0: newx=0
					if newy < 0: newy=0
					if newx+self._w > CuTWidgets.CuApplication.getW() : newx=CuTWidgets.CuApplication.getW()-self._w
					if newy+self._h > CuTWidgets.CuApplication.getH() : newy=CuTWidgets.CuApplication.getH()-self._h
					self.move(newx, newy);



def main(screen):
	app = CuTWidgets.CuApplication(screen, sys.argv)

	mw = CuTWidgets.CuMainWindow()
	mw.setBorder(True)

	layout = CuTWidgets.CuHLayout()

	tw1 = CuTestInput(parent=mw, name='tw1')
	tw1.setBorder(True)
	layout.addWidget(tw1)

	tw2 = CuTestInput(parent=mw, name='tw2')
	tw2.setBorder(True)
	layout.addWidget(tw2)

	vlayout = CuTWidgets.CuVLayout()
	p1 = CuTWidgets.CuPanel(parent=mw, name='p1')
	p1.setBorder(True)
	layout.addWidget(p1)

	tw4 = CuTestInput(parent=mw, name='tw4')
	tw4.setBorder(True)
	layout.addWidget(tw4)

	tw3 = CuTestInput(parent=p1, name='tw3')
	tw3.setBorder(True)
	vlayout.addWidget(tw3)

	mtw1 = CuMovableTestInput(parent=p1, name='mtw1')
	mtw1.setBorder(True)
	vlayout.addWidget(mtw1)

	mw.setLayout(layout)
	p1.setLayout(vlayout)
	mw.show()

	# sys.exit()
	app.exec_()


CuTCore.CuWrapper(main)
