# ascii_pong.py

import curses, time




"""
def main(screen):
	global paddle_pos

	def char_key():
		try:
			return chr(ord(screen.getkey()))
		except TypeError:
			pass

	def put_str(y = None, x = None, s):
		try:
			screen.addstr(y, x, s)
		except curses.error:
			pass

	curses.noecho()
	# curses.cbreak()
	screen.keypad(True)

	while char_key() != "q":
		for h in range(PADDLE_HEIGHT):
			screen.addstr(paddle_pos[1] + h, paddle_pos[0], "#")

		screen.clear()

		key = char_key()

		if key == "w":
			screen.addstr("up")
			paddle_pos[1] += 1
		elif key == "s":
			screen.addstr("down")
			paddle_pos[1] -= 1
"""

# next time:
# colored ball
# cool colored background (maybe)
# colored paddle

paddle_y = 0
PADDLE_HEIGHT = 5

ball_pos = [5, 5]
b_going_right = True
b_going_down = True

def move_ball(screen):
	global ball_pos

	wall_bounce(screen)

	if b_going_right: ball_pos[0] += 1
	else: ball_pos[0] -= 1

	if b_going_down: ball_pos[1] += 1
	else: ball_pos[1] -= 1

	put_char(screen, *ball_pos, "O", curses.color_pair(1))


def wall_bounce(screen):
	global b_going_right, b_going_down

	x, y = screen.getmaxyx()[::-1]

	if ball_pos[0] == 0:
		screen.addstr("Hitting left wall")  # remove these later
		b_going_right = True
	elif ball_pos[0] == x:
		screen.addstr("Hitting right wall")
		b_going_right = False
	if ball_pos[1] == 0:
		screen.addstr("Hitting top of window")
		b_going_down = True
	elif ball_pos[1] == y - 1:
		screen.addstr("Hitting bottom of window")
		b_going_down = False


char_ascii = lambda screen, char: screen.getch() == ord(char)
char_special = lambda screen, spec: screen.getch() == spec

def put_char(screen, x, y, s, color_pair = None):
	try:
		screen.move(y, x)
		if color_pair is None:
			screen.addstr(y, x, s)
		else:
			screen.addstr(y, x, s, color_pair)
	except curses.error:
		pass

def main(screen):
	global paddle_y

	curses.noecho()
	screen.keypad(True)
	screen.nodelay(True)

	curses.use_default_colors()  # wow, this is cool!

	while not char_ascii(screen, "q"):

		curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)

		if char_special(screen, curses.KEY_UP) and paddle_y != 0:
			paddle_y -= 1

		elif char_special(screen, curses.KEY_DOWN):
			if paddle_y != (screen.getmaxyx()[0] - PADDLE_HEIGHT - 1):
				paddle_y += 1

		time.sleep(0.1)

		screen.clear()
		for h in range(PADDLE_HEIGHT + 1):
			put_char(screen, 0, paddle_y + h, "#")

		move_ball(screen)

		screen.refresh()


if __name__ == "__main__":
	curses.wrapper(main)