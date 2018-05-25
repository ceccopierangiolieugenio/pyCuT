'''
https://stackoverflow.com/questions/9254664/python-curses-getmouse?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
'''

import curses 

# print '\033[?1003h'

def main(screen):
	#screen = curses.initscr() 
	#curses.noecho() 
	curses.curs_set(0) 
	screen.keypad(1) 
	curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

	screen.addstr("This is a Sample Curses Script\n\n")
	# printf("\033[?1003h\n"); // Makes the terminal report mouse movement events
	print '\033[?1003h'


	it = 1;
	while True:
	    event = screen.getch()
	    screen.addstr(8, 10, "Iteration:" + str(it))
	    it += 1
	    screen.addstr(9, 10, "Event:" + str(event))
	    if event == curses.ERR: break
	    if event == ord("q"): break 
	    if event == curses.KEY_MOUSE:
	        # _, mx, my, _, _ = curses.getmouse()
	        # y, x = screen.getyx()
	        screen.addstr(10, 10, "pippo")
	        screen.addstr(11, 10, str(curses.getmouse()) + "                      ")

try:
	curses.wrapper(main)
finally:
	# Reset (disable) the terminal report mouse movement events
	print '\033[?1003l'