# title_screen.py

import curses
from copy import deepcopy

char_ascii = lambda screen, char: screen.getch() == ord(char)

P = r"""
 _____
/  _  \
|  ___/
| |
| |
| |
\_/
"""


I = r"""
 ______
|_   __|
  | |
  | |
 _| |__
|______|
"""



X = r"""
 __    __
 \ \  / /
  \ \/ /
  / /\ \
 / /  \ \
/_/    \_\
"""


E = """ e """
L = """ l """
P2 = """ p """
O = """ o """
N = """ n """
G = """ g """

def log(msg):
	open("log.txt", "a").write("\n" + str(msg))

MESSAGE = (P, I, X, E, L, P2, O, N, G)

def put_char(screen, x, y, s, color = None):
	try:
		screen.move(y, x)
		if color is None:
			screen.addstr(y, x, s)
		else:
			screen.addstr(y, x, s, color)
	except curses.error:
		pass

def title_screen(screen):

	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)
	screen.bkgd(" ", curses.color_pair(1))

	max_y, max_x = screen.getmaxyx()

	spacing = max_x // len(MESSAGE)  # may have to subtract spacing by letter width

	# this almost works!
	y, x = max_y // 2, 0
	for index in range(len(MESSAGE)):
		LETTER = MESSAGE[index]
		spacing_index = deepcopy(index) + 1
		for row in LETTER.split("\n"):
			for char in row:
				screen.addstr(y, x, char)
				x += 1
			x = spacing * spacing_index
			y += 1

		y = max_y // 2
		x += spacing

	"""
	y, x = 0, 0
	for LETTER in MESSAGE:
		for row in LETTER.split("\n"):
			for char in row:
				screen.addstr(y, x, char)
				x += 1
			x = 0
			y += 1
	"""

	while not char_ascii(screen, "q"):
		pass
		# start with displaying letters until the user hits enter
		# then go to an option screen (names of players, winning score, colors, etc)



if __name__ == "__main__":
	curses.wrapper(title_screen)