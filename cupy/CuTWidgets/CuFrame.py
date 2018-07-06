from .CuWidget import CuWidget
from .CuLayout import CuLayout

'''
	http://doc.qt.io/qt-5/qframe.html
'''
class CuFrame(CuWidget):
	Plain = 0x0010 #the frame and contents appear level with the surroundings; draws using the palette QPalette::WindowText color (without any 3D effect)
	Raised = 0x0020 #the frame and contents appear raised; draws a 3D raised line using the light and dark colors of the current color group
	Sunken = 0x0030 #the frame and contents appear sunken; draws a 3D sunken line using the light and dark colors of the current color group

	NoFrame = 0 #QFrame draws nothing
	Box = 0x0001 #QFrame draws a box around its contents
	Panel = 0x0002 #QFrame draws a panel to make the contents appear raised or sunken
	StyledPanel = 0x0006 #draws a rectangular panel with a look that depends on the current GUI style. It can be raised or sunken.
	HLine = 0x0004 #QFrame draws a horizontal line that frames nothing (useful as separator)
	VLine = 0x0005 #QFrame draws a vertical line that frames nothing (useful as separator)
	WinPanel = 0x0003 #draws a rectangular panel that can be raised or sunken like those in Windows 2000. Specifying this shape sets the line width to 2 pixels. WinPanel is provided for compatibility. For GUI style independence we recommend using StyledPanel instead.

	def __init__(self, *args, **kwargs):
		self._lineWidth = 1
		CuWidget.__init__(self, *args, **kwargs)
		self._data['win'].box()

	
	def lineWidth(self):
		return self._lineWidth

	def setLineWidth(self, w):
		self._lineWidth = w
		if w == 0:
			self._data['win'].clear()
		elif w > 0:
			self._data['win'].box()

	def setLayout(self, layout):
		if isinstance(layout, CuLayout):
			lw = self._lineWidth
			CuWidget.setLayout(self, layout)
			self.layout().setGeometry(
									self.x()+lw, self.y()+lw,
									self.width()-2*lw, self.height()-2*lw )
			self.layout().update()
		else:
			raise Exception(str(layout) + ' not of type CuLayout')

	def maximumHeight(self):
		return CuWidget.maximumHeight(self) + 2*self._lineWidth
	def maximumWidth(self):
		return CuWidget.maximumWidth(self) + 2*self._lineWidth
	def minimumHeight(self):
		return CuWidget.minimumHeight(self) + 2*self._lineWidth
	def minimumWidth(self):
		return CuWidget.minimumWidth(self) + 2*self._lineWidth

	def resize(self, w, h):
		CuWidget.resize(self, w, h)
		if self.layout() is not None:
			lw = self._lineWidth
			self.layout().setGeometry(
									self.x()+lw, self.y()+lw,
									self.width()-2*lw, self.height()-2*lw )
		if self._lineWidth > 0:
			self._data['win'].box()

	def setGeometry(self, x, y, w, h):
		CuWidget.setGeometry(self, x, y, w, h)
		if self.layout() is not None:
			lw = self._lineWidth
			self.layout().setGeometry(
									self.x()+lw, self.y()+lw,
									self.width()-2*lw, self.height()-2*lw )
			self.layout().update()
		if self._lineWidth > 0:
			self._data['win'].box()

class CuMainWindow(CuFrame):
	def __init__(self, *args, **kwargs):
		CuFrame.__init__(self, *args, **kwargs)