from utils.graph import Graph
import numpy as np


class Solver:

    def __init__(self, puzzle, sub_box_height=3, sub_box_width=3):
        self._puzzle = puzzle
        self._settings = {"rows": self._puzzle.shape[0],
                          "columns": self._puzzle.shape[1],
                          "sub_box_height": sub_box_height,
                          "sub_box_width": sub_box_width,
                          "possible_cell_values": [i + 1 for i in range(self._puzzle.shape[0])]}
        self._graph = Graph(self._settings)

    def _set_starting_values(self):
        for index, vertex in np.ndenumerate(self._graph):
            values[index] = vertex.get_values()

    def solve(self, puzzle):
        return puzzle
