import numpy as np
from utils.vertex import Vertex


class Graph:

    def __init__(self, puzzle_settings_dict):
        self._rows = puzzle_settings_dict["rows"]
        self._columns = puzzle_settings_dict["columns"]
        self._sub_box_height = puzzle_settings_dict["sub_box_height"]
        self._sub_box_width = puzzle_settings_dict["sub_box_width"]
        self._possible_cell_values = puzzle_settings_dict["possible_cell_values"]
        self._graph = self._create_graph()
        self._link_all()

    def __str__(self):
        return str(self.get_possible_values())

    def get_values(self):
        values = np.empty([self._rows, self._columns], dtype=int)
        for index, vertex in np.ndenumerate(self._graph):
            if vertex.is_solved():
                values[index] = list(vertex.get_values())[0]
            else:
                values[index] = 0
        return values

    def get_possible_values(self):
        values = np.empty([self._rows, self._columns], dtype=set)
        for index, vertex in np.ndenumerate(self._graph):
            values[index] = vertex.get_values()
        return values

    def _create_graph(self):
        graph = np.empty([self._rows, self._columns], dtype=object)
        graph.flat = [Vertex(self._possible_cell_values) for _ in graph.flat]
        return graph

    def _link_all(self):
        self._link_rows()
        self._link_columns()
        self._link_sub_boxes()

    def _link_rows(self):
        for row in self._graph:
            self._link_all_in_set(row)

    def _link_columns(self):
        for column in self._graph.T:
            self._link_all_in_set(column)

    def _link_sub_boxes(self):
        for sub_box in split(self._graph, self._sub_box_height, self._sub_box_width):
            self._link_all_in_set(sub_box.flatten())

    @staticmethod
    def _link_all_in_set(vertexes):
        for vertex in vertexes:
            temp_vertex_set = set(vertexes)
            temp_vertex_set.remove(vertex)
            vertex.set_neighbours(temp_vertex_set)

    def set_value(self, row, column, value):
        value_set = {value}
        temp_set_of_values = set(self._possible_cell_values) - value_set
        self.rule_out_values(row, column, temp_set_of_values)

    def rule_out_values(self, row, column, values):
        self._graph[row][column].rule_out(values)


def split(array, nrows, ncols):
    """Split a matrix into sub-matrices."""
    # TODO 2021-01-16: reference or rewrite
    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))
