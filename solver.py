__author__ = 'alex'
from board import Board
from random import randint

class Solver(object):
	def __init__(self):
		self.board = Board(13, 13)

	def random_pt(self):
		return randint(0,13), randint(0,13)

	def basic_patterns(self, pt):
		if pt in self.board.numbers:
			bombs = self.board.numbers[pt]
			neighbors = self.board.gen_neighbors(pt)

			open_neighbors = sum(neighbor in self.board.unclicked_squares for neighbor in neighbors)

			if open_neighbors == bombs:
				for neighbor in neighbors:
					self.board.select_sq(neighbor)
					self.basic_patterns(neighbor)


def main():
	s = Solver()
	pt = s.random_pt()
	s.basic_patterns(pt)
	pt = s.random_pt()
	s.basic_patterns(pt)
	pt = s.random_pt()
	s.basic_patterns(pt)


if __name__ == "__main__":
	main()