from .CuWidget import CuWidget
from .CuFrame import CuFrame
from CuT.CuTCore import pycutSlot, pycutSignal
from CuT.CuTCore import  CuT
from CuT.CuTHelper import CuWrapper
from CuT.CuTGui import CuPainter
from CuT.CuTWidgets import CuHBoxLayout


'''
	http://doc.qt.io/qt-5/qframe.html
'''

class CuAbstractScrollArea(CuFrame):
	pass

class CuPlainTextEdit(CuAbstractScrollArea):
	class _TextArea(CuWidget):
		__slots__ = ('_textLines','_maxTextLines','_scrollLine','_drawWidth')
		def __init__(self, *args, **kwargs):
			self._textLines = []
			self._maxTextLines = 500
			self._scrollLine = 0
			self._drawWidth = 0
			CuWidget.__init__(self, *args, **kwargs)

		def paintEvent(self, event):
			qp = CuPainter()
			qp.begin(self)
			qp.setPen(CuT.white)
			drawWidth = self._drawWidth
			self._drawWidth = 0
			i = self._scrollLine
			while i < len(self._textLines):
				strlen = len(self._textLines[i])
				qp.drawText(1, i - self._scrollLine, self._textLines[i].ljust(drawWidth))
				if self._drawWidth < strlen:
					self._drawWidth = strlen
				i+=1
			qp.end()

		@pycutSlot(str)
		def appendPlainText(self, str):
			self._textLines.append(str)
			if len(self._textLines) > self.height():
				self._scrollLine = len(self._textLines) - self.height()
			self.update()

	__slots__ = ('_textArea','_layout')

	def __init__(self, *args, **kwargs):
		CuAbstractScrollArea.__init__(self, *args, **kwargs)
		self._textArea = self._TextArea(parent=self)
		self._layout = CuHBoxLayout()
		self._layout.addWidget(self._textArea)
		self.setLayout(self._layout)

	@pycutSlot(str)
	def appendPlainText(self, str):
		self._textArea.appendPlainText(str)
