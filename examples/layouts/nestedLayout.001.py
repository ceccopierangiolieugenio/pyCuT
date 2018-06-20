#!/usr/bin/python

from CuT.CuTCore import  CuT
from CuT.CuTGui import CuPainter
from CuT.CuTWidgets import CuApplication, CuMainWindow, CuWidget, CuHBoxLayout, CuVBoxLayout, CuPanel
from CuT.CuTHelper import CuWrapper

class MainWindow(CuMainWindow):
	pass

class Widget(CuWidget):
	def paintEvent(self, event):
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		qp.drawText(3, 3, "Widget")
		qp.setPen(CuT.yellow)
		qp.drawText(3, 4, self.accessibleName())
		qp.setPen(CuT.green)
		qp.drawText(3, 5, "Size: " + str(self.size()))
		qp.drawText(3, 10, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()

def main(screen):
	import sys

	app = CuApplication(screen, sys.argv)
	window = MainWindow()
	window.setBorder(True)

	layout = CuHBoxLayout()

	tw1 = Widget(parent=window)
	tw1.setAccessibleName('tw1')
	tw1.setBorder(True)
	layout.addWidget(tw1)

	tw2 = Widget(parent=window)
	tw2.setAccessibleName('tw2')
	layout.addWidget(tw2)

	vlayout1 = CuVBoxLayout()
	vlayout2 = CuVBoxLayout()

	p1 = CuPanel(parent=window)
	p1.setBorder(True)
	layout.addWidget(p1)

	tw3 = Widget(parent=p1)
	tw3.setAccessibleName('tw3')
	tw3.setBorder(False)
	vlayout1.addWidget(tw3)

	tw5 = Widget(parent=p1)
	tw5.setAccessibleName('tw5')
	tw5.setBorder(True)
	vlayout1.addWidget(tw5)

	p2 = CuPanel(parent=window)
	layout.addWidget(p2)

	tw6 = Widget(parent=p2)
	tw6.setAccessibleName('tw6')
	tw6.setBorder(True)
	vlayout2.addWidget(tw6)

	tw7 = Widget(parent=p2)
	tw7.setAccessibleName('tw7')
	tw7.setBorder(True)
	vlayout2.addWidget(tw7)

	window.setLayout(layout)
	p1.setLayout(vlayout1)
	p2.setLayout(vlayout2)
	window.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	CuWrapper.init(main)
