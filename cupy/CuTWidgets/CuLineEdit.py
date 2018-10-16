# -*- coding: utf-8 -*-

from .CuWidget import CuWidget
from CuT.CuTCore import pycutSlot, pycutSignal
from CuT.CuTCore import  CuT, cuDebug
from CuT.CuTHelper import CuWrapper
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuHelper

'''
	http://doc.qt.io/qt-5/qlineedit.html
'''

class CuLineEdit(CuWidget):
	class EchoMode(int): pass
	Normal             = 0 #Display characters as they are entered. This is the default.
	NoEcho             = 1 #Do not display anything. This may be appropriate for passwords where even the length of the password should be kept secret.
	Password           = 2 #Display platform-dependent password mask characters instead of the characters actually entered.
	PasswordEchoOnEdit = 3 #Display characters as they are entered while editing otherwise display characters as with Password.

	class ActionPosition(int): pass
	LeadingPosition  = 0 # The widget is displayed to the left of the text when using layout direction Qt::LeftToRight or to the right when using Qt::RightToLeft, respectively.
	TrailingPosition = 1 # The widget is displayed to the right of the text when using layout direction Qt::LeftToRight or to the left when using Qt::RightToLeft, respectively.

	''' Note of the textline sizes

		LineEdit                 -------------------
		Text                 abcdefghi
		Cursor                     X
		_displayOffset  [4]  <-->
		_cursorPosition [3]  ------>

	'''

	__slots__ = ('_text', '_cursorPosition', '_displayOffset', '_bgColor', '_lastDisplayLen')
	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)
		self._text = u''
		self._cursorPosition = 0
		self._displayOffset  = 0
		self._lastDisplayLen = 0
		self._bgColor = CuT.black
		# Click/Tab focus, no Wheel focus
		self.setFocusPolicy(CuT.StrongFocus)
		self.setMaximumSize(1000000,1)
		self.setMinimumSize(5,1)

	@pycutSlot(str)
	def setText(self, st):
		self._text = st
		self._cursorPosition = len(st)
		self.update()

	@pycutSlot()
	def clear(self):
		self._text = u''
		self.update()

	def enterEvent(self, evt):
		CuHelper.setWidgetColor(self, CuWrapper.WR_COL_BLACK, CuWrapper.WR_COL_BLUE)
		self._bgColor = CuT.blue
		self.update()

	def leaveEvent(self, evt):
		CuHelper.setWidgetColor(self, CuWrapper.WR_COL_BLACK, CuWrapper.WR_COL_BLACK)
		self._bgColor = CuT.black
		self.update()

	def focusInEvent(self, evt):
		# cuDebug("Evt: "+str(evt))
		# CuHelper.enableCursor(CuHelper.replaceCursor)
		cpos = self._cursorPosition - self._displayOffset
		if cpos >= 0 and cpos < self.width():
			CuHelper.enableCursor()
			CuHelper.moveCursor(x=cpos, y=0, widget=self)
		else:
			CuHelper.disableCursor()

	def focusOutEvent(self, evt):
		CuHelper.disableCursor()

	def paintEvent(self, event):
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		qp.setBrush(self._bgColor)
		# Erase the first char after the string (useful in case of delete action)
		newDisplayLen = len(self._text) - self._displayOffset
		if newDisplayLen > self.width():
			newDisplayLen = self.width()
		# cuDebug("W:"+str(self.width())+"  NewDl: "+str(newDisplayLen)+"  lastdl: "+str(self._lastDisplayLen))
		if self._lastDisplayLen > newDisplayLen:			
			qp.eraseRect(newDisplayLen, 0, self._lastDisplayLen - newDisplayLen, 1)
		self._lastDisplayLen = newDisplayLen
		qp.drawText(0, 0, self._text[self._displayOffset:].encode('utf-8'))
		# qp.drawText(20,0,u'£@£¬`漢__あ__'.encode('utf-8'))
		qp.end()

	def mousePressEvent(self, evt):
		x, y = evt.pos()
		x += self._displayOffset
		if x > len(self._text):
			self._cursorPosition = len(self._text)
		else:
			self._cursorPosition = x

	def keyReleaseEvent(self, evt):
		# cuDebug("Key: "+str(evt.key())+"  txt: ->"+evt.text()+"<- len:" + str(len(self._text)))
		if evt.key() == CuT.Key_Backspace:
			if self._cursorPosition > 0:
				c = self._cursorPosition
				pre  = self._text[:c-1]
				post = self._text[c:]
				self._text = pre+post
				self._cursorPosition -= 1
		elif evt.key() == CuT.Key_Delete:
			if self._cursorPosition < len(self._text):
				c = self._cursorPosition+1
				pre  = self._text[:c-1]
				post = self._text[c:]
				self._text = pre+post
		elif evt.key() == CuT.Key_Right:
			if self._cursorPosition < len(self._text):
				self._cursorPosition += 1
		elif evt.key() == CuT.Key_Left:
			if self._cursorPosition > 0:
				self._cursorPosition -= 1
		elif evt.key() == CuT.Key_Home:
			self._cursorPosition = 0
		elif evt.key() == CuT.Key_End:
			self._cursorPosition = len(self._text)
		else:
			c = self._cursorPosition
			pre  = self._text[:c]
			post = self._text[c:]
			self._text = (pre+evt.text()+post)
			self._cursorPosition += 1
			# cuDebug((str(self._cursorPosition)+pre+"<-->"+post+"<---->"+evt.text().decode("utf-8")).encode('utf-8'))
		if self._cursorPosition - self._displayOffset >= self.width() - 1:
			self._displayOffset = self._cursorPosition - self.width() + 1
		if self._cursorPosition - self._displayOffset < 0:
			self._displayOffset = self._cursorPosition
		cpos = self._cursorPosition - self._displayOffset
		if cpos >= 0 and cpos < self.width():
			CuHelper.enableCursor()
			CuHelper.moveCursor(x=cpos, y=0, widget=self)
		else:
			CuHelper.disableCursor()
		self.update()
