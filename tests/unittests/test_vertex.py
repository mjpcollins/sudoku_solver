from unittest import TestCase
from utils import Vertex


class TestVertex(TestCase):

    def setUp(self):
        self.vertex = Vertex([1, 2, 3])
        self.neighbour_vertex = Vertex([1, 3, 7])
        self.other_neighbour_vertex = Vertex([1, 5, 9])
        self.solved_vertex = Vertex([1])
        self.solved_vertex_2 = Vertex([2])

    def test_init(self):
        self.assertEqual({1, 2, 3}, self.vertex._possible_values)
        self.assertEqual(set(), self.vertex._neighbours)
        self.assertEqual(False, self.vertex._solved)
        self.assertEqual(True, self.solved_vertex._solved)

    def test_rule_out(self):
        self.assertEqual({1, 2, 3}, self.vertex._possible_values)
        self.vertex.rule_out({2})
        self.assertEqual({1, 3}, self.vertex._possible_values)

    def test_set_neighbour(self):
        self.assertEqual(set(), self.vertex._neighbours)
        self.vertex.set_neighbour(self.neighbour_vertex)
        self.assertEqual({self.neighbour_vertex}, self.vertex._neighbours)
        self.vertex.set_neighbour(self.other_neighbour_vertex)
        self.assertEqual({self.neighbour_vertex, self.other_neighbour_vertex}, self.vertex._neighbours)

    def test_set_solved_neighbour(self):
        self.vertex.set_neighbour(self.solved_vertex)
        self.assertEqual({2, 3}, self.vertex._possible_values)
        self.assertEqual(False, self.vertex._solved)
        self.vertex.set_neighbour(self.solved_vertex_2)
        self.assertEqual({3}, self.vertex._possible_values)
        self.assertEqual(True, self.vertex._solved)

    def test_get_neighbours(self):
        self.assertEqual(set(), self.vertex.get_neighbours())
        self.vertex._neighbours = {self.neighbour_vertex}
        self.assertEqual({self.neighbour_vertex}, self.vertex.get_neighbours())

    def test_check_solved(self):
        self.assertEqual(False, self.vertex._check_solved())
        self.vertex._possible_values = {1}
        self.assertEqual(True, self.vertex._check_solved())

    def test_is_solved(self):
        self.assertEqual(False, self.vertex.is_solved())
        self.assertEqual(True, self.solved_vertex.is_solved())

    def test_resolve_neighbour(self):
        self.assertEqual({1, 2, 3}, self.vertex._possible_values)
        self.vertex._resolve_neighbour(self.solved_vertex)
        self.assertEqual({2, 3}, self.vertex._possible_values)

    def test_get_values(self):
        self.assertEqual({1, 2, 3}, self.vertex.get_values())
        self.vertex._possible_values = {1}
        self.assertEqual({1}, self.vertex.get_values())

    def test_resolve_neighbours(self):
        self.vertex._neighbours.add(self.solved_vertex)
        self.vertex._neighbours.add(self.solved_vertex_2)
        self.assertEqual({1, 2 ,3}, self.vertex._possible_values)
        self.assertEqual(False, self.vertex._solved)
        self.vertex.resolve_neighbours()
        self.assertEqual({3}, self.vertex._possible_values)
        self.assertEqual(True, self.vertex._solved)

    def test_no_solutions(self):
        self.vertex._possible_values = {1, 2}
        self.vertex.set_neighbour(self.solved_vertex)
        with self.assertRaises(ValueError):
            self.vertex.set_neighbour(self.solved_vertex_2)

    def test_set_neighbours(self):
        self.vertex.set_neighbours({self.neighbour_vertex, self.other_neighbour_vertex})
        self.assertEqual({self.neighbour_vertex, self.other_neighbour_vertex}, self.vertex._neighbours)

    def test_alert_neighbours(self):
        self.vertex._neighbours = {self.neighbour_vertex, self.other_neighbour_vertex}
        self.other_neighbour_vertex._neighbours = {self.neighbour_vertex, self.vertex}
        self.neighbour_vertex._neighbours = {self.vertex, self.other_neighbour_vertex}
        self.vertex._possible_values = {1}
        self.vertex._solved = True
        self.vertex.alert_neighbours()
        self.assertEqual({3, 7}, self.neighbour_vertex._possible_values)
        self.assertEqual({5, 9}, self.other_neighbour_vertex._possible_values)

    def test_alert_neighbours_after_solve(self):
        self.vertex._neighbours = {self.neighbour_vertex, self.other_neighbour_vertex}
        self.other_neighbour_vertex._neighbours = {self.neighbour_vertex, self.vertex}
        self.neighbour_vertex._neighbours = {self.vertex, self.other_neighbour_vertex}
        self.vertex.rule_out({2, 3})
        self.assertEqual({3, 7}, self.neighbour_vertex._possible_values)
        self.assertEqual({5, 9}, self.other_neighbour_vertex._possible_values)
