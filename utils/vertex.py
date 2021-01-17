

class Vertex:

    def __init__(self, possible_values):
        self._possible_values = set(possible_values)
        self._neighbours = set()
        self._solved = False
        self._value = 0
        self._check_solved()

    def _check_solved(self):
        self._solved = len(self._possible_values) == 1
        if self._solved:
            self._value = list(self._possible_values)[0]
        return self._solved

    def is_solved(self):
        return self._solved

    def set_value(self, value):
        self._possible_values = {value}
        self._check_solved()

    def rule_out(self, values_set, alert_neighbours=True):
        self._possible_values = self._possible_values - values_set
        if self._possible_values:
            if self._check_solved() and alert_neighbours:
                self.alert_neighbours()
        else:
            raise ValueError("No more possible solutions for this vertex!")

    def only_allow(self, values_set, alert_neighbours=True):
        self._possible_values = values_set
        if self._possible_values:
            if self._check_solved() and alert_neighbours:
                self.alert_neighbours()
        else:
            raise ValueError("No more possible solutions for this vertex!")

    def alert_neighbours(self):
        for neighbour in self._neighbours:
            neighbour.resolve_neighbours()

    def resolve_neighbours(self):
        for neighbour in self._neighbours:
            if neighbour.is_solved():
                self.rule_out(neighbour.get_values(), alert_neighbours=False)

    def set_neighbours(self, vertex_set):
        for vertex in vertex_set:
            self._neighbours.add(vertex)
        self.resolve_neighbours()

    def get_neighbours(self):
        return self._neighbours

    def get_values(self):
        return self._possible_values

    def get_known_value(self):
        return self._value
