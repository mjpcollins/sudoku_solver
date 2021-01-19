from unittest import TestCase
from utils import Solver
import numpy as np
from numpy.testing import assert_array_equal


class TestSolver(TestCase):

    def setUp(self):
        self.puzzles = {"very_easy": {"puzzles": np.load("data/very_easy_puzzle.npy"),
                                      "solutions": np.load("data/very_easy_solution.npy")},
                        "easy": {"puzzles": np.load("data/easy_puzzle.npy"),
                                 "solutions": np.load("data/easy_solution.npy")},
                        "medium": {"puzzles": np.load("data/medium_puzzle.npy"),
                                   "solutions": np.load("data/medium_solution.npy")},
                        "hard": {"puzzles": np.load("data/hard_puzzle.npy"),
                                 "solutions": np.load("data/hard_solution.npy")}}
        self.hard_sudoku = Solver(self.puzzles["hard"]["puzzles"][4])

    def test_solve_very_easy(self):
        self.solve("very_easy")

    def test_solve_easy(self):
        self.solve("easy")

    def test_solve_medium(self):
        self.solve("medium")

    def test_solve_one_hard(self):
        assert_array_equal(self.hard_sudoku.solve(), self.puzzles["hard"]["solutions"][4])

    def solve(self, difficulty):
        for index, puzzle in enumerate(self.puzzles[difficulty]["puzzles"]):
            solver = Solver(puzzle)
            assert_array_equal(solver.solve(), self.puzzles[difficulty]["solutions"][index])

