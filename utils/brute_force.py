import os


def clear():
    os.system('clear')


seen_graphs = set()
skipped_graphs = list()


class BruteForce:

    def __init__(self, graph):
        self._main_graph = graph.copy()

    def take_move(self, move):
        self._main_graph.set_value(index=move["index"],
                                   value=move["value"])

    def no_further_moves(self):
        return self.is_solved() or self.is_impossible()

    def is_solved(self):
        return self._main_graph.is_solved()

    def is_impossible(self):
        return self._main_graph.is_impossible()

    def get_graph(self):
        return self._main_graph

    def force(self):
        return self.force_depth_first()

    def force_depth_first(self):
        if self.no_further_moves():
            return self._main_graph
        forced_results = self._force_depth_first_algo()
        for result in forced_results:
            if result.is_solved():
                return result
        return forced_results[0]

    def _is_next_move_after_a_zero(self, move):
        lowest_zero = self._main_graph.lowest_empty_cell()
        return move["distance"] > lowest_zero

    def _force_depth_first_algo(self):
        forced_results = list()
        for move in self._main_graph.yield_possible_moves():
            forcer = BruteForce(self._main_graph)
            if self._is_next_move_after_a_zero(move):
                forcer._main_graph.no_solutions()
                forced_results.append(forcer._main_graph)
                continue
            forcer.take_move(move=move)
            fingerprint = forcer.fingerprint()
            self.print()
            if fingerprint in seen_graphs:
                skipped_graphs.append(fingerprint)
                continue
            forced_results.append(forcer.force_depth_first())
        return forced_results

    # def force_pick_best_move(self):
    #     if self.no_further_moves():
    #         return self._main_graph
    #     forced_results = self._force_pick_best_move_algo()
    #     for result in forced_results:
    #         if result.is_solved():
    #             return result
    #     return forced_results[0]

    def fingerprint(self):
        return self._main_graph.fingerprint()

    # def _force_pick_best_move_algo(self):
    #     possible_options = list()
    #     forced_results = list()
    #     for move in self._main_graph.yield_possible_moves():
    #         forcer = BruteForce(self._main_graph)
    #         forcer.take_move(move=move)
    #         fingerprint = forcer.fingerprint()
    #         if fingerprint in seen_graphs:
    #             skipped_graphs.append(fingerprint)
    #             continue
    #         seen_graphs.add(fingerprint)
    #         delta = (forcer._main_graph.get_values() - self._main_graph.get_values()).sum()
    #         possible_options.append([delta, forcer])
    #     possible_options.sort(key=lambda x: x[0], reverse=True)
    #     for option in possible_options:
    #         self.print()
    #         forcer = option[1]
    #         forced_results.append(forcer.force_pick_best_move())
    #     return forced_results

    def print(self):
        clear()
        print(self._main_graph.get_values())
        print(f"Seen: {len(seen_graphs)}")
        print(f"Skipped: {len(skipped_graphs)}")

