#!/usr/bin/python

import sys

from CuT import CuTCore, CuTWidgets
from CuT.CuTCore import  CuT, CuEvent
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

class CuTestInput(CuTWidgets.CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0
	_gx, _gy, _sx, _sy, _wx, _wy = 0, 0, 0, 0, 0, 0

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)

	def paintEvent(self, event):
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		qp.drawText(3, 3, "CuTestInput... [" + self.accessibleName() + "]")
		qp.setPen(CuT.yellow)
		qp.drawText(3, 4, "     x: "  + str(self._ix) + "   ")
		qp.drawText(3, 5, "     y: "  + str(self._iy) + "   ")
		qp.setPen(CuT.green)
		qp.drawText(3, 6, "     gx: " + str(self._gx) + "   ")
		qp.drawText(3, 7, "     gy: " + str(self._gy) + "   ")
		qp.drawText(3, 8, "     sx: " + str(self._sx) + "   ")
		qp.drawText(3, 9, "     sy: " + str(self._sy) + "   ")
		qp.drawText(3,10, "     wx: " + str(self._wx) + "   ")
		qp.drawText(3,11, "     wy: " + str(self._wy) + "   ")
		qp.setPen(CuT.red)
		qp.drawText(3, 12, "bstate: " + str(self._bstate) + "        ")
		qp.setPen(CuT.lightGray)
		qp.drawText(3, 15, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()

	def event(self, evt):
		if isinstance(evt, CuTCore.CuMouseEvent):
			self._ix, self._iy = evt.pos()
			self._gx, self._gy = evt.globalPos()
			self._sx, self._sy = evt.screenPos()
			self._wx, self._wy = evt.screenPos()
			self._bstate = evt.button()
		self.update()
		return CuTWidgets.CuWidget.event(self, evt)

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
		if isinstance(evt, CuTCore.CuMouseEvent):
			x, y = evt.screenPos()
			#if evt.button() == CuEvent.MouseButtonPress:
			#	self._state = "Clicked"
			if evt.button() == CuEvent.MouseButtonPress:
				self._state = "Pressed"
				self._px, self._py = self.getPos()
				self._mx, self._my = x, y
			elif evt.button() == CuEvent.MouseButtonRelease:
				self._state = None
			elif evt.button() == CuEvent.MouseMove:
				if self._state == "Pressed":
					newx = self._px+x-self._mx
					newy = self._py+y-self._my
					if newx < 0: newx=0
					if newy < 0: newy=0
					if newx+self.width()  > CuTWidgets.CuApplication.getW() : newx=CuTWidgets.CuApplication.getW()-self.width()
					if newy+self.height() > CuTWidgets.CuApplication.getH() : newy=CuTWidgets.CuApplication.getH()-self.height()
					self.move(newx, newy);
			self.update()
			# return True
			return CuTestInput.event(self, evt)



def main(screen):
	app = CuTWidgets.CuApplication(screen, sys.argv)

	mw = CuTWidgets.CuMainWindow()
	mw.setMaximumSize(180,50)
	mw.setMinimumSize(60,30)
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
