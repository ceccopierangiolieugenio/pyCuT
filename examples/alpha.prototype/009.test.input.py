#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging

from CuT import CuTCore, CuTWidgets
from CuT.CuTCore import  CuT, CuPoint, CuSize,  CuEvent, pycutSlot, pycutSignal
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

class CuTestInput(CuTWidgets.CuWidget):
	_bstate = 0
	_wheelAngle  = 0
	_key = ' '

	def __init__(self, *args, **kwargs):
		CuTWidgets.CuWidget.__init__(self, *args, **kwargs)

	def leaveEvent(self, evt):
		self.update()

	def wheelEvent(self, evt):
		logging.debug("evt:"+str(evt.type())+" Name:"+self.accessibleName())
		self._wheelAngle = evt.angleDelta().y()
		self.update()

	def keyReleaseEvent(self, evt):
		self._key = evt.text()
		self.update()

	def event(self, evt):
		if isinstance(evt, CuTCore.CuMouseEvent):
			self._bstate = evt.button()
		self.update()
		return CuTWidgets.CuWidget.event(self, evt)

	def paintEvent(self, event):
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
		qp.setPen(CuT.yellow)
		qp.drawText(3, 7, "Key Pressed: " + self._key.ljust(4))

		qp.setPen(CuT.color0)
		qp.drawText(3, 9,  "color0      abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.color1)
		qp.drawText(3, 10, "color1      abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.black)
		qp.drawText(3, 11, "black       abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.white)
		qp.drawText(3, 12, "white       abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkGray)
		qp.drawText(3, 13, "darkGray    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.gray)
		qp.drawText(3, 14, "gray        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.lightGray)
		qp.drawText(3, 15, "lightGray   abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.red)
		qp.drawText(3, 16, "red         abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.green)
		qp.drawText(3, 17, "green       abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.blue)
		qp.drawText(3, 18, "blue        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.cyan)
		qp.drawText(3, 19, "cyan        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.magenta)
		qp.drawText(3, 20, "magenta     abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.yellow)
		qp.drawText(3, 21, "yellow      abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkRed)
		qp.drawText(3, 22, "darkRed     abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkGreen)
		qp.drawText(3, 23, "darkGreen   abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkBlue)
		qp.drawText(3, 24, "darkBlue    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkCyan)
		qp.drawText(3, 25, "darkCyan    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkMagenta)
		qp.drawText(3, 26, "darkMagenta abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.darkYellow)
		qp.drawText(3, 27, "darkYellow  abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.setPen(CuT.transparent)
		qp.drawText(3, 28, "transparent abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

		qp.setPen(CuT.yellow)
		qp.setBrush(CuT.red)
		qp.drawText(3, 30, " Eugenio ")
		qp.setPen(CuT.red)
		qp.setBrush(CuT.yellow)
		qp.drawText(12, 30, " Parodi ")

		qp.setPen(CuT.yellow)
		qp.setBrush(CuT.gray)
		qp.drawText(3, 31, " Eugenio ")
		qp.setPen(CuT.red)
		qp.setBrush(CuT.gray)
		qp.drawText(12, 31, " Parodi ")

		qp.setBrush(CuT.black)

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
	log = None
	def cut_message_handler(mode, context, message):
		#if log is None:
		#	return
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
		#log.appendPlainText('cut_message_handler: line: %d, func: %s(), file: %s' % (
		#		context.line, context.function, context.file))
		#log.appendPlainText('  %s: %s' % (mode, message))
		logging.debug('  %s: %s\n' % (mode, message))
	logging.basicConfig(filename='session.log',level=logging.DEBUG)
	CuTCore.cuInstallMessageHandler(cut_message_handler)

	app = CuTWidgets.CuApplication(screen, sys.argv)

	mainLayout = CuTWidgets.CuVBoxLayout()

	mw = CuTWidgets.CuMainWindow(name='MW')
	mw.setMaximumSize(180,60)
	mw.setMinimumSize(80,30)

	layout = CuTWidgets.CuHBoxLayout()

	ti1 = CuTestInput(parent=mw, name='Focus 001')
	ti1.setFocusPolicy(CuT.StrongFocus)
	tw1 = addFrame(ti1)
	layout.addWidget(tw1)

	layout.addWidget(addFrame(CuTWidgets.CuScrollBar(parent=mw)))

	vlayout2 = CuTWidgets.CuVBoxLayout()
	ti2 = CuTestInput(parent=mw, name='Wheel Focus 002')
	ti2.setFocusPolicy(CuT.WheelFocus)
	tw2 = addFrame(addFrame(ti2))
	vlayout2.addWidget(tw2)

	ti3 = CuTestInput(parent=mw, name='Disabled Focus')
	ti3.setFocusPolicy(CuT.NoFocus)
	vlayout2.addWidget(ti3)

	lineEdit = CuTWidgets.CuLineEdit(parent=mw)
	lineEdit.setText("Eugenio Parodi 123456789 - abcdefghijklmnopqrstu")
	vlayout2.addWidget(addFrame(lineEdit))

	log = CuTWidgets.CuPlainTextEdit(parent=mw)
	log.setMaximumSize(10000,20)
	log.setMinimumSize(10,20)

	file_in = open('utf-8.txt')
	for line in file_in:
		log.appendPlainText(line.strip())
	file_in.close()

	CuTCore.cuDebug('Test LOG!!!')

	layout.addItem(vlayout2)

	mainLayout.addItem(layout)
	#mainLayout.addWidget(lineEdit)
	mainLayout.addWidget(log)

	mw.setLayout(mainLayout)
	mw.show()

	app.exec_()

CuWrapper.init(main)
