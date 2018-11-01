from CuT.CuTCore import  CuT
from CuT.CuTCore import pycutSlot, pycutSignal
from CuT.CuTWidgets import CuWidget, CuApplication
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

class CuAbstractSlider(CuWidget):
	class SliderAction(int): pass
	SliderNoAction      = 0
	SliderSingleStepAdd = 1
	SliderSingleStepSub = 2
	SliderPageStepAdd   = 3
	SliderPageStepSub   = 4
	SliderToMinimum     = 5
	SliderToMaximum     = 6
	SliderMove          = 7

	class SliderChange(int): pass
	SliderRangeChange       = 0
	SliderOrientationChange = 1
	SliderStepsChange       = 2
	SliderValueChange       = 3

	__slots__ = (
			# Properties
			'minimum', 'maximum', 'pageStep', 'value', 'position',
			'pressValue', 'singleStep', 'singleStepFromItemView',
			'viewMayChangeSingleStep', 'offset_accumulated', 'tracking',
			'blocktracking', 'pressed', 'invertedAppearance', 'invertedControls',
			'orientation', 'repeatAction', 'isAutoRepeating', 'repeatMultiplier',
			# Signals
			'actionTriggered', 'rangeChanged', 'sliderMoved',
			'sliderPressed', 'sliderReleased', 'valueChanged')

	actionTriggered = pycutSignal(int) # action
	rangeChanged    = pycutSignal(int, int) # min, max
	sliderMoved     = pycutSignal(int) # value
	sliderPressed   = pycutSignal()
	sliderReleased  = pycutSignal()
	valueChanged    = pycutSignal(int) # value

	def __init__(self, *args, **kwargs):
		CuWidget.__init__(self, *args, **kwargs)
		self.minimum            = 0
		self.maximum            = 99
		self.pageStep           = 10
		self.value              = 0
		self.position           = 0
		self.pressValue         = -1
		self.singleStep         = 1
		self.singleStepFromItemView  = -1
		self.viewMayChangeSingleStep = True
		self.offset_accumulated = 0
		self.tracking           = True
		self.blocktracking      = False
		self.pressed            = False
		self.invertedAppearance = False
		self.invertedControls   = False
		self.orientation        = CuT.Horizontal
		self.repeatAction       = CuAbstractSlider.SliderNoAction
		self.isAutoRepeating    = False
		self.repeatMultiplier   = 1
		# self.firstRepeat.invalidate();

	@pycutSlot(int, int)
	def setRange(self, vmin, vmax):
		oldMin = self.minimum
		oldMax = self.maximum
		self.minimum = vmin
		self.maximum = max(vmin, vmax)
		if oldMin != self.minimum or oldMax != self.maximum:
			self.sliderChange(self.SliderRangeChange)
			self.rangeChanged.emit(self.minimum, self.maximum)
			self.setValue(self.value)

	def setSteps(single, page):
		self.singleStep = abs(single)
		self.pageStep = abs(page)
		self.sliderChange(CuAbstractSlider.SliderStepsChange)

	@pycutSlot(CuT.Orientation)
	def setOrientation(self, orientation):
		if self.orientation == orientation:
			return
		self.orientation = orientation
		self.update();
		self.updateGeometry();

	def orientation(self): return self.orientation

	def setMinimum(self, m): self.setRange(m, max(self.maximum, m))
	def setMaximum(self, m): self.setRange(min(self.maximum, m), m)
	def maximum(self): return self.maximum
	def minimum(self): return self.minimum

	def setSingleStep(self, step):
		self.viewMayChangeSingleStep = (step < 0)
		if step < 0 and self.singleStepFromItemView > 0:
			step = self.singleStepFromItemView
		if step != self.singleStep:
			self.setSteps(step, self.pageStep)

	def singleStep(self): return self.singleStep

	def setPageStep(self, step):
		if step != self.pageStep:
			self.setSteps(self.singleStep, step)

	def pageStep(self): return self.pageStep

	def setTracking(self, t):            self.tracking = t

	def hasTracking(self):        return self.tracking

	def setSliderDown(self, down):
		doEmit = self.pressed != down
		self.pressed = down

		if doEmit:
			if down:
				self.sliderPressed.emit()
			else:
			 	self.sliderReleased.emit()

		if not down and self.position != self.value:
			self.triggerAction(self.SliderMove)

	def isSliderDown(self):
		return self.pressed

	def setSliderPosition(self, position):
		position = self._bound(position)
		if position == self.position:
			return
		self.position = position
		if not self.tracking:
			self.update()
		if self.pressed:
			self.sliderMoved.emit(position)
		if self.tracking and not self.blocktracking:
			self.triggerAction(self.SliderMove)

	def sliderPosition(self):
		return self.position

	def value(self):
		return self.value

	@pycutSlot(int)
	def setValue(self, value):
		value = self._bound(value)
		if self.value == value and self.position == value:
			return
		self.value = value
		if self.position != value:
			self.position = value
			if self.pressed:
				self.sliderMoved.emit(value)
		##ifndef QT_NO_ACCESSIBILITY
		#	QAccessibleValueChangeEvent event(this, self.value)
		#	QAccessible::updateAccessibility(&event)
		##endif
		self.sliderChange(self.SliderValueChange)
		self.valueChanged.emit(value)

	def invertedAppearance(self):
		return self.invertedAppearance

	def setInvertedAppearance(self, b):
		self.invertedAppearance = b
		self.update()

	def invertedControls(self):
		return self.invertedControls

	def setInvertedControls(self, b):
		self.invertedControls = b

	def _bound(self, val):
		return max(self.minimum, min(self.maximum, val))

	def _overflowSafeAdd(self, add):
		newValue = self.value + add
		if add > 0 and newValue < self.value:
			newValue = self.maximum;
		elif add < 0 and newValue > self.value:
			newValue = self.minimum;
		return newValue

	def triggerAction(self, action):
		if   action == CuAbstractSlider.SliderSingleStepAdd:
			self.value = self._overflowSafeAdd(self.singleStep)
		elif action == CuAbstractSlider.SliderSingleStepSub:
			self.value = self._overflowSafeAdd(-self.singleStep)
		elif action == CuAbstractSlider.SliderPageStepAdd:
			self.value = self._overflowSafeAdd(self.pageStep)
		elif action == CuAbstractSlider.SliderPageStepSub:
			self.value = self._overflowSafeAdd(-self.pageStep)
		elif action == CuAbstractSlider.SliderToMinimum:
			self.value = self.minimum
		elif action == CuAbstractSlider.SliderToMaximum:
			self.value = self.maximum
		elif action == CuAbstractSlider.SliderMove: pass
		elif action == CuAbstractSlider.SliderNoAction: pass
		else:
			error = "action: "+str(action)+" not recognized"
			raise TypeError(error)
		self.actionTriggered.emit(action)

	# TODO:
	# void QAbstractSlider::setRepeatAction(SliderAction action, int thresholdTime, int repeatTime)
	# QAbstractSlider::SliderAction QAbstractSlider::repeatAction() const
	# void QAbstractSlider::timerEvent(QTimerEvent *e)

	# Private "QAbstractSliderPrivate" #
	def effectiveSingleStep(self):
		return self.singleStep * self.repeatMultiplier

	def sliderChange(self, sc):
		self.update()


	def scrollByDelta(self, orientation, modifiers, delta):
		def qBound(minv, val, maxv):
			return max(minv, min(maxv, val))

		stepsToScroll = 0
		# in Qt scrolling to the right gives negative values.
		if orientation == CuT.Horizontal:
			delta = -delta
		offset = delta / 120
	
		if (modifiers & CuT.ControlModifier) or (modifiers & CuT.ShiftModifier):
			# Scroll one page regardless of delta:
			stepsToScroll = qBound(-self.pageStep, int(offset * self.pageStep), self.pageStep)
			self.offset_accumulated = 0
		else:
			# Calculate how many lines to scroll. Depending on what delta is (and
			# offset), we might end up with a fraction (e.g. scroll 1.3 lines). We can
			# only scroll whole lines, so we keep the reminder until next event.
			stepsToScrollF = CuApplication.wheelScrollLines() * offset * self.effectiveSingleStep()
			# Check if wheel changed direction since last event:
			if self.offset_accumulated != 0 and (offset / self.offset_accumulated) < 0:
				self.offset_accumulated = 0
	
			self.offset_accumulated += stepsToScrollF
			stepsToScroll = qBound(-self.pageStep, int(self.offset_accumulated), self.pageStep)
			self.offset_accumulated -= int(self.offset_accumulated)
			if stepsToScroll == 0:
				# We moved less than a line, but might still have accumulated partial scroll,
				# unless we already are at one of the ends.
				if self.invertedControls:
					effective_offset = -self.offset_accumulated
				else:
					effective_offset = self.offset_accumulated

				if effective_offset > 0 and self.value < self.maximum:
					return True
				if effective_offset < 0 and self.value > self.minimum:
					return True

				self.offset_accumulated = 0
				return False
	
		if self.invertedControls:
			stepsToScroll = -stepsToScroll
	
		prevValue = self.value
		position = self._bound(self._overflowSafeAdd(stepsToScroll)); # value will be updated by triggerAction()
		self.triggerAction(CuAbstractSlider.SliderMove)
	
		if prevValue == self.value :
			self.offset_accumulated = 0
			return False
		return True


	def wheelEvent(self, e):
		e.ignore()
		delta = e.angleDelta()
		if e.inverted():
			delta = -delta
		# guess orientation
		orientation = CuT.Horizontal if abs(delta.x()) > abs(delta.y()) else CuT.Vertical
		if self.scrollByDelta(
				orientation, e.modifiers(), 
				delta.x() if orientation == CuT.Horizontal else delta.y()):
		#if self.scrollByDelta(e.orientation(), e.modifiers(), delta):
			e.accept()


	def keyPressEvent(self, ev):
		action = self.SliderNoAction
		if ev.key() == CuT.Key_Select:
			if QApplication.keypadNavigationEnabled():
				self.setEditFocus(not self.hasEditFocus())
			else:
				ev.ignore()
		elif ev.key() == CuT.Key_Back:
			if (CuApplication.keypadNavigationEnabled() and self.hasEditFocus()):
				self.setValue(self.origValue)
				self.setEditFocus(False)
			else:
				ev.ignore()

		# It seems we need to use invertedAppearance for Left and right, otherwise, things look weird.
		elif ev.key() == CuT.Key_Left:
			# In QApplication::KeypadNavigationDirectional, we want to change the slider
			# value if there is no left/right navigation possible and if this slider is not
			# inside a tab widget.
			if (CuApplication.keypadNavigationEnabled()
					and (not hasEditFocus()and CuApplication.navigationMode() == CuT.NavigationModeKeypadTabOrder
					or self.orientation == CuT.Vertical
					or not self.hasEditFocus()
					and (CuWidgetPrivate.canKeypadNavigate(CuT.Horizontal) or CuWidgetPrivate.inTabWidget(self)))):
				ev.ignore()
				return

			if CuApplication.keypadNavigationEnabled() and self.orientation == CuT.Vertical:
				action = self.SliderSingleStepSub if self.invertedControls else self.SliderSingleStepAdd
			elif isRightToLeft():
				action = self.SliderSingleStepSub if self.invertedAppearance else self.SliderSingleStepAdd
			else:
				action = self.SliderSingleStepSub if not self.invertedAppearance else self.SliderSingleStepAdd
		elif ev.key() == CuT.Key_Right:
			#ifdef QT_KEYPAD_NAVIGATION
			# Same logic as in CuT.Key_Left
			if (CuApplication.keypadNavigationEnabled()
					and (not self.hasEditFocus() and CuApplication.navigationMode() == CuT.NavigationModeKeypadTabOrder
					or self.orientation == CuT.Vertical
					or not self.hasEditFocus()
					and (CuWidgetPrivate.canKeypadNavigate(CuT.Horizontal) or CuWidgetPrivate.inTabWidget(self)))):
				ev.ignore()
				return

			if CuApplication.keypadNavigationEnabled() and self.orientation == CuT.Vertical:
				action = self.SliderSingleStepAdd if self.invertedControls else self.SliderSingleStepSub
			elif isRightToLeft():
				action = self.SliderSingleStepAdd if self.invertedAppearance else self.SliderSingleStepSub
			else:
				action = self.SliderSingleStepAdd if not self.invertedAppearance else self.SliderSingleStepSub
		elif ev.key() == CuT.Key_Up:
			#ifdef QT_KEYPAD_NAVIGATION
			# In QApplication::KeypadNavigationDirectional, we want to change the slider
			# value if there is no up/down navigation possible.
			if (CuApplication.keypadNavigationEnabled()
					and (CuApplication.navigationMode() == CuT.NavigationModeKeypadTabOrder
					or self.orientation == CuT.Horizontal
					or not self.hasEditFocus() and CuWidgetPrivate.canKeypadNavigate(CuT.Vertical))):
				ev.ignore()
			else:
				#endif
				action = self.SliderSingleStepSub if self.invertedControls else self.SliderSingleStepAdd
		elif ev.key() == CuT.Key_Down:
			#ifdef QT_KEYPAD_NAVIGATION
			# Same logic as in CuT.Key_Up
			if (CuApplication.keypadNavigationEnabled()
					and (CuApplication.navigationMode() == CuT.NavigationModeKeypadTabOrder
					or self.orientation == CuT.Horizontal
					or not self.hasEditFocus() and CuWidgetPrivate.canKeypadNavigate(CuT.Vertical))):
				ev.ignore()
			else:
			#endif
				action = self.SliderSingleStepAdd if self.invertedControls else self.SliderSingleStepSub
		elif ev.key() == CuT.Key_PageUp:
			action = self.SliderPageStepSub if self.invertedControls else self.SliderPageStepAdd
		elif ev.key() == CuT.Key_PageDown:
			action = self.SliderPageStepAdd if self.invertedControls else self.SliderPageStepSub
		elif ev.key() == CuT.Key_Home:
			action = self.SliderToMinimum
		elif ev.key() == CuT.Key_End:
			action = self.SliderToMaximum
		else:
			ev.ignore()

		if action != self.SliderNoAction:
			triggerAction(action)
