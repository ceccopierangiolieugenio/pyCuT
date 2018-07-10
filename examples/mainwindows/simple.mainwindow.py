#!/usr/bin/python

from CuT.CuTCore import  CuT
from CuT.CuTWidgets import CuApplication, CuMainWindow
from CuT.CuTGui import CuPainter
from CuT.CuTHelper import CuWrapper

class MainWindow(CuMainWindow):
	def paintEvent(self, evt):
		qp = CuPainter()
		qp.begin(self)
		qp.setPen(CuT.white)
		qp.drawText(5, 5, "MainWindow")
		qp.end()
		CuMainWindow.paintEvent(self, evt)


def main(screen):
	import sys

	app = CuApplication(screen, sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	CuWrapper.init(main)
