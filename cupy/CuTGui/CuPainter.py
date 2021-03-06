
''' CuPainter
        ref: http://doc.qt.io/qt-5/qpainter.html#end
'''

from CuT.CuTCore import  CuT

class CuPainter:
	__slots__ = ('_device','_pen')
	def __init__(self, device=None):
		self._device = device
		self._pen = {'fg':CuT.white, 'bg':CuT.NoBrush}

	def begin(self, device):
		self._device = device

	def end(self):
		pass

	def setBrush(self, color):
		self._pen['bg'] = color

	def setPen(self, color):
		self._pen['fg'] = color
		# if color   == CuT.color0: pass
		# elif color == CuT.color1: pass
		# elif color == CuT.black: pass
		# elif color == CuT.white: pass
		# elif color == CuT.darkGray: pass
		# elif color == CuT.gray: pass
		# elif color == CuT.lightGray: pass
		# elif color == CuT.red: pass
		# elif color == CuT.green: pass
		# elif color == CuT.blue: pass
		# elif color == CuT.cyan: pass
		# elif color == CuT.magenta: pass
		# elif color == CuT.yellow: pass
		# elif color == CuT.darkRed: pass
		# elif color == CuT.darkGreen: pass
		# elif color == CuT.darkBlue: pass
		# elif color == CuT.darkCyan: pass
		# elif color == CuT.darkMagenta: pass
		# elif color == CuT.darkYellow: pass
		# elif color == CuT.transparent: pass

	'''
		void	drawText(const QPointF &position, const QString &text)
		void	drawText(const QPoint &position, const QString &text)
		void	drawText(int x, int y, const QString &text)
		void	drawText(const QRectF &rectangle, int flags, const QString &text, QRectF *boundingRect = nullptr)
		void	drawText(const QRect &rectangle, int flags, const QString &text, QRect *boundingRect = nullptr)
		void	drawText(int x, int y, int width, int height, int flags, const QString &text, QRect *boundingRect = nullptr)
		void	drawText(const QRectF &rectangle, const QString &text, const QTextOption &option = QTextOption())

		@typing.overload
		def drawText(self, p: typing.Union[QtCore.QPointF, QtCore.QPoint], s: str) -> None: ...
		@typing.overload
		def drawText(self, rectangle: QtCore.QRectF, flags: int, text: str) -> QtCore.QRectF: ...
		@typing.overload
		def drawText(self, rectangle: QtCore.QRect, flags: int, text: str) -> QtCore.QRect: ...
		@typing.overload
		def drawText(self, rectangle: QtCore.QRectF, text: str, option: 'QTextOption' = ...) -> None: ...
		@typing.overload
		def drawText(self, p: QtCore.QPoint, s: str) -> None: ...
		@typing.overload
		def drawText(self, x: int, y: int, width: int, height: int, flags: int, text: str) -> QtCore.QRect: ...
		@typing.overload
		def drawText(self, x: int, y: int, s: str) -> None: ...

	'''
	def drawText(self, tx, ty, text):
		self._device.getWin().drawString(tx, ty, text, self._pen['fg'], self._pen['bg'])

	def eraseRect(self, ex, ey, ew, eh):
		self._device.getWin().eraseRect(ex, ey, ew, eh)
