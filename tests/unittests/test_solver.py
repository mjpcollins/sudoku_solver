from unittest import TestCase
from utils import Solver
import numpy as np
from numpy.testing import assert_array_equal


class TestSolver(TestCase):

    def setUp(self):
        self.first_v_easy_puzzle = np.load("data/very_easy_puzzle.npy")[0]
        self.first_v_easy_solution = np.load("data/very_easy_solution.npy")[0]
        self.v_easy_solver = Solver(puzzle=self.first_v_easy_puzzle)

        self.first_easy_puzzle = np.load("data/easy_puzzle.npy")[0]
        self.first_easy_solution = np.load("data/easy_solution.npy")[0]
        self.easy_solver = Solver(puzzle=self.first_easy_puzzle)

        self.first_medium_puzzle = np.load("data/medium_puzzle.npy")[0]
        self.first_medium_solution = np.load("data/medium_solution.npy")[0]
        self.medium_solver = Solver(puzzle=self.first_medium_puzzle)

        self.first_hard_puzzle = np.load("data/hard_puzzle.npy")[0]
        self.first_hard_solution = np.load("data/hard_solution.npy")[0]
        self.hard_solver = Solver(puzzle=self.first_hard_puzzle)

    def test_init(self):
        assert_array_equal(self.first_v_easy_puzzle, self.v_easy_solver._puzzle)
        assert_array_equal((9, 9), self.v_easy_solver._shape)
        self.assertEqual(9, self.v_easy_solver._settings["rows"])
        self.assertEqual(9, self.v_easy_solver._settings["columns"])
        self.assertEqual(3, self.v_easy_solver._settings["sub_box_height"])
        self.assertEqual(3, self.v_easy_solver._settings["sub_box_width"])
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], self.v_easy_solver._settings["possible_cell_values"])
        self.assertEqual((9, 9), self.v_easy_solver._graph._graph.shape)

    def test_quick_parse(self):
        self.v_easy_solver._quick_parse()
        assert_array_equal(self.first_v_easy_solution, self.v_easy_solver._graph.get_values())

    def test_solver_very_easy(self):
        actual_solution = self.v_easy_solver.solve()
        assert_array_equal(self.first_v_easy_solution, actual_solution)

    def test_solver_easy(self):
        actual_solution = self.easy_solver.solve()
        assert_array_equal(self.first_easy_solution, actual_solution)

    def test_solver_medium(self):
        actual_solution = self.medium_solver.solve()
        assert_array_equal(self.first_medium_solution, actual_solution)

    def test_solver_hard(self):
        actual_solution = self.hard_solver.solve()
        assert_array_equal(self.first_hard_solution, actual_solution)
