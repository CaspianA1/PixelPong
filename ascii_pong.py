# ascii_pong.py

import curses, time
from random import randint as ra, choice as ch




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
# hit the paddle - done
# make the paddle faster than the ball, or give it some acceleration - done
# add a second paddle - done
# increase baud rate of terminal - not sure how to do?

left_paddle_y = 0
right_paddle_y = 0

left_score = 0
right_score = 0

PADDLE_HEIGHT = 10
PADDLE_DIST_WALL = 10

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

	x, y = screen.getmaxyx()[::-1]

	put_char(screen, *ball_pos, "*")

	hit_paddle(screen)

def wall_bounce(screen):
	global b_going_right, b_going_down, left_score, right_score

	x, y = screen.getmaxyx()[::-1]

	if ball_pos[0] == 0:
		b_going_right = True
		right_score += 1
	elif ball_pos[0] == x:
		b_going_right = False
		left_score += 1
	if ball_pos[1] == 0:
		b_going_down = True
	elif ball_pos[1] == y:
		b_going_down = False

def hit_paddle(screen):
	global b_going_right, b_going_down

	# left paddle x collision
	if ball_pos[0] in (PADDLE_HEIGHT - 1, PADDLE_HEIGHT + 1):
		# left paddle y collision
		if ball_pos[1] in range(left_paddle_y, left_paddle_y + PADDLE_HEIGHT + 1):
			curses.flash()
			b_going_right = not b_going_right

	# right paddle x collision
	elif ball_pos[0] in (screen.getmaxyx()[1] - PADDLE_DIST_WALL - 1,
		screen.getmaxyx()[1] - PADDLE_DIST_WALL + 1):
		# right paddle y position
		if ball_pos[1] in range(right_paddle_y, right_paddle_y + PADDLE_HEIGHT - 1):
			curses.flash()
			curses.beep()
			b_going_right = not b_going_right

char_ascii = lambda screen, char: screen.getch() == ord(char)
# char_special = lambda screen, spec: screen.getch() == spec

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
	global b_going_right, b_going_down

	rand_x = lambda: ra(0, screen.getmaxyx()[1])
	rand_y = lambda: ra(0, screen.getmaxyx()[0] - PADDLE_HEIGHT - 1)

	# initialization
	ball_pos = [rand_x(), rand_y()]

	left_paddle_y = rand_y()
	right_paddle_y = rand_y()

	b_going_right = ch((True, False))
	b_going_down = ch((True, False))

	# curses.noecho()
	# curses.cbreak()
	# screen.keypad(True)  # .wrapper initializes these by default
	# curses.noraw()
	curses.raw()
	curses.savetty()

	screen.nodelay(True)

	curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)  # screen
	screen.bkgd(" ", curses.color_pair(1))

	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)  # left and right paddle

	while not char_ascii(screen, "q"):
		_, x = screen.getmaxyx()
		#screen.addstr(0, 0, f"Ball x and y: {ball_pos[0]} {ball_pos[1]}")
		#sscreen.addstr(1, 0, f"Left paddle y: {left_paddle_y}")
		screen.addstr(0, x // 3, f"| Player 1 Score: {left_score}   Player 2 score: {right_score}  |")
		screen.addstr(1, x // 3, r"|_\/_\/_\/_\/_\/_\/_\/_\/_\/_\/_\/_\/_\/\|")

		max_y, max_x = screen.getmaxyx()

		# maybe use ungetch somewhere here

		if char_ascii(screen, "w") and left_paddle_y != 0:
			left_paddle_y -= 2

			if left_paddle_y < 0:
				left_paddle_y = 0

		elif char_ascii(screen, "s"):
			left_paddle_y += 2

			if left_paddle_y + PADDLE_HEIGHT > max_y:
				left_paddle_y = max_y - PADDLE_HEIGHT - 1

		# if char_special(screen, curses.KEY_UP) and right_paddle_y != 0:
		if char_ascii(screen, "i") and right_paddle_y != 0:
			right_paddle_y -= 2

			if right_paddle_y < 0:
				right_paddle_y = 0

		# elif char_special(screen, curses.KEY_DOWN):
		elif char_ascii(screen, "k"):
			if right_paddle_y != (screen.getmaxyx()[0] - PADDLE_HEIGHT - 1):
				right_paddle_y += 2

			if right_paddle_y + PADDLE_HEIGHT > max_y:
				right_paddle_y = max_y - PADDLE_HEIGHT - 1

		# curses.napms(185)
		screen.clear()
		curses.napms(40)

		for h in range(PADDLE_HEIGHT + 1):

			put_char(screen,
			PADDLE_DIST_WALL,
			left_paddle_y + h,
			" ", curses.color_pair(2))  # left paddle

			put_char(
			screen,
			screen.getmaxyx()[1] - PADDLE_DIST_WALL, 
			right_paddle_y + h, " ",
			curses.color_pair(2))  # right paddle

		move_ball(screen)
		screen.refresh()


if __name__ == "__main__":
	curses.wrapper(main)
