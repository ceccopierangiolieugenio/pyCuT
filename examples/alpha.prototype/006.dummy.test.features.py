#!/usr/bin/python

import sys
import logging

from CuT import CuTCore, CuTWidgets
from CuT.CuTCore import  CuT, CuEvent
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

logging.basicConfig(filename='session.log',level=logging.DEBUG)

class CuTestInput(CuTWidgets.CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0
	_gx, _gy, _sx, _sy, _wx, _wy = 0, 0, 0, 0, 0, 0
	_inside = False
	_wheelAngle  = 0

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)

	def paintEvent(self, event):
		# logging.debug("Paint - evt:"+str(event)+" Name:"+self.accessibleName())
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		if self.underMouse():
			qp.drawText(3, 3, "CuTestInput... [" + self.accessibleName() + "] [X]")
		else:
			qp.drawText(3, 3, "CuTestInput... [" + self.accessibleName() + "] [ ]")
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
		if self._wheelAngle == 0:
			qp.drawText(3, 12, "bstate: " + str(self._bstate) + "                ")
		elif self._wheelAngle > 0:
			qp.drawText(3, 12, "bstate: Wheel - UP        ")
			self._wheelAngle = 0
		elif self._wheelAngle < 0:
			qp.drawText(3, 12, "bstate: Wheel - DOWN        ")
			self._wheelAngle = 0
		qp.setPen(CuT.lightGray)
		qp.drawText(3, 15, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkGreen)
		qp.drawText(0, 0,               "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.drawText(0, self.height()-1, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()

#	def enterEvent(self, evt): pass
	def leaveEvent(self, evt):
		self.update()

	def wheelEvent(self, evt):
		logging.debug("evt:"+str(evt.type())+" Name:"+self.accessibleName())
		self._wheelAngle = evt.angleDelta()
		self.update()

	def event(self, evt):
		#logging.debug("evt:"+str(evt.type())+" Name:"+self.accessibleName())
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
		qp.drawText(3, 19, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()

	def mousePressEvent(self, evt):
		logging.debug("evt:"+str(evt.type())+" Name:"+self.accessibleName())
		if evt.type() == CuT.LeftButton:
			self._state = "Pressed"
			self._px, self._py = self.pos()
			self._mx, self._my = evt.screenPos()

	def mouseReleaseEvent(self, evt):
		self._state = None

	def event(self, evt):
		if isinstance(evt, CuTCore.CuMouseEvent):
			x, y = evt.screenPos()
			if evt.button() == CuEvent.MouseMove:
				if self._state == "Pressed":
					newx = self._px+x-self._mx
					newy = self._py+y-self._my
					self.move(newx, newy);
			self.update()
		return CuTestInput.event(self, evt)

def addFrame(widget):
	f = CuTWidgets.CuFrame(parent=widget.parentWidget())
	f.resize(100,100)
	l = CuTWidgets.CuHBoxLayout()
	widget.setParent(f)
	l.addWidget(widget)
	f.setLayout(l)
	return f

def main(screen):
	app = CuTWidgets.CuApplication(screen, sys.argv)

	mw = CuTWidgets.CuMainWindow(name='MW')
	mw.setMaximumSize(180,60)
	mw.setMinimumSize(60,30)

	layout = CuTWidgets.CuHBoxLayout()

	tw1 = addFrame(CuTestInput(parent=mw, name='tw1'))
	layout.addWidget(tw1)

	vlayout2 = CuTWidgets.CuVBoxLayout()

	tw2 = addFrame(addFrame(CuTestInput(parent=mw, name='tw2')))
	vlayout2.addWidget(tw2)

	tw2_1 = addFrame(CuMovableTestInput(parent=mw, name='tw2.1'))
	vlayout2.addWidget(tw2_1)

	tw2_2 = CuTestInput(parent=mw, name='tw2.2')
	vlayout2.addWidget(tw2_2)

	layout.addItem(vlayout2)

	vlayout = CuTWidgets.CuVBoxLayout()
	f1 = CuTWidgets.CuFrame(parent=mw, name='f1')
	layout.addWidget(f1)

	tw4 = CuTestInput(parent=mw, name='tw4')
	layout.addWidget(tw4)

	tw3 = CuTestInput(parent=f1, name='tw3')
	vlayout.addWidget(tw3)

	mtw1 = addFrame(addFrame(CuMovableTestInput(parent=f1, name='mtw1')))
	vlayout.addWidget(mtw1)

	mw.setLayout(layout)
	f1.setLayout(vlayout)
	mw.show()

	app.exec_()


CuWrapper.init(main)
