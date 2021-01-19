from utils.vertex import Vertex
from math import sqrt
import itertools


class Graph:

    def __init__(self, size, possible_values, init=True):
        self._size = size
        self._possible_cell_values = set(possible_values)
        self.vertexes = dict()
        if init:
            self.create_graph()

    def create_graph(self):
        for vertex_id in itertools.product(range(self._size), range(self._size)):
            self.vertexes[vertex_id] = Vertex(self._possible_cell_values,
                                              vertex_id=vertex_id,
                                              graph=self)
        self._link_all()

    def set_value(self, index, value):
        self.vertexes[index].set_vertex_value(value=value)

    def quick_set_value(self, index, value):
        self.vertexes[index].set_vertex_value(value=value,
                                              update_neighbours=False)

    def update(self):
        for vertexes in self.vertexes.values():
            vertexes.resolve_neighbours()

    def copy(self):
        duplicate_graph = Graph(size=self._size,
                                possible_values=self._possible_cell_values,
                                init=False)
        for vertex_index in self.vertexes:
            duplicate_graph.vertexes[vertex_index] = self.vertexes[vertex_index].copy(duplicate_graph)
        return duplicate_graph

    def _link_all(self):
        self._link(axis=0)
        self._link(axis=1)
        self._link_sub_boxes()

    def _link(self, axis=0):
        for i in range(self._size):
            vertex_row_set = set()
            for j in range(self._size):
                if axis == 0:
                    vertex_row_set.add((i, j))
                else:
                    vertex_row_set.add((j, i))
            self._link_all_in_set(vertex_row_set)

    def _link_sub_boxes(self):
        box_size = int(sqrt(self._size))
        boxes = {box_id: set() for box_id in itertools.product(range(box_size), range(box_size))}
        for i in range(self._size):
            for j in range(self._size):
                boxes[(i // box_size, j // box_size)].add((i, j))
        for box in boxes.values():
            self._link_all_in_set(box)

    def _link_all_in_set(self, vertexes):
        vertex_index_set = set(vertexes)
        for vertex_index in vertexes:
            vertex_index_set.remove(vertex_index)
            self.vertexes[vertex_index].add_neighbours(vertex_index_set)
            vertex_index_set.add(vertex_index)
