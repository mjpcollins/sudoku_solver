from unittest import TestCase
from utils.graph import Graph
from utils.vertex import Vertex
import itertools


class TestGraph(TestCase):

    def setUp(self):
        self._possible_cell_values = {1, 2, 3, 4}
        self._size = 4
        self.graph = Graph(size=self._size)
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
            self.assertEqual({1, 2, 3, 4}, vertex.get_possible_values())

    # def test_link_rows(self):
    #     import numpy as np
    #     graph = self.get_unlinked_graph()
    #     graph._link(axis=0)
    #     for index, _ in np.ndenumerate(np.zeros(4, 4)):
    #         print(index)

    # def test_link_columns(self):
    #     graph = self.get_unlinked_graph()
    #     graph._link(axis=1)
    #     for column in graph:
    #         for cell in column:
    #             expected_neighbours = set(column)
    #             expected_neighbours.remove(cell)
    #             self.assertEqual(expected_neighbours, cell.get_neighbours())
    #
    # def test_link_sub_boxes(self):
    #     self.graph.vertex_array.flat = [Vertex(self._possible_cell_values) for _ in self.graph.vertex_array.flat]
    #     self.graph._link_sub_boxes()
    #     expected_neighbours = {self.graph.vertex_array[1][0],
    #                            self.graph.vertex_array[1][1],
    #                            self.graph.vertex_array[0][1]}
    #     actual_neighbours = (self.graph.vertex_array[0][0].get_neighbours())
    #     self.assertEqual(expected_neighbours, actual_neighbours)
    #
    # def test_link_all_in_set(self):
    #     graph = self.get_unlinked_graph()
    #     v1 = (1, 2)
    #     v2 = (3, 2)
    #     v3 = (2, 2)
    #     graph._link_all_in_set({v1, v2, v3})
    #     self.assertEqual({v2, v3}, graph.vertexes[v1].get_neighbours())
    #     self.assertEqual({v1, v3}, graph.vertexes[v2].get_neighbours())
    #     self.assertEqual({v1, v2}, graph.vertexes[v3].get_neighbours())
    #
    # def test_link_all(self):
    #     self.graph.vertexes = {}
    #     for vertex_id in itertools.product(range(self._size), range(self._size)):
    #         self.graph.vertexes[vertex_id] = Vertex(self._possible_cell_values,
    #                                                 vertex_id=vertex_id,
    #                                                 graph=self.graph)
    #     self.graph._link_all()
    #     actual_neighbours = self.graph.vertexes[(0, 0)].get_neighbours()
    #     self.assertEqual(self.expected_neighbours_for_0_0, actual_neighbours)

    def test_set_value(self):
        self.graph.set_value((0, 0), 3)
        self.assertEqual({3}, self.graph.vertexes[(0, 0)].get_possible_values())
        self.assertEqual(True, self.graph.vertexes[(0, 0)].is_solved())
        for neighbour in self.expected_neighbours_for_0_0:
            self.assertEqual({1, 2, 4}, self.graph.vertexes[neighbour].get_possible_values())
            self.assertEqual(False, self.graph.vertexes[neighbour].is_solved())

    def test_quick_set_value(self):
        self.graph.quick_set_value((0, 0), 3)
        self.assertEqual({3}, self.graph.vertexes[(0, 0)].get_possible_values())
        self.assertEqual(True, self.graph.vertexes[(0, 0)].is_solved())
        for neighbour in self.expected_neighbours_for_0_0:
            self.assertEqual({1, 2, 3, 4}, self.graph.vertexes[neighbour].get_possible_values())
            self.assertEqual(False, self.graph.vertexes[neighbour].is_solved())

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
            self.assertEqual({1, 2, 3, 4}, neighbour.get_possible_values())
            self.assertEqual(False, neighbour.is_solved())
        self.graph.update()
        for neighbour_index in self.expected_neighbours_for_0_0:
            neighbour = self.graph.vertexes[neighbour_index]
            self.assertEqual({1, 2, 4}, neighbour.get_possible_values())
            self.assertEqual(False, neighbour.is_solved())

    def get_unlinked_graph(self):
        graph = Graph(size=self._size)
        graph.vertexes = {}
        for vertex_id in itertools.product(range(self._size), range(self._size)):
            graph.vertexes[vertex_id] = Vertex(self._possible_cell_values,
                                               vertex_id=vertex_id,
                                               graph=graph)
        return graph
