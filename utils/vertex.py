

class Vertex:

    def __init__(self, possible_values):
        self._possible_values = set(possible_values)
        self._neighbours = set()
        self._solved = False
        self._check_solved()

    def resolve_neighbours(self):
        for neighbour in self._neighbours:
            self._resolve_neighbour(neighbour)

    def set_neighbours(self, vertex_set):
        for vertex in vertex_set:
            self.set_neighbour(vertex)

    def set_neighbour(self, vertex):
        self._neighbours.add(vertex)
        self._resolve_neighbour(vertex)

    def is_solved(self):
        return self._solved

    def _resolve_neighbour(self, neighbour):
        if neighbour.is_solved():
            self.rule_out(neighbour.get_values())

    def rule_out(self, values_set):
        self._possible_values = self._possible_values - values_set
        if self._possible_values:
            if self._check_solved():
                self.alert_neighbours()
        else:
            raise ValueError("No more possible solutions for this vertex!")

    def _check_solved(self):
        self._solved = len(self._possible_values) == 1
        return self._solved

    def get_neighbours(self):
        return self._neighbours

    def get_values(self):
        return self._possible_values

    def alert_neighbours(self):
        for neighbour in self._neighbours:
            neighbour.resolve_neighbours()
