#!/usr/bin/python

from CuT.CuTGui import CuPainter
from CuT.CuTCore import  CuT
from CuT.CuTWidgets import CuApplication, CuMainWindow, CuWidget, CuHBoxLayout, CuVBoxLayout, CuFrame
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
		qp.drawText(3, 5, "Max: "  + str(self.maximumSize()))
		qp.drawText(3, 6, "Min: "  + str(self.minimumSize()))
		qp.setPen(CuT.red)
		qp.drawText(3, 7, "Size: " + str(self.size()))
		qp.setPen(CuT.lightGray)
		qp.drawText(3, 12, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		qp.end()


def main(screen):
	import sys

	app = CuApplication(screen, sys.argv)
	window = MainWindow()

	layout = CuHBoxLayout()

	tw1 = Widget(parent=window); tw1.setAccessibleName('tw1');
	tw1.setMaximumSize(25,50)
	tw1.setMinimumSize(20,25)
	layout.addWidget(tw1)

	tw2 = Widget(parent=window); tw2.setAccessibleName('tw2')
	tw2.setMaximumSize(30,9000)
	layout.addWidget(tw2)

	vlayout1 = CuVBoxLayout()
	vlayout2 = CuVBoxLayout()

	p1 = CuFrame(parent=window);
	layout.addWidget(p1)

	tw3 = Widget(parent=p1); tw3.setAccessibleName('tw3');
	tw3.setMaximumSize(20,10)
	tw3.setMinimumSize(10,4)
	vlayout1.addWidget(tw3)

	tw5 = Widget(parent=p1); tw5.setAccessibleName('tw5');
	tw5.setMaximumSize(30,9000)
	vlayout1.addWidget(tw5)

	p2 = CuFrame(parent=window)
	layout.addWidget(p2)

	tw6 = Widget(parent=p2); tw6.setAccessibleName('tw6');
	tw6.setMaximumSize(60,9000)
	vlayout2.addWidget(tw6)

	tw7 = Widget(parent=p2); tw7.setAccessibleName('tw7');
	tw7.setMaximumSize(60,9000)
	vlayout2.addWidget(tw7)

	window.setLayout(layout)
	p1.setLayout(vlayout1)
	p2.setLayout(vlayout2)
	window.show()

	sys.exit(app.exec_())


if __name__ == '__main__':
	CuWrapper.init(main)
