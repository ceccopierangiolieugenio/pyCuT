import curses, curses.panel
import logging

from CuT.CuTWidgets import CuApplication

def CuWrapper(func):
	try:
		curses.wrapper(func)
	finally:
		CuApplication.__CuEnd__()
