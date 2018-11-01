'''
    Event
'''

from .CuT import CuT, CuPoint

class CuEvent:
	'''
		enum QEvent::Type
		http://doc.qt.io/qt-5/qevent.html#Type-enum
	'''
	class Type(int): pass
	# None                           = 0     # Not an event.
	ActionAdded                      = 114   # A new action has been added (QActionEvent).
	ActionChanged                    = 113   # An action has been changed (QActionEvent).
	ActionRemoved                    = 115   # An action has been removed (QActionEvent).
	ActivationChange                 = 99    # A widget's top-level window activation state has changed.
	ApplicationActivate              = 121   # This enum has been deprecated. Use ApplicationStateChange instead.
	ApplicationActivated             = ApplicationActivate   # This enum has been deprecated. Use ApplicationStateChange instead.
	ApplicationDeactivate            = 122   # This enum has been deprecated. Use ApplicationStateChange instead.
	ApplicationFontChange            = 36    # The default application font has changed.
	ApplicationLayoutDirectionChange = 37    # The default application layout direction has changed.
	ApplicationPaletteChange         = 38    # The default application palette has changed.
	ApplicationStateChange           = 214   # The state of the application has changed.
	ApplicationWindowIconChange      = 35    # The application's icon has changed.
	ChildAdded                       = 68    # An object gets a child (QChildEvent).
	ChildPolished                    = 69    # A widget child gets polished (QChildEvent).
	ChildRemoved                     = 71    # An object loses a child (QChildEvent).
	Clipboard                        = 40    # The clipboard contents have changed.
	Close                            = 19    # Widget was closed (QCloseEvent).
	CloseSoftwareInputPanel          = 200   # A widget wants to close the software input panel (SIP).
	ContentsRectChange               = 178   # The margins of the widget's content rect changed.
	ContextMenu                      = 82    # Context popup menu (QContextMenuEvent).
	CursorChange                     = 183   # The widget's cursor has changed.
	DeferredDelete                   = 52    # The object will be deleted after it has cleaned up (QDeferredDeleteEvent)
	DragEnter                        = 60    # The cursor enters a widget during a drag and drop operation (QDragEnterEvent).
	DragLeave                        = 62    # The cursor leaves a widget during a drag and drop operation (QDragLeaveEvent).
	DragMove                         = 61    # A drag and drop operation is in progress (QDragMoveEvent).
	Drop                             = 63    # A drag and drop operation is completed (QDropEvent).
	DynamicPropertyChange            = 170   # A dynamic property was added, changed, or removed from the object.
	EnabledChange                    = 98    # Widget's enabled state has changed.
	Enter                            = 10    # Mouse enters widget's boundaries (QEnterEvent).
	EnterEditFocus                   = 150   # An editor widget gains focus for editing. QT_KEYPAD_NAVIGATION must be defined.
	EnterWhatsThisMode               = 124   # Send to toplevel widgets when the application enters "What's This?" mode.
	Expose                           = 206   # Sent to a window when its on-screen contents are invalidated and need to be flushed from the backing store.
	FileOpen                         = 116   # File open request (QFileOpenEvent).
	FocusIn                          = 8     # Widget or Window gains keyboard focus (QFocusEvent).
	FocusOut                         = 9     # Widget or Window loses keyboard focus (QFocusEvent).
	FocusAboutToChange               = 23    # Widget or Window focus is about to change (QFocusEvent)
	FontChange                       = 97    # Widget's font has changed.
	Gesture                          = 198   # A gesture was triggered (QGestureEvent).
	GestureOverride                  = 202   # A gesture override was triggered (QGestureEvent).
	GrabKeyboard                     = 188   # Item gains keyboard grab (QGraphicsItem only).
	GrabMouse                        = 186   # Item gains mouse grab (QGraphicsItem only).
	GraphicsSceneContextMenu         = 159   # Context popup menu over a graphics scene (QGraphicsSceneContextMenuEvent).
	GraphicsSceneDragEnter           = 164   # The cursor enters a graphics scene during a drag and drop operation (QGraphicsSceneDragDropEvent).
	GraphicsSceneDragLeave           = 166   # The cursor leaves a graphics scene during a drag and drop operation (QGraphicsSceneDragDropEvent).
	GraphicsSceneDragMove            = 165   # A drag and drop operation is in progress over a scene (QGraphicsSceneDragDropEvent).
	GraphicsSceneDrop                = 167   # A drag and drop operation is completed over a scene (QGraphicsSceneDragDropEvent).
	GraphicsSceneHelp                = 163   # The user requests help for a graphics scene (QHelpEvent).
	GraphicsSceneHoverEnter          = 160   # The mouse cursor enters a hover item in a graphics scene (QGraphicsSceneHoverEvent).
	GraphicsSceneHoverLeave          = 162   # The mouse cursor leaves a hover item in a graphics scene (QGraphicsSceneHoverEvent).
	GraphicsSceneHoverMove           = 161   # The mouse cursor moves inside a hover item in a graphics scene (QGraphicsSceneHoverEvent).
	GraphicsSceneMouseDoubleClick    = 158   # Mouse press again (double click) in a graphics scene (QGraphicsSceneMouseEvent).
	GraphicsSceneMouseMove           = 155   # Move mouse in a graphics scene (QGraphicsSceneMouseEvent).
	GraphicsSceneMousePress          = 156   # Mouse press in a graphics scene (QGraphicsSceneMouseEvent).
	GraphicsSceneMouseRelease        = 157   # Mouse release in a graphics scene (QGraphicsSceneMouseEvent).
	GraphicsSceneMove                = 182   # Widget was moved (QGraphicsSceneMoveEvent).
	GraphicsSceneResize              = 181   # Widget was resized (QGraphicsSceneResizeEvent).
	GraphicsSceneWheel               = 168   # Mouse wheel rolled in a graphics scene (QGraphicsSceneWheelEvent).
	Hide                             = 18    # Widget was hidden (QHideEvent).
	HideToParent                     = 27    # A child widget has been hidden.
	HoverEnter                       = 127   # The mouse cursor enters a hover widget (QHoverEvent).
	HoverLeave                       = 128   # The mouse cursor leaves a hover widget (QHoverEvent).
	HoverMove                        = 129   # The mouse cursor moves inside a hover widget (QHoverEvent).
	IconDrag                         = 96    # The main icon of a window has been dragged away (QIconDragEvent).
	IconTextChange                   = 101   # Widget's icon text has been changed. (Deprecated)
	InputMethod                      = 83    # An input method is being used (QInputMethodEvent).
	InputMethodQuery                 = 207   # A input method query event (QInputMethodQueryEvent)
	KeyboardLayoutChange             = 169   # The keyboard layout has changed.
	KeyPress                         = 6     # Key press (QKeyEvent).
	KeyRelease                       = 7     # Key release (QKeyEvent).
	LanguageChange                   = 89    # The application translation changed.
	LayoutDirectionChange            = 90    # The direction of layouts changed.
	LayoutRequest                    = 76    # Widget layout needs to be redone.
	Leave                            = 11    # Mouse leaves widget's boundaries.
	LeaveEditFocus                   = 151   # An editor widget loses focus for editing. QT_KEYPAD_NAVIGATION must be defined.
	LeaveWhatsThisMode               = 125   # Send to toplevel widgets when the application leaves "What's This?" mode.
	LocaleChange                     = 88    # The system locale has changed.
	NonClientAreaMouseButtonDblClick = 176   # A mouse double click occurred outside the client area (QMouseEvent).
	NonClientAreaMouseButtonPress    = 174   # A mouse button press occurred outside the client area (QMouseEvent).
	NonClientAreaMouseButtonRelease  = 175   # A mouse button release occurred outside the client area (QMouseEvent).
	NonClientAreaMouseMove           = 173   # A mouse move occurred outside the client area (QMouseEvent).
	MacSizeChange                    = 177   # The user changed his widget sizes (macOS only).
	MetaCall                         = 43    # An asynchronous method invocation via QMetaObject::invokeMethod().
	ModifiedChange                   = 102   # Widgets modification state has been changed.
	MouseButtonDblClick              = 4     # Mouse press again (QMouseEvent).
	MouseButtonPress                 = 2     # Mouse press (QMouseEvent).
	MouseButtonRelease               = 3     # Mouse release (QMouseEvent).
	MouseMove                        = 5     # Mouse move (QMouseEvent).
	MouseTrackingChange              = 109   # The mouse tracking state has changed.
	Move                             = 13    # Widget's position changed (QMoveEvent).
	NativeGesture                    = 197   # The system has detected a gesture (QNativeGestureEvent).
	OrientationChange                = 208   # The screens orientation has changes (QScreenOrientationChangeEvent).
	Paint                            = 12    # Screen update necessary (QPaintEvent).
	PaletteChange                    = 39    # Palette of the widget changed.
	ParentAboutToChange              = 131   # The widget parent is about to change.
	ParentChange                     = 21    # The widget parent has changed.
	PlatformPanel                    = 212   # A platform specific panel has been requested.
	PlatformSurface                  = 217   # A native platform surface has been created or is about to be destroyed (QPlatformSurfaceEvent).
	Polish                           = 75    # The widget is polished.
	PolishRequest                    = 74    # The widget should be polished.
	QueryWhatsThis                   = 123   # The widget should accept the event if it has "What's This?" help (QHelpEvent).
	ReadOnlyChange                   = 106   # Widget's read-only state has changed (since Qt 5.4).
	RequestSoftwareInputPanel        = 199   # A widget wants to open a software input panel (SIP).
	Resize                           = 14    # Widget's size changed (QResizeEvent).
	ScrollPrepare                    = 204   # The object needs to fill in its geometry information (QScrollPrepareEvent).
	Scroll                           = 205   # The object needs to scroll to the supplied position (QScrollEvent).
	Shortcut                         = 117   # Key press in child for shortcut key handling (QShortcutEvent).
	ShortcutOverride                 = 51    # Key press in child, for overriding shortcut key handling (QKeyEvent).
	Show                             = 17    # Widget was shown on screen (QShowEvent).
	ShowToParent                     = 26    # A child widget has been shown.
	SockAct                          = 50    # Socket activated, used to implement QSocketNotifier.
	StateMachineSignal               = 192   # A signal delivered to a state machine (QStateMachine::SignalEvent).
	StateMachineWrapped              = 193   # The event is a wrapper for, i.e., contains, another event (QStateMachine::WrappedEvent).
	StatusTip                        = 112   # A status tip is requested (QStatusTipEvent).
	StyleChange                      = 100   # Widget's style has been changed.
	TabletMove                       = 87    # Wacom tablet move (QTabletEvent).
	TabletPress                      = 92    # Wacom tablet press (QTabletEvent).
	TabletRelease                    = 93    # Wacom tablet release (QTabletEvent).
	TabletEnterProximity             = 171   # Wacom tablet enter proximity event (QTabletEvent), sent to QApplication.
	TabletLeaveProximity             = 172   # Wacom tablet leave proximity event (QTabletEvent), sent to QApplication.
	TabletTrackingChange             = 219   # The Wacom tablet tracking state has changed (since Qt 5.9).
	ThreadChange                     = 22    # The object is moved to another thread. This is the last event sent to this object in the previous thread. See QObject::moveToThread().
	Timer                            = 1     # Regular timer events (QTimerEvent).
	ToolBarChange                    = 120   # The toolbar button is toggled on macOS.
	ToolTip                          = 110   # A tooltip was requested (QHelpEvent).
	ToolTipChange                    = 184   # The widget's tooltip has changed.
	TouchBegin                       = 194   # Beginning of a sequence of touch-screen or track-pad events (QTouchEvent).
	TouchCancel                      = 209   # Cancellation of touch-event sequence (QTouchEvent).
	TouchEnd                         = 196   # End of touch-event sequence (QTouchEvent).
	TouchUpdate                      = 195   # Touch-screen event (QTouchEvent).
	UngrabKeyboard                   = 189   # Item loses keyboard grab (QGraphicsItem only).
	UngrabMouse                      = 187   # Item loses mouse grab (QGraphicsItem, QQuickItem).
	UpdateLater                      = 78    # The widget should be queued to be repainted at a later time.
	UpdateRequest                    = 77    # The widget should be repainted.
	WhatsThis                        = 111   # The widget should reveal "What's This?" help (QHelpEvent).
	WhatsThisClicked                 = 118   # A link in a widget's "What's This?" help was clicked.
	Wheel                            = 31    # Mouse wheel rolled (QWheelEvent).
	WinEventAct                      = 132   # A Windows-specific activation event has occurred.
	WindowActivate                   = 24    # Window was activated.
	WindowBlocked                    = 103   # The window is blocked by a modal dialog.
	WindowDeactivate                 = 25    # Window was deactivated.
	WindowIconChange                 = 34    # The window's icon has changed.
	WindowStateChange                = 105   # The window's state (minimized, maximized or full-screen) has changed (QWindowStateChangeEvent).
	WindowTitleChange                = 33    # The window title has changed.
	WindowUnblocked                  = 104   # The window is unblocked after a modal dialog exited.
	WinIdChange                      = 203   # The window system identifer for this native widget has changed.
	ZOrderChange                     = 126   # The widget's z-order has changed. This event is never sent to top level windows.

	__slots__ = ('d', 't', 'posted', 'spont', 'm_accept')
	def __init__(self, *args, **kwargs):
		self.d = 0
		self.t = kwargs.get('type', None)
		self.posted   = False
		self.spont    = False
		self.m_accept = True

	def type(self):
		return self.t

	def spontaneous(self):
		return self.spont

	def setAccepted(self, accepted):
		self.m_accept = accepted

	def isAccepted(self):
		return self.m_accept

	def accept(self):
		self.m_accept = True

	def ignore(self):
		self.m_accept = False



''' CuInputEvent
	ref: http://doc.qt.io/qt-5/qinputevent.html
'''
class CuInputEvent(CuEvent):
	__slots__ = ('modState', 'ts')
	def __init__(self, *args, **kwargs):
		CuEvent.__init__(self, *args, **kwargs)
		self.modState = kwargs.get('modifiers', CuT.NoModifier)
		self.ts       = 0

	def modifiers(self):
		return self.modState

	def timestamp(self):
		return self.ts

	def setTimestamp(self, atimestamp):
		self.ts = atimestamp


''' CuMouseEvent
	ref: http://doc.qt.io/qt-5/qmouseevent.html#x
'''
class CuMouseEvent(CuInputEvent):
	__slots__ = ('l', 'w', 's', 'b')

	def __init__(self, *args, **kwargs):
		CuInputEvent.__init__(self, *args, **kwargs)
		self.l = kwargs.get('localPos', CuPoint(0, 0))
		self.w = kwargs.get('windowPos', CuPoint(0, 0))
		self.s = kwargs.get('screenPos', CuPoint(0, 0))
		self.b = kwargs.get('button', CuT.NoButton)

	def globalPos(self):
		return self.s

	# Returns the global x position of the mouse cursor at the time of the event.
	def globalX(self):
		return self.s.x()

	# Returns the global y position of the mouse cursor at the time of the event.
	def globalY(self):
		return self.s.y()

	# Returns the position of the mouse cursor, relative to the widget that received the event.
	def pos(self):
		return self.l

	# Returns the position of the mouse cursor as a Point, relative to the screen that received the event.
	def screenPos(self):
		return self.s

	# Returns the position of the mouse cursor as a Point, relative to the window that received the event.
	def windowPos(self):
		return self.w

	# Returns the x position of the mouse cursor, relative to the widget that received the event.
	def x(self):
		return self.l.x()

	# Returns the y position of the mouse cursor, relative to the widget that received the event.
	def y(self):
		return self.l.y()

	def button(self):
		return self.b



''' CuWheelEvent
	ref: http://doc.qt.io/qt-5/qwheelevent.html
'''
class CuWheelEvent(CuInputEvent):
	__slots__ = ('p', 'g', 'angleD', 'invertedScrolling')
	def __init__(self, *args, **kwargs):
		CuInputEvent.__init__(self, *args, **kwargs)
		self.p      = kwargs.get('pos', CuPoint())
		self.g      = kwargs.get('globalPos', CuPoint())
		self.angleD = kwargs.get('angleDelta', CuPoint())
		self.invertedScrolling = False

	def globalPos(self):
		return self.g

	# Returns the global x position of the mouse cursor at the time of the event.
	def globalX(self):
		return self.g.x()

	# Returns the global y position of the mouse cursor at the time of the event.
	def globalY(self):
		return self.g.y()

	# Returns the position of the mouse cursor, relative to the widget that received the event.
	def pos(self):
		return self.x(), self.y()

	# Returns the x position of the mouse cursor, relative to the widget that received the event.
	def x(self):
		return self.p.x()

	# Returns the y position of the mouse cursor, relative to the widget that received the event.
	def y(self):
		return self.p.y()

	def angleDelta(self):
		return self.angleD

	def inverted(self):
		return self.invertedScrolling

''' CuKeyEvent
	ref: http://doc.qt.io/qt-5/qkeyevent.html
'''
class CuKeyEvent(CuInputEvent):
	__slots__ = ('_key','_text')
	def __init__(self, *args, **kwargs):
		CuInputEvent.__init__(self, *args, **kwargs)
		self._key  = kwargs.get('key', '')
		self._text = kwargs.get('text', '')

	def key(self):
		return self._key

	def text(self):
		return self._text

class CuFocusEvent(CuEvent):
	__slots__ = ('_reason')
	def __init__(self, *args, **kwargs):
		CuEvent.__init__(self, *args, **kwargs)
		self._reason  = kwargs.get('reason', CuT.OtherFocusReason)

	def gotFocus(self):
		return self.type() == CuEvent.FocusIn

	def lostFocus(self):
		return self.type() == CuEvent.FocusOut

	def reason(self):
		return self._reason
