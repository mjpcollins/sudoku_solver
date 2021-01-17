from unittest import TestCase
from utils.sudoku_puzzle import SudokuPuzzle
from utils.vertex import Vertex
import numpy as np
from numpy.testing import assert_array_equal


class TestSudokuPuzzle(TestCase):

    def setUp(self):
        self.input_puzzle = np.array([[0, 3, 0, 0],
                                      [0, 0, 0, 0],
                                      [0, 0, 0, 0],
                                      [0, 0, 0, 0]], dtype=int)
        self.puzzle = SudokuPuzzle(self.input_puzzle)

    def test_init(self):
        self.assertEqual(4, self.puzzle._size)
        self.assertEqual("<class 'utils.graph.Graph'>", str(type(self.puzzle._graph)))
        self.assertEqual(16, len(self.puzzle._graph.vertexes))
        assert_array_equal(self.input_puzzle, self.puzzle._puzzle_array)

    def test_get_values(self):
        self.puzzle.set_value((0, 0),
                              value=2)
        self.puzzle.set_value((1, 2),
                              value=2)
        expected_array = np.array([[2, 3, 0, 0],
                                   [0, 0, 2, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]], dtype=int)
        actual_array = self.puzzle.get_values()
        assert_array_equal(expected_array, actual_array)

    def test_get_possible_values(self):
        self.puzzle.set_value((0, 0),
                              value=2)
        self.puzzle.set_value((1, 2),
                              value=2)
        expected_dict = {(0, 0): {2}, (0, 1): {3}, (0, 2): {1, 4}, (0, 3): {1, 4}, (1, 0): {1, 4}, (1, 1): {1, 4}, (1, 2): {2}, (1, 3): {1, 3, 4}, (2, 0): {1, 3, 4}, (2, 1): {1, 2, 3, 4}, (2, 2): {1, 3, 4}, (2, 3): {1, 2, 3, 4}, (3, 0): {1, 3, 4}, (3, 1): {1, 2, 3, 4}, (3, 2): {1, 3, 4}, (3, 3): {1, 2, 3, 4}}
        actual_dict = self.puzzle.get_possible_values()
        self.assertEqual(expected_dict, actual_dict)

    def test_is_solved(self):
        self.assertEqual(False, self.puzzle.is_solved())
        self.puzzle._graph.vertexes = {(0, 0): Vertex([1], (0, 0), self.puzzle._graph),
                                       (0, 1): Vertex([2], (0, 1), self.puzzle._graph),
                                       (0, 2): Vertex([3], (0, 2), self.puzzle._graph),
                                       (0, 3): Vertex([4], (0, 3), self.puzzle._graph),

                                       (1, 0): Vertex([3], (1, 0), self.puzzle._graph),
                                       (1, 1): Vertex([4], (1, 1), self.puzzle._graph),
                                       (1, 2): Vertex([2], (1, 2), self.puzzle._graph),
                                       (1, 3): Vertex([1], (1, 3), self.puzzle._graph),

                                       (2, 0): Vertex([2], (2, 0), self.puzzle._graph),
                                       (2, 1): Vertex([1], (2, 1), self.puzzle._graph),
                                       (2, 2): Vertex([4], (2, 2), self.puzzle._graph),
                                       (2, 3): Vertex([3], (2, 3), self.puzzle._graph),

                                       (3, 0): Vertex([4], (3, 0), self.puzzle._graph),
                                       (3, 1): Vertex([3], (3, 1), self.puzzle._graph),
                                       (3, 2): Vertex([1], (3, 2), self.puzzle._graph),
                                       (3, 3): Vertex([2], (3, 3), self.puzzle._graph)}
        self.assertEqual(True, self.puzzle.is_solved())

    def test_yield_possible_moves(self):
        self.puzzle.set_value((0, 0), value=4)
        self.puzzle.set_value((1, 1), value=1)
        self.puzzle.update_unknowns()
        expected_moves = [{'distance': 2, 'index': (0, 2), 'value': 1}, {'distance': 2, 'index': (0, 2), 'value': 2}, {'distance': 3, 'index': (0, 3), 'value': 1}, {'distance': 3, 'index': (0, 3), 'value': 2}, {'distance': 6, 'index': (1, 2), 'value': 3}, {'distance': 6, 'index': (1, 2), 'value': 4}, {'distance': 7, 'index': (1, 3), 'value': 3}, {'distance': 7, 'index': (1, 3), 'value': 4}, {'distance': 8, 'index': (2, 0), 'value': 1}, {'distance': 8, 'index': (2, 0), 'value': 3}, {'distance': 9, 'index': (2, 1), 'value': 2}, {'distance': 9, 'index': (2, 1), 'value': 4}, {'distance': 10, 'index': (2, 2), 'value': 1}, {'distance': 10, 'index': (2, 2), 'value': 2}, {'distance': 10, 'index': (2, 2), 'value': 3}, {'distance': 10, 'index': (2, 2), 'value': 4}, {'distance': 11, 'index': (2, 3), 'value': 1}, {'distance': 11, 'index': (2, 3), 'value': 2}, {'distance': 11, 'index': (2, 3), 'value': 3}, {'distance': 11, 'index': (2, 3), 'value': 4}, {'distance': 12, 'index': (3, 0), 'value': 1}, {'distance': 12, 'index': (3, 0), 'value': 3}, {'distance': 13, 'index': (3, 1), 'value': 2}, {'distance': 13, 'index': (3, 1), 'value': 4}, {'distance': 14, 'index': (3, 2), 'value': 1}, {'distance': 14, 'index': (3, 2), 'value': 2}, {'distance': 14, 'index': (3, 2), 'value': 3}, {'distance': 14, 'index': (3, 2), 'value': 4}, {'distance': 15, 'index': (3, 3), 'value': 1}, {'distance': 15, 'index': (3, 3), 'value': 2}, {'distance': 15, 'index': (3, 3), 'value': 3}, {'distance': 15, 'index': (3, 3), 'value': 4}]
        self.assertEqual(expected_moves, self.puzzle.get_all_possible_moves())

    def test_lowest_empty_cell(self):
        self.puzzle.set_value((0, 0), value=4)
        self.puzzle.set_value((1, 1), value=1)
        self.assertEqual({"index": (0, 2), "distance": 2}, self.puzzle.lowest_empty_cell())

    def test_lowest_empty_cell_no_zeros(self):

        self.puzzle._graph.vertexes = {(0, 0): Vertex([1], (0, 0), self.puzzle._graph),
                                       (0, 1): Vertex([2], (0, 1), self.puzzle._graph),
                                       (0, 2): Vertex([3], (0, 2), self.puzzle._graph),
                                       (0, 3): Vertex([4], (0, 3), self.puzzle._graph),

                                       (1, 0): Vertex([3], (1, 0), self.puzzle._graph),
                                       (1, 1): Vertex([4], (1, 1), self.puzzle._graph),
                                       (1, 2): Vertex([2], (1, 2), self.puzzle._graph),
                                       (1, 3): Vertex([1], (1, 3), self.puzzle._graph),

                                       (2, 0): Vertex([2], (2, 0), self.puzzle._graph),
                                       (2, 1): Vertex([1], (2, 1), self.puzzle._graph),
                                       (2, 2): Vertex([4], (2, 2), self.puzzle._graph),
                                       (2, 3): Vertex([3], (2, 3), self.puzzle._graph),

                                       (3, 0): Vertex([4], (3, 0), self.puzzle._graph),
                                       (3, 1): Vertex([3], (3, 1), self.puzzle._graph),
                                       (3, 2): Vertex([1], (3, 2), self.puzzle._graph),
                                       (3, 3): Vertex([2], (3, 3), self.puzzle._graph)}
        self.assertEqual(None, self.puzzle.lowest_empty_cell())

    def test_copy(self):
        self.puzzle.set_value((0, 1),
                              value=3)
        new_graph = self.puzzle.copy()
        assert_array_equal(self.puzzle.get_values(), new_graph.get_values())
        new_graph.set_value((2, 0),
                            value=4)
        expected_array_org = np.array([[0, 3, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0]], dtype=int)
        expected_array_copy = np.array([[0, 3, 0, 0],
                                        [0, 0, 0, 0],
                                        [4, 0, 0, 0],
                                        [0, 0, 0, 0]], dtype=int)
        assert_array_equal(expected_array_org, self.puzzle.get_values())
        assert_array_equal(expected_array_copy,  new_graph.get_values())
        expected_neighbours_for_0_0 = {((1), (0)),
                                       ((1), (1)),
                                       ((0), (1)),
                                       ((0), (2)),
                                       ((0), (3)),
                                       ((2), (0)),
                                       ((3), (0))}
        actual_neighbours = new_graph._graph.vertexes[(0, 0)].get_neighbours()
        self.assertEqual(expected_neighbours_for_0_0, actual_neighbours)

    def test_init_values(self):
        input_puzzle = np.array([[0, 3, 0, 0],
                                 [0, 0, 0, 0],
                                 [4, 0, 0, 0],
                                 [0, 0, 0, 0]], dtype=int)
        puzzle = SudokuPuzzle(input_puzzle)
        assert_array_equal(input_puzzle, puzzle.get_values())

    def test_update_unknowns(self):
        input_puzzle = np.array([[1, 3, 0, 0],
                                 [2, 0, 0, 0],
                                 [4, 0, 0, 0],
                                 [0, 0, 0, 0]], dtype=int)
        expected_puzzle = np.array([[1, 3, 0, 0],
                                    [2, 4, 0, 0],
                                    [4, 0, 0, 0],
                                    [3, 0, 0, 0]], dtype=int)
        puzzle = SudokuPuzzle(input_puzzle)
        puzzle.update_unknowns()
        assert_array_equal(expected_puzzle, puzzle.get_values())
