#!/usr/bin/python

from CuT.CuTCore import CuApplication, CuWrapper
from CuT.CuTWidgets import CuMainWindow, CuWidget, CuHBoxLayout, CuVBoxLayout, CuPanel

class MainWindow(CuMainWindow):
	pass


class Widget(CuWidget):
	def paint(self):
		CuWidget.paint(self)
		self.getWin().addstr(3, 3, "Widget")
		self.getWin().addstr(4, 3, self.accessibleName())
		self.getWin().addstr(5, 3, "Max: "  + str(self.maximumSize()))
		self.getWin().addstr(6, 3, "Min: "  + str(self.minimumSize()))
		self.getWin().addstr(7, 3, "Size: " + str(self.size()))


def main(screen):
	import sys

	app = CuApplication(screen, sys.argv)
	window = MainWindow()
	window.setBorder(True)

	layout = CuHBoxLayout()

	tw1 = Widget(parent=window); tw1.setAccessibleName('tw1'); tw1.setBorder(True)
	tw1.setMaximumSize(25,50)
	tw1.setMinimumSize(20,25)
	layout.addWidget(tw1)

	tw2 = Widget(parent=window); tw2.setAccessibleName('tw2')
	tw2.setMaximumSize(30,9000)
	layout.addWidget(tw2)

	vlayout1 = CuVBoxLayout()
	vlayout2 = CuVBoxLayout()

	p1 = CuPanel(parent=window); p1.setBorder(True)
	layout.addWidget(p1)

	tw3 = Widget(parent=p1); tw3.setAccessibleName('tw3'); tw3.setBorder(True)
	tw3.setMaximumSize(20,10)
	tw3.setMinimumSize(10,4)
	vlayout1.addWidget(tw3)

	tw5 = Widget(parent=p1); tw5.setAccessibleName('tw5'); tw5.setBorder(True)
	tw5.setMaximumSize(30,9000)
	vlayout1.addWidget(tw5)

	p2 = CuPanel(parent=window)
	layout.addWidget(p2)

	tw6 = Widget(parent=p2); tw6.setAccessibleName('tw6'); tw6.setBorder(True)
	tw6.setMaximumSize(50,9000)
	vlayout2.addWidget(tw6)

	tw7 = Widget(parent=p2); tw7.setAccessibleName('tw7'); tw7.setBorder(True)
	tw7.setMaximumSize(50,9000)
	vlayout2.addWidget(tw7)

	window.setLayout(layout)
	p1.setLayout(vlayout1)
	p2.setLayout(vlayout2)
	window.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	CuWrapper(main)
