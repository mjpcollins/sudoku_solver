from unittest import TestCase, mock
from utils import Graph, Vertex
import numpy as np
from numpy.testing import assert_array_equal
import io


class TestGraph(TestCase):

    def setUp(self):
        self._possible_cell_values = {1, 2, 3, 4}
        self._settings = {"rows": 4,
                          "columns": 4,
                          "sub_box_height": 2,
                          "sub_box_width": 2,
                          "possible_cell_values": self._possible_cell_values}
        self.graph = Graph(self._settings)
        self.expected_neighbours_for_0_0 = {self.graph._graph[1][0],
                                            self.graph._graph[1][1],
                                            self.graph._graph[0][1],
                                            self.graph._graph[0][2],
                                            self.graph._graph[0][3],
                                            self.graph._graph[2][0],
                                            self.graph._graph[3][0]}

    def test_init(self):
        self.assertEqual(4, self.graph._rows)
        self.assertEqual(4, self.graph._columns)
        self.assertEqual(2, self.graph._sub_box_height)
        self.assertEqual(2, self.graph._sub_box_width)

    def test_params_work(self):
        pass

    def test_create_graph(self):
        for cell in self.graph._graph.flat:
            self.assertEqual({1, 2, 3, 4}, cell.get_values())

    def test_link_rows(self):
        self.graph._graph = self.graph._create_graph(self._possible_cell_values)
        self.graph._link_rows()
        for row in self.graph._graph:
            for cell in row:
                expected_neighbours = set(row)
                expected_neighbours.remove(cell)
                self.assertEqual(expected_neighbours, cell.get_neighbours())

    def test_link_columns(self):
        self.graph._graph = self.graph._create_graph(self._possible_cell_values)
        self.graph._link_columns()
        for column in self.graph._graph.T:
            for cell in column:
                expected_neighbours = set(column)
                expected_neighbours.remove(cell)
                self.assertEqual(expected_neighbours, cell.get_neighbours())

    def test_link_sub_boxes(self):
        self.graph._graph = self.graph._create_graph(self._possible_cell_values)
        self.graph._link_sub_boxes()
        expected_neighbours = {self.graph._graph[1][0],
                               self.graph._graph[1][1],
                               self.graph._graph[0][1]}
        actual_neighbours = (self.graph._graph[0][0].get_neighbours())
        self.assertEqual(expected_neighbours, actual_neighbours)

    def test_link_all_in_set(self):
        v1 = Vertex([1, 2])
        v2 = Vertex([3, 2])
        v3 = Vertex([5, 2])
        self.graph._link_all_in_set({v1, v2, v3})
        self.assertEqual({v2, v3}, v1.get_neighbours())
        self.assertEqual({v1, v3}, v2.get_neighbours())
        self.assertEqual({v1, v2}, v3.get_neighbours())

    def test_link_all(self):
        self.graph._link_all()
        actual_neighbours = self.graph._graph[0][0].get_neighbours()
        self.assertEqual(self.expected_neighbours_for_0_0, actual_neighbours)

    def test_rule_out_values(self):
        self.graph.rule_out_values(0, 0, {2, 3})
        self.assertEqual({1, 4}, self.graph._graph[0][0].get_values())
        self.assertEqual(False, self.graph._graph[0][0].is_solved())

    def test_set_value(self):
        self.graph.set_value(0, 0, 3)
        self.assertEqual({3}, self.graph._graph[0][0].get_values())
        self.assertEqual(True, self.graph._graph[0][0].is_solved())
        expected_remaining_possible_values = {1, 2, 4}
        for neighbour in self.expected_neighbours_for_0_0:
            self.assertEqual(expected_remaining_possible_values,
                             neighbour.get_values())
            self.assertEqual(False, neighbour.is_solved())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print(self, mock_stdout):
        print(self.graph)
        expected_str = "[[{1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4}]\n" \
                       " [{1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4}]\n" \
                       " [{1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4}]\n" \
                       " [{1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4}]]\n"
        self.assertEqual(expected_str, mock_stdout.getvalue())

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_value_values_set(self, mock_stdout):
        self.graph.set_value(row=0,
                             column=0,
                             value=2)
        self.graph.set_value(row=1,
                             column=2,
                             value=2)
        print(self.graph)
        expected_str = "[[{2} {1, 3, 4} {1, 3, 4} {1, 3, 4}]\n" \
                       " [{1, 3, 4} {1, 3, 4} {2} {1, 3, 4}]\n" \
                       " [{1, 3, 4} {1, 2, 3, 4} {1, 3, 4} {1, 2, 3, 4}]\n" \
                       " [{1, 3, 4} {1, 2, 3, 4} {1, 3, 4} {1, 2, 3, 4}]]\n"
        self.assertEqual(expected_str, mock_stdout.getvalue())

    def test_get_values(self):
        self.graph.set_value(row=0,
                             column=0,
                             value=2)
        self.graph.set_value(row=1,
                             column=2,
                             value=2)
        expected_array = np.array([[2, 0, 0, 0],
                                   [0, 0, 2, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]], dtype=int)
        actual_array = self.graph.get_values()
        assert_array_equal(expected_array, actual_array)

    def test_is_solved(self):
        self.assertEqual(False, self.graph.is_solved())
        self.graph._graph = np.array([[Vertex([1]), Vertex([2]), Vertex([3]), Vertex([4])],
                                      [Vertex([3]), Vertex([4]), Vertex([2]), Vertex([1])],
                                      [Vertex([2]), Vertex([1]), Vertex([4]), Vertex([3])],
                                      [Vertex([4]), Vertex([3]), Vertex([1]), Vertex([2])]], dtype=object)
        self.assertEqual(True, self.graph.is_solved())

    def test_no_solutions(self):
        self.assertEqual(False, self.graph._impossible)
        self.graph.no_solutions()
        expected_array = np.array([[-1, -1, -1, -1],
                                   [-1, -1, -1, -1],
                                   [-1, -1, -1, -1],
                                   [-1, -1, -1, -1]], dtype=int)
        assert_array_equal(expected_array, self.graph.get_values())
        self.assertEqual(True, self.graph._impossible)

    def test_yield_possible_moves(self):
        self.graph.set_value(row=0,
                             column=0,
                             value=4)
        self.graph.set_value(row=1,
                             column=2,
                             value=1)
        expected_moves = [{'index': (0, 1), 'value': 1}, {'index': (0, 1), 'value': 2}, {'index': (0, 1), 'value': 3}, {'index': (0, 2), 'value': 2}, {'index': (0, 2), 'value': 3}, {'index': (0, 3), 'value': 2}, {'index': (0, 3), 'value': 3}, {'index': (1, 0), 'value': 2}, {'index': (1, 0), 'value': 3}, {'index': (1, 1), 'value': 2}, {'index': (1, 1), 'value': 3}, {'index': (1, 3), 'value': 2}, {'index': (1, 3), 'value': 3}, {'index': (1, 3), 'value': 4}, {'index': (2, 0), 'value': 1}, {'index': (2, 0), 'value': 2}, {'index': (2, 0), 'value': 3}, {'index': (2, 1), 'value': 1}, {'index': (2, 1), 'value': 2}, {'index': (2, 1), 'value': 3}, {'index': (2, 1), 'value': 4}, {'index': (2, 2), 'value': 2}, {'index': (2, 2), 'value': 3}, {'index': (2, 2), 'value': 4}, {'index': (2, 3), 'value': 1}, {'index': (2, 3), 'value': 2}, {'index': (2, 3), 'value': 3}, {'index': (2, 3), 'value': 4}, {'index': (3, 0), 'value': 1}, {'index': (3, 0), 'value': 2}, {'index': (3, 0), 'value': 3}, {'index': (3, 1), 'value': 1}, {'index': (3, 1), 'value': 2}, {'index': (3, 1), 'value': 3}, {'index': (3, 1), 'value': 4}, {'index': (3, 2), 'value': 2}, {'index': (3, 2), 'value': 3}, {'index': (3, 2), 'value': 4}, {'index': (3, 3), 'value': 1}, {'index': (3, 3), 'value': 2}, {'index': (3, 3), 'value': 3}, {'index': (3, 3), 'value': 4}]
        actual_moves = [move for move in self.graph.yield_possible_moves()]
        actual_moves.sort(key=lambda x: (x["index"], x["value"]))
        self.assertEqual(expected_moves, actual_moves)

    def test_copy(self):
        self.graph.set_value(row=0,
                             column=1,
                             value=3)
        new_graph = self.graph.copy()
        assert_array_equal(self.graph.get_values(), new_graph.get_values())
        new_graph.set_value(row=2,
                            column=0,
                            value=4)
        expected_array_org = np.array([[0, 3, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0],
                                       [0, 0, 0, 0]], dtype=int)
        expected_array_copy = np.array([[0, 3, 0, 0],
                                        [0, 0, 0, 0],
                                        [4, 0, 0, 0],
                                        [0, 0, 0, 0]], dtype=int)
        assert_array_equal(expected_array_org, self.graph.get_values())
        assert_array_equal(expected_array_copy,  new_graph.get_values())

        expected_neighbours_for_0_0 = {new_graph._graph[1][0],
                                       new_graph._graph[1][1],
                                       new_graph._graph[0][1],
                                       new_graph._graph[0][2],
                                       new_graph._graph[0][3],
                                       new_graph._graph[2][0],
                                       new_graph._graph[3][0]}
        actual_neighbours = new_graph._graph[0][0].get_neighbours()
        self.assertEqual(expected_neighbours_for_0_0, actual_neighbours)

    def test_init_values(self):
        input_puzzle = np.array([[0, 3, 0, 0],
                                 [0, 0, 0, 0],
                                 [4, 0, 0, 0],
                                 [0, 0, 0, 0]], dtype=int)
        self.graph.init_values(input_puzzle)
        assert_array_equal(input_puzzle, self.graph.get_values())

    def test_setup_set_value(self):
        init_state = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]], dtype=int)
        expected_state = np.array([[1, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0],
                                   [0, 0, 0, 0]], dtype=int)
        assert_array_equal(init_state, self.graph.get_values())
        self.graph.setup_set_value(row=0,
                                   column=0,
                                   value=1)
        assert_array_equal(expected_state, self.graph.get_values())
