__author__ = 'alex'
import math
from random import randint
import copy

class Board(object):
	def __init__(self, x, y, level=1):
		self.x, self.y = x, y
		self.level = level

		self.bombs = self.gen_bombs(x, y, level)
		self.numbers, self.unclicked_squares = self.gen_numbers(x, y, self.bombs)
		self.blank_board = copy.copy(self.unclicked_squares)
		self.flags = set()

		self.time = 0
		self.round = 0
		self.start = False
		self.win = False


	def _pop_consec_zero_sqs(self, point):
		x, y = point

		neighbors = {(x, y+1), (x, y-1), (x+1, y), (x-1, y)}

		for neighbor in neighbors:
			self.select_sq(neighbor)

		neighbors = self.gen_neighbors(point)

		for neighbor in neighbors:
			if neighbor in self.unclicked_squares and neighbor in self.numbers:
				self.unclicked_squares.remove(neighbor)


	def _num_of_bombs(self, x, y, level):
		return math.ceil(x*y /(5 + (10 / level)))


	def gen_bombs(self, x=1, y=1, level=1):
		num = self._num_of_bombs(x, y, level)
		count = 0
		points = set()

		while count != num:
			point = randint(0, x), randint(0, y)

			if point not in points:
				points.add(point)
				count += 1

		return points

	def gen_neighbors(self, point):
		x, y = point
		xstart, xend = -1, 2
		ystart, yend = -1, 2

		if x <= 0:
			xstart = 0
		elif x >= self.x:
			xend = 1

		if y <= 0:
			ystart = 0
		elif y >= self.y:
			yend = 1

		nearby = {(x + x_i, y + y_i) for x_i in range(xstart, xend) for y_i in range(ystart, yend)}
		nearby.remove(point)

		return nearby

	def gen_numbers(self, x=1, y=1, board=set()):
		points = {(_x, _y) for _x in range(x+1) for _y in range(y+1)}
		numbers = dict()

		for point in points:
			if point in board:
				continue

			nearby = sum(neighbor in board for neighbor in self.gen_neighbors(point))

			if not nearby:
				continue

			numbers[point] = nearby

		return numbers, points

	def select_sq(self, point):
		if point not in self.unclicked_squares:
			return

		self.unclicked_squares.remove(point)

		if point in self.bombs:
			self.end_game(False)
			return

		elif point in self.numbers:
			return

		else:
			self._pop_consec_zero_sqs(point)


	def set_flag(self, pt):
		if pt in self.flags:
			self.flags.remove(pt)
			self.unclicked_squares.add(pt)
			return True

		elif pt in self.unclicked_squares:
			self.flags.add(pt)

			used_all_flags = len(self.flags) == len(self.bombs)

			if used_all_flags and (self.flags == self.bombs):
				self.end_game(True)

			return False

	def start_game(self):
		if not self.start:
			self.start = True
			self.win = False

		self.round += 1


	def end_game(self, win=False):
		self.win = win
		self.unclicked_squares = set()
		self.start = False


def main():
	b = Board(10, 10, 1)

if __name__ == "__main__":
	main()
