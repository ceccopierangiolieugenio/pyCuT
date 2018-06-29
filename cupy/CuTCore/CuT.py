
class CuT:
	class GlobalColor(int):
		pass

	color0 = 1 # type: 'Qt.GlobalColor'
	color1 = 2
	black = 3
	white = 4
	darkGray = 5
	gray = 6
	lightGray = 7
	red = 8
	green = 9
	blue = 10
	cyan = 11
	magenta = 12
	yellow = 13
	darkRed = 14
	darkGreen = 15
	darkBlue = 16
	darkCyan = 17
	darkMagenta = 18
	darkYellow = 19
	transparent = 20

	NoButton      = 0x00000000 # The button state does not refer to any button (see QMouseEvent::button()).
	AllButtons    = 0x07ffffff # This value corresponds to a mask of all possible mouse buttons. Use to set the 'acceptedButtons' property of a MouseArea to accept ALL mouse buttons.
	LeftButton    = 0x00000001 # The left button is pressed, or an event refers to the left button. (The left button may be the right button on left-handed mice.)
	RightButton   = 0x00000002 # The right button.
	MidButton     = 0x00000004 # The middle button.
	MiddleButton  = MidButton # The middle button.
	BackButton    = 0x00000008 # The 'Back' button. (Typically present on the 'thumb' side of a mouse with extra buttons. This is NOT the tilt wheel.)
	XButton1      = BackButton # The 'Back' Button.
	ExtraButton1  = XButton1 # The 'Back' Button.
	ForwardButton = 0x00000010 # The 'Forward' Button. (Typically present beside the 'Back' button, and also pressed by the thumb.)
	XButton2      = ForwardButton # The 'Forward Button.
	ExtraButton2  = ForwardButton # The 'Forward' Button.
	TaskButton    = 0x00000020 # The 'Task' Button.
	ExtraButton3  = TaskButton # The 'Task' Button.
	ExtraButton4  = 0x00000040 # The 7th non-wheel Mouse Button.
	ExtraButton5  = 0x00000080 # The 8th non-wheel Mouse Button.
	ExtraButton6  = 0x00000100 # The 9th non-wheel Mouse Button.
	ExtraButton7  = 0x00000200 # The 10th non-wheel Mouse Button.
	ExtraButton8  = 0x00000400 # The 11th non-wheel Mouse Button.
	ExtraButton9  = 0x00000800 # The 12th non-wheel Mouse Button.
	ExtraButton10 = 0x00001000 # The 13th non-wheel Mouse Button.
	ExtraButton11 = 0x00002000 # The 14th non-wheel Mouse Button.
	ExtraButton12 = 0x00004000 # The 15th non-wheel Mouse Button.
	ExtraButton13 = 0x00008000 # The 16th non-wheel Mouse Button.
	ExtraButton14 = 0x00010000 # The 17th non-wheel Mouse Button.
	ExtraButton15 = 0x00020000 # The 18th non-wheel Mouse Button.
	ExtraButton16 = 0x00040000 # The 19th non-wheel Mouse Button.
	ExtraButton17 = 0x00080000 # The 20th non-wheel Mouse Button.
	ExtraButton18 = 0x00100000 # The 21st non-wheel Mouse Button.
	ExtraButton19 = 0x00200000 # The 22nd non-wheel Mouse Button.
	ExtraButton20 = 0x00400000 # The 23rd non-wheel Mouse Button.
	ExtraButton21 = 0x00800000 # The 24th non-wheel Mouse Button.
	ExtraButton22 = 0x01000000 # The 25th non-wheel Mouse Button.
	ExtraButton23 = 0x02000000 # The 26th non-wheel Mouse Button.
	ExtraButton24 = 0x04000000 # The 27th non-wheel Mouse Button.


class CuPoint:
	def __init__(self, x=0, y=0):
		self._x = x
		self._y = y

class CuPointF(CuPoint):
	pass