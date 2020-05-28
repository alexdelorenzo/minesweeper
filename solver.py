__author__ = 'alex'
from board import Board
from random import randint

class Solver(object):
	def __init__(self):
		self.board = Board(13, 13)

	def random_pt(self):
		return randint(0,13), randint(0,13)



class Cases(object):
	def __init__(self):
		pass

	def _get_clicked_sqs(self, board: Board) -> set:
		return board.unclicked_squares - board.blank

	def _get_visible_nums(self, board: Board) -> set:
		return board.unclicked_squares - set(board.numbers)

	def _get_zero_sqs(self, board: Board) -> set:
		return self._get_visible_nums(board) - self._get_clicked_sqs(board)

	def _get_mapped_neighbors(self, board: Board, pt: tuple) -> set:
		neighbors = board.gen_neighbors(pt)
		mapped_neighbors = {neighbor: pt  for neighbor in neighbors}
		pass

	def _get_edges(self, board, pt, neighbors=None):
		if not neighbors:
			neighbors = board.gen_neighbors(pt)

		x, y = pt
		xinterval, yinterval = (x-1, x, x+1), (y-1, y, y+1)


		edges = left, right, top, bottom = \
			{(x-1, yi) for yi in yinterval}, \
			{(x+1, yi) for yi in yinterval}, \
			{(xi, y+1) for xi in xinterval}, \
			{(xi, y-1) for xi in xinterval}

		return edges

	def _is_on_soft_edge(self, board: Board, pt: tuple, neighbors=None, edges=None) -> bool:
		if not neighbors:
			neighbors = board.gen_neighbors(pt)

		if not edges:
			edges = self._get_edges(board, pt, neighbors)

		#intersection of visible zeros and neighbors
		zero_sqs = self._get_zero_sqs(board)
		zero_neighbors = zero_sqs & neighbors

		# check if 3-consec pts are subsets of zero_neighbors, bools
		return any(edge < zero_neighbors for edge in edges)

	def _is_on_edge(self, board: Board, pt: tuple, neighbors=None, edges=None) -> bool:
		if not neighbors:
			neighbors = board.gen_neighbors(pt)

		if len(neighbors) <= 5:
			return True

		if not edges:
			edges = self._get_edges(board, pt, neighbors)

		return self._is_on_soft_edge(board, pt, neighbors, edges)

	def basic_patterns(self, board: Board, pt) -> None:
		if pt in board.numbers:
			bombs = board.numbers[pt]
			neighbors = board.gen_neighbors(pt)

			open_neighbors = neighbors & board.unclicked_squares

			if len(open_neighbors) == bombs:
				for neighbor in neighbors:
					board.select_sq(neighbor)
					self.basic_patterns(neighbor)

	def edge_one_one(self, board: Board, pt, neighbors=None) -> None:
		if not neighbors:
			neighbors = board.gen_neighbors(pt)

		has_edge = self._is_on_edge(board, pt, neighbors)

		if not has_edge:
			return False









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
