
''' CuPalette
		ref: http://pyqt.sourceforge.net/Docs/PyQt5/api/QtGui/qpalette.html
		ref: https://doc.qt.io/qt-5/qpalette.html
'''
class CuPalette:
	class ColorRole(int): pass
	Window        = 10         # A general background color.
	Background    = Window     # This value is obsolete. Use Window instead.
	WindowText    = 0          # A general foreground color.
	Foreground    = WindowText # This value is obsolete. Use WindowText instead.
	Base          = 9          # Used mostly as the background color for text entry widgets, but can also be used for other painting - such as the background of combobox drop down lists and toolbar handles. It is usually white or another light color.
	AlternateBase = 16         # Used as the alternate background color in views with alternating row colors (see QAbstractItemView::setAlternatingRowColors()).
	ToolTipBase   = 18         # Used as the background color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
	ToolTipText   = 19         # Used as the foreground color for QToolTip and QWhatsThis. Tool tips use the Inactive color group of QPalette, because tool tips are not active windows.
	Text          = 6          # The foreground color used with Base. This is usually the same as the WindowText, in which case it must provide good contrast with Window and Base.
	Button        = 1          # The general button background color. This background can be different from Window as some styles require a different background color for buttons.
	ButtonText    = 8          # A foreground color used with the Button color.
	BrightText    = 7          # A text color that is very different from WindowText, and contrasts well with e.g. Dark. Typically used for text that needs to be drawn where Text or WindowText would give poor contrast, such as on pressed push buttons. Note that text colors can be used for things other than just words; text colors are usually used for text, but it's quite common to use the text color roles for lines, 

	def __init__(self, *args, **kwargs): pass
