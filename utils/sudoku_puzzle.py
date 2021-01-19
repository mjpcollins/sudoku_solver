import numpy as np
from utils.graph import Graph


class SudokuPuzzle:

    def __init__(self, puzzle, init_graph=True):
        self._puzzle_array = puzzle
        self._size = self._puzzle_array.shape[0]
        self._graph = None
        if init_graph:
            self._graph = Graph(self._size,
                                possible_values={i for i in range(1, self._size + 1)})
            self._init_values()

    def set_value(self, index, value):
        self._graph.set_value(index, value)

    def get_values(self):
        values_array = np.empty(self._puzzle_array.shape)
        values_array.flat = [self._graph.vertexes[index].known_value
                             for index, _ in np.ndenumerate(values_array)]
        return values_array

    def is_solved(self):
        for vertex in self._graph.vertexes.values():
            if vertex.known_value == 0:
                return False
        return True

    def update_all(self):
        for vertex in self._graph.vertexes.values():
            vertex.resolve_neighbours()

    def update_unknowns(self):
        for vertex in self._graph.vertexes.values():
            if not vertex.solved:
                vertex.resolve_neighbours()

    def yield_all_possible_moves(self):
        for i, j in np.ndindex((self._size, self._size)):
            vertex = self._graph.vertexes[(i, j)]
            if not vertex.solved:
                distance = vertex.id[1] + self._size * vertex.id[0]
                for value in vertex.possible_values:
                    yield {"index": vertex.id,
                           "known_value": value,
                           "distance": distance}

    def lowest_empty_cell(self):
        for i, j in np.ndindex((self._size, self._size)):
            vertex = self._graph.vertexes[(i, j)]
            if not vertex.solved:
                return vertex.id[1] + self._size * vertex.id[0]

    def copy(self):
        duplicate_puzzle = SudokuPuzzle(self._puzzle_array, init_graph=False)
        duplicate_puzzle._graph = self._graph.copy()
        return duplicate_puzzle

    def _init_values(self):
        for index, value in np.ndenumerate(self._puzzle_array):
            if value != 0:
                self._graph.quick_set_value(index, value)
