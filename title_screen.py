# title_screen.py

import curses
from copy import deepcopy

P = r"""
 _____
/  _  \
|  ___/
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


E = r"""
 _______
|  _____|
| |_____
|  _____|
| |_____
|_______|
"""

L = r"""
 _
| |
| |
| |
| |____
|______|
"""

O = r"""
   _____
  /     \
 |  ___  |
 | |___| |
 |       |
  \_____/
"""

N = r"""
 _     _
| \ \ | |
|  \ \| |
| | \ | |
| |  \| |
|_|   \_|
"""

G = r"""
  ________ 
 /  _____/ 
/   \  ___ 
\    \_\  \
 \______  /
        \/ 
"""


MESSAGE = (P, I, X, E, L, P, O, N, G)

def log(msg):
	open("log.txt", "a").write("\n" + str(msg))

char_ascii = lambda screen, char: screen.getch() == ord(char)
char_special = lambda screen, spec: screen.getch() == spec

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

	spacing = max_x // len(MESSAGE) - 5 # may have to subtract spacing by letter width

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

	screen.addstr(max_y // 2 + 10, max_x // 2 - (max_x // 8), "Press any key to start!")
		
	if char_special(screen, curses.KEY_ENTER):
		return

		# start with displaying letters until the user hits enter
		# then go to an option screen (names of players, winning score, colors, etc)



if __name__ == "__main__":
	curses.wrapper(title_screen)