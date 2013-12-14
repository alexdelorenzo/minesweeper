__author__ = 'alex'


import pyglet
from random import random as r
from board import Board
from math import floor

cursor = None

xi, yi = 15,15
x, y = xi, yi
lvl = 1
starts = True
mines = Board(xi, yi)


colors_rgb = \
	(7,126,138, 255), \
	(6, 84, 127, 255), \
	(0,115,94, 255), \
	(7,138,77, 255), \
	(6,127,37, 255)

colors_dec = [tuple(rgb/255 for rgb in color) for color in colors_rgb]
b1, b2, b3, b4, b5 = colors_rgb

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
four, gl_flag, indices = 4, 'v2i', (0, 1, 2, 0, 2, 3)
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
	set_live_color(*zero_sq)
	gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices))

	for bomb in board.bombs:
		draw_square(bomb, scale, bomb_sq)




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

	process_board(mines, starts)

	if not board.start:
		if board.win:
				window.set_caption(":) You win. Time: " + str(board.time))
		else:
				window.set_caption(":( You lose.")

	for sq in board.unclicked_squares:
		draw_square(sq, scale, unclicked_sq)

	for flag in mines.flags:
		draw_square(flag, scale, flag_sq)


def _draw_nums(board, pts):
	for pt in pts:
		num = board.numbers[pt]
		
		draw_square(pt, scale, number_sq)
		draw_text(str(number), pt, size=8, color=black)

def get_visible_sqs(board):
	draw_these_nums = board.numbers - board.unclicked_squares
	draw_these_zeros = board._blank_board - board.unclicked_squares

	return draw_these_nums, draw_these_zeros



@window.event
def on_mouse_motion(x, y, dx, dy):
	pass



def on_draw(*args): pass

@window.event
def on_mouse_press(x, y, button, modifiers, board=mines):
	point = floor(x / scale), floor(y / scale)

	if button == 1:
		if point not in mines.flags:
			mines.select_sq(point)
	elif button == 4:
		if point in mines.flags:
			mines.flags.remove(point)
		else:
			if point in mines.unclicked_squares:
				mines.flags.add(point)

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

