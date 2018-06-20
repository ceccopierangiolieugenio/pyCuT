
''' CuColor
		ref: http://pyqt.sourceforge.net/Docs/PyQt5/api/QtGui/qcolor.html
		ref: https://doc.qt.io/qt-5/qcolor.html
'''
class CuColor:
	def __init__(self, fg = None, bg=None, attr=None):
		self._fg   = fg
		self._bg   = bg
		self._attr = attr
