import numpy as np
from utils.vertex import Vertex


class Graph:

    def __init__(self, puzzle_settings_dict):
        self._settings = puzzle_settings_dict
        self._impossible = False
        self._graph = GraphInitialiser(self._settings).create_graph()

    def __str__(self):
        return str(self.get_values())

    def init_values(self, puzzle):
        for index, value in np.ndenumerate(puzzle):
            if value != 0:
                self.quick_set_value(index, value)
        return True

    def quick_set_value(self, index, value):
        self.set_value(index, value, alert_neighbours=False)

    def set_value(self, index, value, alert_neighbours=True):
        try:
            self._graph[index[0]][index[1]].only_allow(values_set={value},
                                                       alert_neighbours=alert_neighbours)
        except ValueError:
            self.no_solutions()
            return False

    def alert_all(self):
        def alert(vertex):
            vertex.alert_neighbours()
        vectorized_alert = np.vectorize(alert)
        try:
            vectorized_alert(self._graph)
        except ValueError:
            self.no_solutions()

    def no_solutions(self):
        self._graph = GraphInitialiser(self._settings).create_graph(possible_cell_values={-1},
                                                                    link_all=False)
        self._impossible = True

    def yield_possible_moves(self):
        def get_values_from_vertex(vertex):
            return vertex.get_values()
        vectorized_possible_values = np.vectorize(get_values_from_vertex)
        options_matrix = vectorized_possible_values(self._graph)
        all_choices = []
        for index, options in np.ndenumerate(options_matrix):
            if len(options) > 1:
                for choice in options:
                    index_array = np.array(index)
                    dist = index_array[0] + index_array[1] * self._graph.shape[1]
                    all_choices.append({"index": index_array,
                                        "value": choice,
                                        "distance": dist})
        all_choices.sort(key=lambda x: x["distance"])
        for choice in all_choices:
            yield choice

    def lowest_empty_cell(self):
        def get_known_value_from_vertex(vertex):
            return vertex.get_known_value()
        vectorized_known_values = np.vectorize(get_known_value_from_vertex)
        known_values_matrix = vectorized_known_values(self._graph)
        for index, value in enumerate(known_values_matrix.flat):
            if value == 0:
                return index

    def copy(self):
        new_graph = Graph(self._settings.copy())
        new_graph.init_values(self.get_values())
        return new_graph

    def is_solved(self):
        return not (0 in self.get_values())

    def is_impossible(self):
        return self._impossible

    def get_values(self):
        def get_values_from_vertex(x):
            return x.get_known_value()

        vectorized_known_values = np.vectorize(get_values_from_vertex)
        return vectorized_known_values(self._graph)

    def get_possible_values(self):
        def get_possible_values_from_vertex(x):
            return x.get_values()

        vectorized_possible_values = np.vectorize(get_possible_values_from_vertex)
        return vectorized_possible_values(self._graph)

    def fingerprint(self):
        return hash(str(self._graph))


class GraphInitialiser:

    def __init__(self, puzzle_settings_dict):
        self._settings = puzzle_settings_dict
        self._rows = self._settings["rows"]
        self._columns = self._settings["columns"]
        self._sub_box_height = self._settings["sub_box_height"]
        self._sub_box_width = self._settings["sub_box_width"]
        self._possible_cell_values = self._settings["possible_cell_values"]
        self._graph = None

    def create_graph(self, possible_cell_values=None, link_all=True):
        if not possible_cell_values:
            possible_cell_values = self._possible_cell_values
        self._graph = np.empty([self._rows, self._columns], dtype=object)
        self._graph.flat = [Vertex(possible_cell_values) for _ in self._graph.flat]
        if link_all:
            self._link_all()
        return self._graph

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


def split(array, nrows, ncols):
    """Split a matrix into sub-matrices."""
    # TODO 2021-01-16: reference or rewrite
    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))
