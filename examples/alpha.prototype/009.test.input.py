#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging

from CuT import CuTCore, CuTWidgets
from CuT.CuTCore import  CuT, CuEvent, pycutSlot, pycutSignal
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

class CuTestInput(CuTWidgets.CuWidget):
	_bstate = 0
	_wheelAngle  = 0

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)

	def leaveEvent(self, evt):
		self.update()

	def wheelEvent(self, evt):
		logging.debug("evt:"+str(evt.type())+" Name:"+self.accessibleName())
		self._wheelAngle = evt.angleDelta()
		self.update()

	def event(self, evt):
		if isinstance(evt, CuTCore.CuMouseEvent):
			self._bstate = evt.button()
		self.update()
		return CuTWidgets.CuWidget.event(self, evt)

	def paintEvent(self, event):
		# logging.debug("Paint - evt:"+str(event)+" Name:"+self.accessibleName())
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		if self.underMouse():
			qp.drawText(3, 3, "CuTestFocus... [" + self.accessibleName() + "] [X]")
		else:
			qp.drawText(3, 3, "CuTestFocus... [" + self.accessibleName() + "] [ ]")
		qp.setPen(CuT.red)
		if self._wheelAngle == 0:
			qp.drawText(3, 5, "bstate: " + str(self._bstate) + "                ")
		elif self._wheelAngle > 0:
			qp.drawText(3, 5, "bstate: Wheel - UP        ")
			self._wheelAngle = 0
		elif self._wheelAngle < 0:
			qp.drawText(3, 5, "bstate: Wheel - DOWN        ")
			self._wheelAngle = 0
		qp.setPen(CuT.green)
		if self.hasFocus():
			qp.drawText(3, 6, "Focus: [X]")
		else:
			qp.drawText(3, 6, "Focus: [ ]")
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

def cut_message_handler(mode, context, message):
	if mode == CuTCore.CuTInfoMsg:
		mode = 'INFO'
	elif mode == CuTCore.CuTWarningMsg:
		mode = 'WARNING'
	elif mode == CuTCore.CuTCriticalMsg:
		mode = 'CRITICAL'
	elif mode == CuTCore.CuTFatalMsg:
		mode = 'FATAL'
	else:
		mode = 'DEBUG'
	logging.debug('cut_message_handler: line: %d, func: %s(), file: %s' % (
			context.line, context.function, context.file))
	logging.debug('  %s: %s\n' % (mode, message))

logging.basicConfig(filename='session.log',level=logging.DEBUG)
CuTCore.cuInstallMessageHandler(cut_message_handler)

def main(screen):
	app = CuTWidgets.CuApplication(screen, sys.argv)

	CuTCore.cuDebug('something informative')

	mainLayout = CuTWidgets.CuVBoxLayout()

	mw = CuTWidgets.CuMainWindow(name='MW')
	mw.setMaximumSize(120,60)
	mw.setMinimumSize(80,30)

	layout = CuTWidgets.CuHBoxLayout()

	ti1 = CuTestInput(parent=mw, name='Focus 001')
	ti1.setFocusPolicy(CuT.StrongFocus)
	tw1 = addFrame(ti1)
	layout.addWidget(tw1)

	vlayout2 = CuTWidgets.CuVBoxLayout()
	ti2 = CuTestInput(parent=mw, name='Wheel Focus 002')
	ti2.setFocusPolicy(CuT.WheelFocus)
	tw2 = addFrame(addFrame(ti2))
	vlayout2.addWidget(tw2)

	ti3 = CuTestInput(parent=mw, name='Disabled Focus')
	ti3.setFocusPolicy(CuT.NoFocus)
	vlayout2.addWidget(ti3)

	log = CuTWidgets.CuPlainTextEdit(parent=mw)
	log.setMaximumSize(10000,20)
	log.setMinimumSize(10,20)

	layout.addItem(vlayout2)

	mainLayout.addItem(layout)
	mainLayout.addWidget(log)

	mw.setLayout(mainLayout)
	mw.show()

	app.exec_()


CuWrapper.init(main)
