from utils.graph import Graph
from utils.brute_force import BruteForce
import numpy as np


class Solver:

    def __init__(self, puzzle, sub_box_height=3, sub_box_width=3):
        self._puzzle = puzzle
        self._shape = self._puzzle.shape
        self._settings = {"rows": self._puzzle.shape[0],
                          "columns": self._puzzle.shape[1],
                          "sub_box_height": sub_box_height,
                          "sub_box_width": sub_box_width,
                          "possible_cell_values": [i + 1 for i in range(self._puzzle.shape[0])]}
        self._graph = Graph(self._settings)
        self._set_starting_values()

    def _set_starting_values(self):
        self._graph.init_values(self._puzzle)

    def _quick_parse(self):
        self._graph.alert_all()

    def _brute_force(self):
        self._graph = BruteForce(self._graph).force()

    def solve(self):
        if self._is_solved():
            return self._graph.get_values()
        self._quick_parse()
        if self._is_solved():
            return self._graph.get_values()
        self._brute_force()
        if self._is_solved():
            return self._graph.get_values()

    def _is_solved(self):
        return self._graph.is_solved() or self._graph.is_impossible()
