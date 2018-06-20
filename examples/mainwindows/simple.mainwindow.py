#!/usr/bin/python

from CuT.CuTWidgets import CuApplication, CuMainWindow
from CuT.CuTHelper import CuWrapper

class MainWindow(CuMainWindow):
	def paint(self):
		CuMainWindow.paint(self)
		self.getWin().addstr(3, 3, "MainWindow")


def main(screen):
	import sys

	app = CuApplication(screen, sys.argv)
	window = MainWindow()
	window.setBorder(True)
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	CuWrapper.init(main)
