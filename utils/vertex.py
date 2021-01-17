

class Vertex:

    def __init__(self, possible_values, vertex_id, graph, init=True):
        self.id = vertex_id
        self.neighbours = set()
        self._possible_values = set(possible_values)
        self._solved = False
        self._graph = graph
        self._value = 0
        if init:
            self._check_solved()

    def _check_solved(self):
        self._solved = len(self._possible_values) == 1
        if self._solved:
            self._value = list(self._possible_values)[0]
        return self._solved

    def is_solved(self):
        return self._solved

    def set_vertex_value(self, value, update_neighbours=True):
        self._possible_values = {value}
        self._value = value
        self._solved = True
        if update_neighbours:
            self.update_neighbours()

    def update_neighbours(self):
        for neighbour_index in self.neighbours:
            self._graph.vertexes[neighbour_index].resolve_neighbours()

    def resolve_neighbours(self):
        for neighbour_index in self.neighbours:
            neighbour_vertex = self._graph.vertexes[neighbour_index]
            if neighbour_vertex.is_solved():
                self._rule_out(neighbour_vertex.get_known_value())

        if self._possible_values:
            if not self._solved:
                self._check_solved()
        else:
            raise ValueError("No more possible solutions for this vertex!")

    def _rule_out(self, value):
        self._possible_values.discard(value)

    def add_neighbours(self, vertex_set):
        for vertex in vertex_set:
            self.neighbours.add(vertex)
        self.resolve_neighbours()

    def get_neighbours(self):
        return self.neighbours

    def get_possible_values(self):
        return self._possible_values

    def get_known_value(self):
        return self._value

    def copy(self, graph):
        copied_vertex = Vertex(possible_values=self._possible_values,
                               vertex_id=self.id,
                               graph=graph,
                               init=False)
        copied_vertex.neighbours = set(self.get_neighbours())
        copied_vertex._solved = bool(self.is_solved())
        copied_vertex._value = int(self._value)
        return copied_vertex
