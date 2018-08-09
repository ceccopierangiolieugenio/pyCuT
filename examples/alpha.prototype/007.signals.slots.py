#!/usr/bin/python

import sys
import logging

from CuT import CuTCore, CuTWidgets
from CuT.CuTCore import  CuT, CuEvent, pycutSlot, pycutSignal
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

# logging.basicConfig(filename='session.log',level=logging.DEBUG)

class CuTestInput(CuTWidgets.CuWidget):
	_id, _ix, _iy, _iz, _bstate = 0, 0, 0, 0, 0
	_gx, _gy, _sx, _sy, _wx, _wy = 0, 0, 0, 0, 0, 0
	_inside = False
	triggered_slot = 0
	_wheelAngle  = 0

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)

		self.test_signal_in_001 = pycutSignal(int)
		self.test_signal_in_002 = pycutSignal(int, int)
		# self.test_signal = pycutSignal(int, str)

	test_signal = pycutSignal(int, str)
	test_signal_out_001 = pycutSignal(int, int, int)
	test_signal_out_002 = pycutSignal(int, int, int, int)

	@pycutSlot(int, str)
	def test_slot(self, x, y):
		logging.debug("test_slot triggered - Name:" + self.accessibleName() + " x:" + str(x) + " y:" + y)
		self.triggered_slot += 1
		self.update()

	def mousePressEvent(self, evt):
		logging.debug("Emitting Signal - Name:" + self.accessibleName())
		self.test_signal.emit(123, 'Eugenio')

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
		qp.setPen(CuT.blue)
		qp.drawText(3, 13, "Triggered Slot: " + str(self.triggered_slot))
		qp.setPen(CuT.lightGray)
		qp.drawText(3, 15, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkGreen)
		qp.drawText(0, 0,               "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.drawText(0, self.height()-1, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()

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
	mw.setMaximumSize(120,40)
	mw.setMinimumSize(60,30)

	layout = CuTWidgets.CuHBoxLayout()

	ti1 = CuTestInput(parent=mw, name='Sender')
	tw1 = addFrame(ti1)
	layout.addWidget(tw1)

	vlayout2 = CuTWidgets.CuVBoxLayout()
	ti2 = CuTestInput(parent=mw, name='Recv_1')
	tw2 = addFrame(addFrame(ti2))
	vlayout2.addWidget(tw2)

	tw2_2 = CuTestInput(parent=mw, name='Recv_2')
	vlayout2.addWidget(tw2_2)

	ti1.test_signal.connect(ti2.test_slot)
	ti1.test_signal.connect(tw2_2.test_slot)

	ti2.test_signal.connect(ti1.test_slot)
	ti2.test_signal.connect(tw2_2.test_slot)
	tw2_2.test_signal.connect(ti1.test_slot)

	logging.debug("signal ti1.test_signal:        " + str(ti1.test_signal))
	logging.debug("signal ti1.test_signal_out_001:" + str(ti1.test_signal_out_001))
	logging.debug("signal ti1.test_signal_out_002:" + str(ti1.test_signal_out_002))
	logging.debug("signal ti1.test_signal_in_001: " + str(ti1.test_signal_in_001))
	logging.debug("signal ti1.test_signal_in_002: " + str(ti1.test_signal_in_002))

	logging.debug("signal ti1.test_signal:        " + str(ti1.test_signal))
	logging.debug("signal ti1.test_signal_out_001:" + str(ti1.test_signal_out_001))
	logging.debug("signal ti1.test_signal_out_002:" + str(ti1.test_signal_out_002))
	logging.debug("signal ti1.test_signal_in_001: " + str(ti1.test_signal_in_001))
	logging.debug("signal ti1.test_signal_in_002: " + str(ti1.test_signal_in_002))

	layout.addItem(vlayout2)

	mw.setLayout(layout)
	mw.show()

	app.exec_()


CuWrapper.init(main)
