from unittest import TestCase
from utils.graph import Graph
from utils.vertex import Vertex
import itertools


class TestGraph(TestCase):

    def setUp(self):
        self._possible_cell_values = {1, 2, 3, 4}
        self._size = 4
        self.graph = Graph(size=self._size,
                           possible_values=self._possible_cell_values)
        self.expected_neighbours_for_0_0 = {(1, 0),
                                            (1, 1),
                                            (0, 1),
                                            (0, 2),
                                            (0, 3),
                                            (2, 0),
                                            (3, 0)}

    def test_init(self):
        self.assertEqual(4, self.graph._size)
        self.assertEqual({1, 2, 3, 4}, self.graph._possible_cell_values)
        self.assertEqual("<class 'dict'>", str(type(self.graph.vertexes)))
        self.assertEqual(16, len(self.graph.vertexes))

    def test_create_graph(self):
        for vertex in self.graph.vertexes.values():
            self.assertEqual({1, 2, 3, 4}, vertex.possible_values)

    def test_set_value(self):
        self.graph.set_value((0, 0), 3)
        self.assertEqual({3}, self.graph.vertexes[(0, 0)].possible_values)
        self.assertEqual(True, self.graph.vertexes[(0, 0)].solved)
        for neighbour in self.expected_neighbours_for_0_0:
            self.assertEqual({1, 2, 4}, self.graph.vertexes[neighbour].possible_values)
            self.assertEqual(False, self.graph.vertexes[neighbour].solved)

    def test_quick_set_value(self):
        self.graph.quick_set_value((0, 0), 3)
        self.assertEqual({3}, self.graph.vertexes[(0, 0)].possible_values)
        self.assertEqual(True, self.graph.vertexes[(0, 0)].solved)
        for neighbour in self.expected_neighbours_for_0_0:
            self.assertEqual({1, 2, 3, 4}, self.graph.vertexes[neighbour].possible_values)
            self.assertEqual(False, self.graph.vertexes[neighbour].solved)

    def test_raises_value_error_on_no_solutions(self):
        self.graph.set_value((0, 0), 1)
        self.graph.set_value((1, 1), 2)
        self.graph.set_value((3, 1), 3)
        with self.assertRaises(ValueError):
            self.graph.set_value((2, 2), 1)

    def test_update(self):
        self.graph.quick_set_value((0, 0), 3)
        for neighbour_index in self.expected_neighbours_for_0_0:
            neighbour = self.graph.vertexes[neighbour_index]
            self.assertEqual({1, 2, 3, 4}, neighbour.possible_values)
            self.assertEqual(False, neighbour.solved)
        self.graph.update()
        for neighbour_index in self.expected_neighbours_for_0_0:
            neighbour = self.graph.vertexes[neighbour_index]
            self.assertEqual({1, 2, 4}, neighbour.possible_values)
            self.assertEqual(False, neighbour.solved)

    def get_unlinked_graph(self):
        graph = Graph(size=self._size)
        graph.vertexes = {}
        for vertex_id in itertools.product(range(self._size), range(self._size)):
            graph.vertexes[vertex_id] = Vertex(self._possible_cell_values,
                                               vertex_id=vertex_id,
                                               graph=graph)
        return graph
