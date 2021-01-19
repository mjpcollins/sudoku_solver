

class Vertex:

    def __init__(self, possible_values, vertex_id, graph, init=True):
        self.id = vertex_id
        self.neighbours = set()
        self.possible_values = set(possible_values)
        self.known_value = 0
        self.solved = False
        self._graph = graph
        if init:
            self._check_solved()

    def add_neighbours(self, vertex_set):
        self.neighbours.update(vertex_set)

    def set_vertex_value(self, value, update_neighbours=True):
        self.possible_values = {value}
        self.known_value = value
        self.solved = True
        if update_neighbours:
            self.update_neighbours()

    def update_neighbours(self):
        for neighbour_index in self.neighbours:
            self._graph.vertexes[neighbour_index].resolve_neighbours()

    def resolve_neighbours(self):
        for neighbour_index in self.neighbours:
            neighbour_vertex = self._graph.vertexes[neighbour_index]
            if neighbour_vertex.solved:
                self.possible_values.discard(neighbour_vertex.known_value)
        self._check_vertex_state()

    def copy(self, graph):
        copied_vertex = Vertex(possible_values=self.possible_values,
                               vertex_id=self.id,
                               graph=graph,
                               init=False)
        copied_vertex.neighbours = set(self.neighbours)
        copied_vertex.solved = self.solved
        copied_vertex.known_value = self.known_value
        return copied_vertex

    def _check_vertex_state(self):
        if self.possible_values:
            if not self.solved:
                self._check_solved()
        else:
            raise ValueError("No more possible solutions for this vertex!")

    def _check_solved(self):
        self.solved = len(self.possible_values) == 1
        if self.solved:
            self.known_value = list(self.possible_values)[0]
        return self.solved
