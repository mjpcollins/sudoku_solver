import numpy as np
from utils.graph import Graph


class SudokuPuzzle:

    def __init__(self, puzzle, init_graph=True):
        self._puzzle_array = puzzle
        self._size = self._puzzle_array.shape[0]
        self._graph = None
        if init_graph:
            self._graph = Graph(self._size)
            self._init_values()

    def _init_values(self):
        for index, value in np.ndenumerate(self._puzzle_array):
            if value != 0:
                self._graph.quick_set_value(index, value)

    def set_value(self, index, value):
        self._graph.set_value(index, value)

    def get_all_possible_moves(self):
        moves = []
        possible_moves = self.get_possible_values()
        for index in possible_moves:
            value_set = possible_moves[index]
            if len(value_set) > 1:
                distance = index[1] + self._size * index[0]
                for value in value_set:
                    moves.append({"index": index,
                                  "value": value,
                                  "distance": distance})
        moves.sort(key=lambda x: (x["distance"], x["value"]))
        return moves

    def lowest_empty_cell(self):
        for index, value in np.ndenumerate(self.get_values()):
            distance = index[1] + self._size * index[0]
            if value == 0:
                return {"index": index, "distance": distance}
        return None

    def update_unknowns(self):
        for vertex in self._graph.vertexes.values():
            if not vertex.is_solved():
                vertex.resolve_neighbours()

    def update_all(self):
        for vertex in self._graph.vertexes.values():
            vertex.resolve_neighbours()

    def copy(self):
        duplicate_puzzle = SudokuPuzzle(self._puzzle_array.copy(), init_graph=False)
        duplicate_puzzle._graph = self._graph.copy()
        return duplicate_puzzle

    def is_solved(self):
        return not (0 in self.get_values())

    def get_values(self):
        values_array = np.empty(shape=(self._size, self._size))
        values_array.flat = [self._graph.vertexes[index].get_known_value()
                             for index, _ in np.ndenumerate(values_array)]
        return values_array

    def get_possible_values(self):
        return {index: self._graph.vertexes[index].get_possible_values() for index in self._graph.vertexes}
