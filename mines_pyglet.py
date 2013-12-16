__author__ = 'alex'


import pyglet
from random import random as r
from board import Board
from math import floor

cursor = None

xi, yi = 30, 30
x, y = xi, yi
lvl = 5
starts = True
mines = Board(xi, yi, lvl)
flag_mode = False


brd = {(_x,_y) for _x in range(x) for _y in range(y)}

scale = 20

black = 0, 0, 0, 255
white = 255, 255, 255
purple = 0.5, 0, 0.5
orange = 1, 0.5, 0
red = 255, 0, 0
default = white

number_sq = 0.5, 0.5, 0.5
zero_sq = 0.25, 0.25, 0.25
bomb_sq = red
unclicked_sq = 0.75, 0.75, 0.75
flag_sq = orange

set_live_color = pyglet.gl.glColor3f
gl_draw_sq = pyglet.graphics.draw_indexed

window = pyglet.window.Window(width=(x+1)*scale, height=(y+1)*scale)
four, gl_flag, indices = 4, 'v2i2', (0, 1, 2, 0, 2, 3)
vertices = 0,0, x*scale+scale,0, x*scale+scale,y*scale+scale, 0,y*scale+scale
set_live_color(*unclicked_sq)
gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices))

def draw_square(point, size=1, color=white):
	set_live_color(*color)
	x, y = point[0] * size, point[1] * size
	x_size, y_size = x + size, y + size
	vertices = x,y, x_size,y, x_size,y_size, x,y_size
	gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices))

def draw_text(label="Txt", point=(10,10), size=1, color=black):
	x, y = point[0] * scale + scale/4, point[1] * scale + scale/4
	font = 'Sans'
	label = pyglet.text.Label(label, font_name=font, font_size=size, x=x, y=y, color=color)
	label.draw()



def process_board(board, start):
	#set_live_color(*zero_sq)
	#gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices))

	these_nums, these_zeros = get_visible_sqs(board)

	_draw_zeros(board, these_zeros)
	_draw_nums(board, these_nums)
	_draw_flags(board)

	if not board.unclicked_squares:
		_draw_bombs(board)



def _draw_nums(board, pts):
	for pt in pts:
		number = board.numbers[pt]
		draw_square(pt, scale, number_sq)
		draw_text(str(number), pt, size=8, color=black)
		board.numbers.pop(pt)

def _draw_zeros(board, pts):
	for pt in pts:
		draw_square(pt, scale, zero_sq)
		board.blank_board.remove(pt)

def _draw_bombs(board):
	for bomb in board.bombs:
		draw_square(bomb, scale, bomb_sq)

def _draw_flags(board):
	for flag in board.flags:
		draw_square(flag, scale, flag_sq)

def _draw_unclicked(board):
	for sq in board.unclicked_squares:
		draw_square(sq, scale, unclicked_sq)

def get_visible_sqs(board):
	draw_these_nums = board.numbers.keys() - board.unclicked_squares
	draw_these_zeros = board.blank_board - board.unclicked_squares

	return draw_these_nums, draw_these_zeros

def update_title(dt, board):
	if not board.start:
		return

	if board.round:
		board.time += 1

	str_mines = "Mines: " + str(len(board.bombs))
	str_flags = "Flags: " + str(len(board.flags))
	str_time = "Time: " + str(board.time)
	window.set_caption(' '.join((str_mines, str_flags, str_time)))

def draw_clicks(board):
	if not board.round:
		board.start_game()
		_draw_unclicked(board)

	process_board(mines, starts)

	if not board.start:
		if board.win:
				window.set_caption(":) You win. Time: " + str(board.time))
		else:
				window.set_caption(":( You lose.")


@window.event
def on_mouse_motion(x, y, dx, dy):
	pass



def on_draw(*args): pass

@window.event
def on_key_press(symbol, modifiers, flag_mode=flag_mode):
	if symbol == pyglet.window.key.F:
		flag_mode = False if flag_mode else True

@window.event
def on_mouse_press(x, y, button, modifiers, board=mines):
	point = floor(x / scale), floor(y / scale)

	if flag_mode and button == 1:
		start_button = 4

	if button == 4:
		if point not in mines.flags:
			mines.select_sq(point)

	elif button == 1:
		truth = mines.set_flag(point)
		if truth:
			draw_square(point, scale, unclicked_sq)

	elif button == 2:
		mines.__init__(xi, xi, lvl)


	draw_clicks(mines)



def main():
	set_live_color(*unclicked_sq)
	pyglet.clock.schedule_once(lambda args: gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices)), 0.1)
	pyglet.clock.schedule_interval(update_title, 1, mines)
	pyglet.app.run()

if __name__ == "__main__":
	#pyglet.clock.schedule(on_draw)
	main()

