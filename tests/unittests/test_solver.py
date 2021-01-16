from unittest import TestCase
from utils import Solver
import numpy as np
from numpy.testing import assert_array_equal


class TestSolver(TestCase):

    def setUp(self):
        self.first_v_easy_puzzle = np.load("data/very_easy_puzzle.npy")[0]
        self.first_v_easy_solution = np.load("data/very_easy_solution.npy")[0]
        self.solver = Solver(puzzle=self.first_v_easy_puzzle)

    def test_init(self):
        assert_array_equal(self.first_v_easy_puzzle, self.solver._puzzle)
        self.assertEqual(9, self.solver._settings["rows"])
        self.assertEqual(9, self.solver._settings["columns"])
        self.assertEqual(3, self.solver._settings["sub_box_height"])
        self.assertEqual(3, self.solver._settings["sub_box_width"])
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], self.solver._settings["possible_cell_values"])
        self.assertEqual((9, 9), self.solver._graph._graph.shape)
        print(self.first_v_easy_puzzle)

    def test_set_starting_values(self):
        """"[[1 0 4 3 8 2 9 5 6]
             [2 0 5 4 6 7 1 3 8]
             [3 8 6 9 5 1 4 0 2]
             [4 6 1 5 2 3 8 9 7]
             [7 3 8 1 4 9 6 2 5]
             [9 5 2 8 7 6 3 1 4]
             [5 2 9 6 3 4 7 8 1]
             [6 0 7 2 9 8 5 4 3]
             [8 4 3 0 1 5 2 6 9]]"""

        expected_array = np.array([[1, 0, 4, 3, 8, 2, 9, 5, 6],
                                   [2, 0, 5, 4, 6, 7, 1, 3, 8],
                                   [3, 8, 6, 9, 5, 1, 4, 0, 2],
                                   [4, 6, 1, 5, 2, 3, 8, 9, 7],
                                   [7, 3, 8, 1, 4, 9, 6, 2, 5],
                                   [9, 5, 2, 8, 7, 6, 3, 1, 4],
                                   [5, 2, 9, 6, 3, 4, 7, 8, 1],
                                   [6, 0, 7, 2, 9, 8, 5, 4, 3],
                                   [8, 4, 3, 0, 1, 5, 2, 6, 9]], dtype=int)
        actual_array = self.solver._graph.get_values()
        print(actual_array)


    # def test_solver_very_easy(self):
    #     actual_solution = self.solver.solve(self.v_easy_puzzle)
    #     assert_array_equal(self.v_easy_solution, actual_solution)
