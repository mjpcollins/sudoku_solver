from utils.sudoku_puzzle import SudokuPuzzle
import numpy as np


class Solver:

    def __init__(self, puzzle):
        self._puzzle = puzzle
        self._sudoku = None
        self._solutions = list()

    def solve(self):
        try:
            solution = self._solve_process()
            if -1 not in solution:
                return solution
        except ValueError:
            pass
        return np.full(self._puzzle.shape, -1)

    def _solve_process(self):
        self._init_puzzle()
        self._sudoku.update_all()

        if self._sudoku.is_solved():
            return self._sudoku.get_values()

        return self._depth_first_algo()

    def _sub_solve_process(self, move):
        try:
            self._sudoku.update_unknowns()
            self._take_move(move)
            if self._sudoku.is_solved():
                return self._sudoku.get_values()
            return self._depth_first_algo()

        except ValueError:
            return {-1}

    def _init_puzzle(self):
        self._sudoku = SudokuPuzzle(puzzle=self._puzzle)

    def _take_move(self, move):
        self._sudoku.set_value(index=move["index"],
                               value=move["value"])

    def _good_moves(self):
        lowest_empty = self._sudoku.lowest_empty_cell()["distance"]
        for move in self._sudoku.get_all_possible_moves():
            if lowest_empty >= move["distance"]:
                yield move

    def _depth_first_algo(self):
        for move in self._good_moves():
            sub_solver = Solver(self._sudoku.get_values().copy())
            sub_solver._sudoku = self._sudoku.copy()
            solution = sub_solver._sub_solve_process(move=move)
            if -1 not in solution:
                return solution
        return {-1}
