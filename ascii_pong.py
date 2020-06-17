# ascii_pong.py

import curses, time
from random import randint as ra




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
# colored ball - done
# cool colored background (maybe) - done
# colored paddle - done
# random starting ball position - done
# hit the paddl
# make the paddle faster than the ball, or give it some acceleration
# add a second paddle

left_paddle_y = 0
PADDLE_HEIGHT = 5

right_paddle_y = 0

ball_pos = [0, 0]
b_going_right = True
b_going_down = True

def move_ball(screen):
	global ball_pos

	wall_bounce(screen)

	if b_going_right: ball_pos[0] += 1
	else: ball_pos[0] -= 1

	if b_going_down: ball_pos[1] += 1
	else: ball_pos[1] -= 1

	put_char(screen, *ball_pos, "*")

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

def put_char(screen, x, y, s, color = None):
	try:
		screen.move(y, x)
		if color is None:
			screen.addstr(y, x, s)
		else:
			screen.addstr(y, x, s, color)
	except curses.error:
		pass

def main(screen):
	global left_paddle_y, right_paddle_y, ball_pos

	rand_x = lambda: ra(0, screen.getmaxyx()[1])
	rand_y = lambda: ra(0, screen.getmaxyx()[0] - PADDLE_HEIGHT - 1)

	# initialization
	ball_pos = [rand_x(), rand_y()]

	left_paddle_y = rand_y()
	right_paddle_y = rand_y()

	curses.noecho()
	screen.keypad(True)
	screen.nodelay(True)
	curses.use_default_colors()  # wow, this is cool!

	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)  # screen
	screen.bkgd(" ", curses.color_pair(1))

	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)  # left paddle

	while not char_ascii(screen, "q"):

		# if char_special(screen, curses.KEY_UP) and paddle_y != 0:
		if char_ascii(screen, "w") and left_paddle_y != 0:
			left_paddle_y -= 1

		elif char_ascii(screen, "s"):
			if left_paddle_y != (screen.getmaxyx()[0] - PADDLE_HEIGHT - 1):
				left_paddle_y += 1

		time.sleep(0.1)

		screen.clear()
		for h in range(PADDLE_HEIGHT + 1):
			put_char(screen, 5, left_paddle_y + h, " ", curses.color_pair(2))

		move_ball(screen)

		screen.refresh()


if __name__ == "__main__":
	curses.wrapper(main)
