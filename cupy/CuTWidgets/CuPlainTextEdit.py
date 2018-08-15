from .CuWidget import CuWidget
from .CuFrame import CuFrame
from CuT.CuTCore import pycutSlot, pycutSignal

'''
	http://doc.qt.io/qt-5/qframe.html
'''

class CuAbstractScrollArea(CuFrame):
	pass

class CuPlainTextEdit(CuAbstractScrollArea):
	@pycutSlot(str)
	def appendPlainText(self, str):
		pass
