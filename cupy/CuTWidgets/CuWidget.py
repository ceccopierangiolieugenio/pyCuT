'''
    Widget
'''

import os

from CuT.CuTHelper import CuWrapper, CuHelper
from CuT.CuTCore import pycutSlot, pycutSignal
from CuT.CuTCore import CuT, CuEvent, CuMouseEvent, CuFocusEvent, CuPoint, CuSize
from .CuLayout import *
from .CuApplication import *



class CuWidget:
	__slots__ = ('_data', '_extra')
	def __init__(self, *args, **kwargs):
		if not CuHelper.app_initialized():
			# Abort:
			#  i.e.
			#    QWidget: Must construct a QApplication before a QWidget
			print(self.__class__.__name__ + ": Must construct a CuApplication before a CuWidget")
			os.abort()

		self._extra = {
				'maxw' : 100000,
				'maxh' : 100000,
				'minw' : 0,
				'minh' : 0,
			}
		self._data = {}

		self._data['parent'] = kwargs.get('parent', None )
		self._data['name'] = kwargs.get('name', '')
		self._data['pos'] = CuPoint(kwargs.get('x', 0), kwargs.get('y', 0))
		self._data['size'] = CuSize(kwargs.get('w', CuHelper.getW()), kwargs.get('h', CuHelper.getH()))


		if self._data['parent'] is None:
			CuHelper.setMainWidget(self)

		self._data['childs'] = []
		self._data['win'] = CuWrapper.newWin(self, self._data['pos'].x(), self._data['pos'].y(), self._data['size'].width(), self._data['size'].height())
		self._data['layout'] = None
		self._data['mouse'] = {'underMouse':False}
		self._data['focus'] = False
		self._data['focus_policy'] = CuT.NoFocus
		self.hide()

	def accessibleName(self):
		return self._data['name']

	def setAccessibleName(self, name):
		self._data['name'] = name

	def getWin(self):
		return self._data['win']

	def paintEvent(self, event): pass

	def underMouse(self):
		return self._data['mouse']['underMouse']

	def mouseDoubleClickEvent(self, evt): pass
	def mouseMoveEvent(self, evt): pass
	def mousePressEvent(self, evt): pass
	def mouseReleaseEvent(self, evt): pass
	def wheelEvent(self, evt): pass
	def enterEvent(self, evt): pass
	def leaveEvent(self, evt): pass
	def keyPressEvent(self, evt): pass
	def keyReleaseEvent(self, evt): pass

	@staticmethod
	def _broadcastLeaveEvent(evt, layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				if item.widget()._data['mouse']['underMouse']:
					item.widget()._data['mouse']['underMouse'] = False
					item.widget().leaveEvent(evt)
			elif isinstance(item, CuLayout):
				CuWidget._broadcastLeaveEvent(evt, item)

	@staticmethod
	def _eventLayoutHandle(evt, layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				widget = item.widget()
				wevt = None
				mouseEvent = False
				if isinstance(evt, CuMouseEvent):
					mouseEvent = True
					wpos = CuHelper.absPos(widget)
					wsize = widget.size()
					ewpos = evt.windowPos()
					espos = evt.screenPos()
					lpos = espos-wpos
					# Skip the mouse event if outside this widget
					# TODO: Use CuRect instead
					if lpos.x() >= 0 and lpos.y() >= 0 and lpos.x() < wsize.width() and lpos.y() < wsize.height():
						# ex,  ey  = evt.pos()
						wevt = CuMouseEvent(
							type=evt.type(),
							localPos  = lpos,
							windowPos = ewpos,
							screenPos = espos,
							button = evt.button())
				if isinstance(evt, CuWheelEvent):
					mouseEvent = True
					wpos = CuHelper.absPos(widget)
					wsize = widget.size()
					egpos = evt.globalPos()
					lpos = egpos-wpos
					# Skip the mouse event if outside this widget
					# TODO: Use CuRect instead
					if lpos.x() >= 0 and lpos.y() >= 0 and lpos.x() < wsize.width() and lpos.y() < wsize.height():
						wevt = CuWheelEvent(
							type=evt.type(),
							pos  = lpos,
							globalPos = egpos,
							angleDelta=evt.angleDelta())
				if mouseEvent:
					if wevt is not None:
						if not widget._data['mouse']['underMouse']:
							widget._data['mouse']['underMouse'] = True
							widget.enterEvent(wevt)
						if widget.event(wevt):
							return True
					else:
						if widget._data['mouse']['underMouse']:
							widget._data['mouse']['underMouse'] = False
							widget.leaveEvent(evt)
						if widget._data['layout'] is not None:
							CuWidget._broadcastLeaveEvent(evt, widget._data['layout'])
					continue

				if widget.event(evt):
					return True
			elif isinstance(item, CuLayout):
				if CuWidget._eventLayoutHandle(evt, item):
					return True
		return False

	def event(self, evt):
		# handle own events
		if evt.type() == CuEvent.MouseMove:
			if evt.button() == CuT.NoButton:
				self.mouseMoveEvent(evt)
		elif   evt.type() == CuEvent.MouseButtonRelease:
			self.mouseReleaseEvent(evt)
		elif evt.type() == CuEvent.MouseButtonPress:
			self.mousePressEvent(evt)
			if self.focusPolicy() & CuT.ClickFocus == CuT.ClickFocus:
				self.setFocus()
		elif evt.type() == CuEvent.Wheel:
			self.wheelEvent(evt)
			if self.focusPolicy() & CuT.WheelFocus == CuT.WheelFocus:
				self.setFocus()
		elif evt.type() == CuEvent.KeyPress:
			self.keyPressEvent(evt)
		elif evt.type() == CuEvent.KeyRelease:
			self.keyReleaseEvent(evt)
		# Trigger this event to the childs
		if self._data['layout'] is not None:
			return CuWidget._eventLayoutHandle(evt, self._data['layout'])


	def setLayout(self, layout):
		if isinstance(layout, CuLayout):
			self._data['layout'] = layout
			self._data['layout'].setParent(self)
			self._data['layout'].setGeometry(0, 0, self.width(), self.height())
			self._data['layout'].update()
		else:
			raise Exception(str(layout) + ' not of type CuLayout')

	def layout(self): return self._data['layout']

	def setParent(self, parent):
		self._data['parent'] = parent
	def parentWidget(self):
		return self._data['parent']

	def x(self): return self._data['pos'].x()
	def y(self): return self._data['pos'].y()
	def width(self):  return self._data['size'].width()
	def height(self): return self._data['size'].height()

	def pos(self): return self._data['pos']
	def size(self):   return self._data['size']

	def maximumSize(self):
		return self.maximumWidth(), self.maximumHeight()
	def maximumHeight(self):
		wMaxH = self._extra['maxh']
		lMaxH = 1000000
		if self._data['layout'] is not None:
			lMaxH = self._data['layout'].maximumHeight()
			if lMaxH < wMaxH:
				return lMaxH
		return wMaxH
	def maximumWidth(self):
		wMaxW = self._extra['maxw']
		lMaxW = 1000000
		if self._data['layout'] is not None:
			lMaxW = self._data['layout'].maximumWidth()
			if lMaxW < wMaxW:
				return lMaxW
		return wMaxW

	def minimumSize(self):
		return self.minimumWidth(), self.minimumHeight()
	def minimumHeight(self):
		wMinH = self._extra['minh']
		lMinH = 1000000
		if self._data['layout'] is not None:
			lMinH = self._data['layout'].minimumHeight()
			if lMinH > wMinH:
				return lMinH
		return wMinH
	def minimumWidth(self):
		wMinW = self._extra['minw']
		lMinW = 1000000
		if self._data['layout'] is not None:
			lMinW = self._data['layout'].minimumWidth()
			if lMinW > wMinW:
				return lMinW
		return wMinW

	def setMaximumSize(self, maxw, maxh): self._extra['maxw'] = maxw; self._extra['maxh'] = maxh
	def setMaximumHeight(self, maxh):     self._extra['maxh'] = maxh
	def setMaximumWidth(self, maxw):      self._extra['maxw'] = maxw

	def setMinimumSize(self, minw, minh): self._extra['minw'] = minw; self._extra['minh'] = minh
	def setMinimumHeight(self, minh):     self._extra['minh'] = minh
	def setMinimumWidth(self, minw):      self._extra['minw'] = minw

	def move(self, x, y):
		self._data['pos'].setX(x)
		self._data['pos'].setY(y)
		self._data['win'].move(self._data['pos'].x(), self._data['pos'].y())
		if self._data['layout'] is not None:
			self._data['layout'].setGeometry(self._data['pos'].x(), self._data['pos'].y(), self._data['size'].width(), self._data['size'].height())
		self.update()

	def resize(self, w, h):
		self._data['size'].setWidth(w)
		self._data['size'].setHeight(h)
		self._data['win'].resize(self._data['size'].width(), self._data['size'].height())
		if self._data['layout'] is not None:
			self._data['layout'].setGeometry(self._data['pos'].x(), self._data['pos'].y(), self._data['size'].width(), self._data['size'].height())
		self.update()

	def setGeometry(self, x, y, w, h):
		self.resize(w, h)
		self.move(x, y)

	@staticmethod
	def _showHandle(layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				item.widget().show()
			elif isinstance(item, CuLayout):
				CuWidget._showHandle(item)

	def show(self):
		self._data['win'].show()
		self._data['visible'] = True
		if self._data['layout'] is not None:
			CuWidget._showHandle(self._data['layout'])

	@staticmethod
	def _hideHandle(layout):
		for i in range(layout.count()):
			item = layout.itemAt(i)
			if isinstance(item, CuWidgetItem) and not item.isEmpty():
				item.widget().hide()
			elif isinstance(item, CuLayout):
				CuWidget._hideHandle(item)

	def hide(self):
		self._data['win'].hide()
		self._data['visible'] = False
		if self._data['layout'] is not None:
			CuWidget._hideHandle(self._data['layout'])

	def isVisible(self):
		return self._data['visible']

	def update(self):
		CuHelper.addUpdateWidget(self)
		if self._data['layout'] is not None:
			self._data['layout'].update()

	'''
		Focus Logic
		ref: http://doc.qt.io/qt-5/qwidget.html

		properties:
			focus : const bool
			focusPolicy : Qt::FocusPolicy

		Public Functions:
			void             clearFocus()

			Qt::FocusPolicy  focusPolicy() const
			QWidget *        focusProxy() const
			QWidget *        focusWidget() const

			bool             hasEditFocus() const
			bool             hasFocus() const

			QWidget *        nextInFocusChain() const
			QWidget *        previousInFocusChain() const

			void             setEditFocus(bool enable)
			void             setFocus(Qt::FocusReason reason)
			void             setFocusPolicy(Qt::FocusPolicy policy)
			void             setFocusProxy(QWidget *w)

		Public Slots:
			void             setFocus()

		Protected Functions:
			virtual void     focusInEvent(QFocusEvent *event)
			bool             focusNextChild()
			virtual bool     focusNextPrevChild(bool next)
			virtual void     focusOutEvent(QFocusEvent *event)
			bool             focusPreviousChild()

		Protected Slots:
			void             updateMicroFocus()
	'''

	@pycutSlot()
	def setFocus(self, reason=CuT.OtherFocusReason):
		tmp = CuHelper.getFocus()
		if tmp is not None:
			tmp.clearFocus()
			tmp.focusOutEvent(
					CuFocusEvent(
						type=CuEvent.FocusOut,
						reason=reason))
			tmp.update()
		CuHelper.setFocus(self)
		self._data['focus'] = True
		self.focusInEvent(
				CuFocusEvent(
					type=CuEvent.FocusIn,
					reason=reason))

	def clearFocus(self):
		CuHelper.clearFocus()
		self._data['focus'] = False

	def focusPolicy(self):
		return self._data['focus_policy']

	def focusProxy(self):   pass
	def focusWidget(self):  pass
	def hasEditFocus(self): pass
	def hasFocus(self):
		return self._data['focus']

	def setEditFocus(self, enable): pass

	#def setFocus(self, reason):
	#	pass

	def setFocusPolicy(self, policy):
		self._data['focus_policy'] = policy

	def setFocusProxy(self, w): pass

	def focusInEvent(self, evt): pass
	def focusOutEvent(self, evt): pass
