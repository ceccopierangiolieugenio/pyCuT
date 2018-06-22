#!/usr/bin/python

import sys

from CuT import CuTCore, CuTWidgets
from CuT.CuTCore import  CuT
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

class CuTestInput(CuTWidgets.CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)

	def paintEvent(self, event):
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		qp.drawText(3, 3, "CuTestInput... [" + self.accessibleName() + "]")
		qp.setPen(CuT.yellow)
		qp.drawText(3, 4, "    id: " + str(self._id))
		qp.setPen(CuT.green)
		qp.drawText(3, 5, "     x: " + str(self._ix))
		qp.drawText(3, 6, "     y: " + str(self._iy))
		qp.drawText(3, 7, "     z: " + str(self._iz))
		qp.setPen(CuT.red)
		qp.drawText(3, 8, "bstate: " + str(self._bstate) + "        ")
		qp.setPen(CuT.lightGray)
		qp.drawText(3, 12, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()

	def event(self, evt):
		if isinstance(evt, CuTCore.CuMouseEvent):
			self._id, self._ix, self._iy, self._iz, self._bstate = evt.getmouse()
		self.update()

class CuMovableTestInput(CuTestInput):
	_state = None
	_px, _py = 0, 0
	_mx, _my = 0, 0

	def paintEvent(self, event):
		CuTestInput.paintEvent(self, event)
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.blue)
		qp.drawText(3, 2, "[MOVABLE] " + str(self._state) + "    ")
		qp.end()

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
					if newx+self.width()  > CuTWidgets.CuApplication.getW() : newx=CuTWidgets.CuApplication.getW()-self.width()
					if newy+self.height() > CuTWidgets.CuApplication.getH() : newy=CuTWidgets.CuApplication.getH()-self.height()
					self.move(newx, newy);
			self.update()



def main(screen):
	app = CuTWidgets.CuApplication(screen, sys.argv)

	mw = CuTWidgets.CuMainWindow()
	mw.setBorder(True)

	layout = CuTWidgets.CuHBoxLayout()

	tw1 = CuTestInput(parent=mw, name='tw1')
	tw1.setBorder(True)
	layout.addWidget(tw1)

	tw2 = CuTestInput(parent=mw, name='tw2')
	tw2.setBorder(True)
	layout.addWidget(tw2)

	vlayout = CuTWidgets.CuVBoxLayout()
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


CuWrapper.init(main)
