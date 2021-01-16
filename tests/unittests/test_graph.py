from unittest import TestCase, mock
from utils import Graph, Vertex
import io


class TestGraph(TestCase):

    def setUp(self):
        self._settings = {"rows": 4,
                          "columns": 4,
                          "sub_box_height": 2,
                          "sub_box_width": 2,
                          "possible_cell_values": [1, 2, 3, 4]}
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
        self.graph._graph = self.graph._create_graph()
        self.graph._link_rows()
        for row in self.graph._graph:
            for cell in row:
                expected_neighbours = set(row)
                expected_neighbours.remove(cell)
                self.assertEqual(expected_neighbours, cell.get_neighbours())

    def test_link_columns(self):
        self.graph._graph = self.graph._create_graph()
        self.graph._link_columns()
        for column in self.graph._graph.T:
            for cell in column:
                expected_neighbours = set(column)
                expected_neighbours.remove(cell)
                self.assertEqual(expected_neighbours, cell.get_neighbours())

    def test_link_sub_boxes(self):
        self.graph._graph = self.graph._create_graph()
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
        import numpy as np
        from numpy.testing import assert_array_equal
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

