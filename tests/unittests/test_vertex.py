from unittest import TestCase
from utils import Vertex, Graph


class TestVertex(TestCase):

    def setUp(self):
        self.graph = Graph(4, init=False,
                           possible_values={1, 2, 3, 4, 7, 5, 9})
        self.graph.vertexes = {
            (0, 0): Vertex({1, 2, 3}, (0, 0), self.graph),
            (0, 1): Vertex({1, 3, 7}, (0, 1), self.graph),
            (1, 0): Vertex({1, 5, 9}, (1, 0), self.graph),
            (0, 2): Vertex({1}, (0, 2), self.graph),
            (1, 1): Vertex({2}, (1, 1), self.graph)
        }

        self.vertex = self.graph.vertexes[(0, 0)]
        self.solved_vertex = self.graph.vertexes[(1, 1)]
        self.solved_vertex_2 = self.graph.vertexes[(0, 2)]
        self.neighbour_vertex = self.graph.vertexes[(0, 1)]
        self.other_neighbour_vertex = self.graph.vertexes[(1, 0)]

    def test_init(self):
        self.assertEqual({1, 2, 3}, self.vertex.possible_values)
        self.assertEqual(set(), self.vertex.neighbours)
        self.assertEqual(False, self.vertex.solved)
        self.assertEqual(True, self.graph.vertexes[(1, 1)].solved)

    def test_set_neighbours_one_by_one(self):
        self.vertex.add_neighbours({self.neighbour_vertex.id})
        self.assertEqual({self.neighbour_vertex.id}, self.vertex.neighbours)
        self.vertex.add_neighbours({self.other_neighbour_vertex.id})
        self.assertEqual({self.neighbour_vertex.id, self.other_neighbour_vertex.id}, self.vertex.neighbours)

    def test_set_neighbours(self):
        self.vertex.add_neighbours({self.neighbour_vertex.id,
                                    self.other_neighbour_vertex.id})
        self.assertEqual({self.neighbour_vertex.id,
                          self.other_neighbour_vertex.id}, self.vertex.neighbours)

    def test_set_solved_neighbours(self):
        self.vertex.add_neighbours({self.solved_vertex_2.id})
        self.vertex.resolve_neighbours()
        self.assertEqual({2, 3}, self.vertex.possible_values)
        self.assertEqual(False, self.vertex.solved)
        self.vertex.add_neighbours({self.solved_vertex.id})
        self.vertex.resolve_neighbours()
        self.assertEqual({3}, self.vertex.possible_values)
        self.assertEqual(True, self.vertex.solved)

    def test_check_solved(self):
        self.assertEqual(False, self.vertex._check_solved())
        self.vertex.possible_values = {1}
        self.assertEqual(True, self.vertex._check_solved())

    def test_get_possible_values(self):
        self.assertEqual({1, 2, 3}, self.vertex.possible_values)
        self.vertex.possible_values = {1}
        self.assertEqual({1}, self.vertex.possible_values)

    def test_resolve_neighbours(self):
        self.vertex.neighbours.add(self.solved_vertex.id),
        self.vertex.neighbours.add(self.solved_vertex_2.id)
        self.assertEqual({1, 2 ,3}, self.vertex.possible_values)
        self.assertEqual(False, self.vertex.solved)
        self.vertex.resolve_neighbours()
        self.assertEqual({3}, self.vertex.possible_values)
        self.assertEqual(True, self.vertex.solved)

    def test_no_solutions(self):
        self.vertex.possible_values.discard(3)
        self.vertex.add_neighbours({self.solved_vertex.id, self.solved_vertex_2.id})
        with self.assertRaises(ValueError):
            self.vertex.resolve_neighbours()

    def test_update_neighbours(self):
        self.vertex.add_neighbours({self.neighbour_vertex.id, self.other_neighbour_vertex.id})
        self.other_neighbour_vertex.add_neighbours({self.neighbour_vertex.id, self.vertex.id})
        self.neighbour_vertex.add_neighbours({self.vertex.id, self.other_neighbour_vertex.id})
        self.vertex.possible_values = {1}
        self.vertex._check_solved()
        self.vertex.update_neighbours()
        self.assertEqual({3, 7}, self.neighbour_vertex.possible_values)
        self.assertEqual({5, 9}, self.other_neighbour_vertex.possible_values)

    def test_alert_neighbours_after_solve(self):
        self.vertex.neighbours = {self.neighbour_vertex.id, self.other_neighbour_vertex.id}
        self.other_neighbour_vertex.neighbours = {self.neighbour_vertex.id, self.vertex.id}
        self.neighbour_vertex.neighbours = {self.vertex.id, self.other_neighbour_vertex.id}
        self.vertex.set_vertex_value(1)
        self.assertEqual({3, 7}, self.neighbour_vertex.possible_values)
        self.assertEqual({5, 9}, self.other_neighbour_vertex.possible_values)
