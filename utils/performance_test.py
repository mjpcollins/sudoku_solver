import time
import numpy as np
from utils.solver import Solver
from numpy.testing import assert_array_equal


class PerformanceTest:

    def __init__(self):
        self._puzzles_in_each_set = 15
        self._v_easy = np.load("data/very_easy_puzzle.npy")
        self._v_easy_solutions = np.load("data/very_easy_solution.npy")

        self._easy = np.load("data/easy_puzzle.npy")
        self._easy_solutions = np.load("data/easy_solution.npy")

        self._medium = np.load("data/medium_puzzle.npy")
        self._medium_solutions = np.load("data/medium_solution.npy")

        self._hard = np.load("data/hard_puzzle.npy")
        self._hard_solutions = np.load("data/hard_solution.npy")

    def solve_all(self):
        self.solve_all_minus_hard()
        self.time_solve(self.solve_hard)

    def solve_all_minus_hard(self):
        self.time_solve(self.solve_very_easy)
        self.time_solve(self.solve_easy)
        self.time_solve(self.solve_medium)

    def solve_one_hard(self, choice=0):
        solver = Solver(self._hard[choice])
        assert_array_equal(self._hard_solutions[choice], solver.solve())

    def time_solve(self, func):
        print(f"Average solve time for {func.__name__}: {func()}")

    def solve_very_easy(self):
        solve_times = []
        for idx, puzzle in enumerate(self._v_easy):
            t1 = time.time()
            solver = Solver(puzzle)
            assert_array_equal(self._v_easy_solutions[idx], solver.solve())
            t2 = time.time()
            solve_time = t2 - t1
            print(f"    Solve time for very easy {idx}: "
                  f"{solve_time}")
            solve_times.append(solve_time)
        return sum(solve_times) / len(solve_times)

    def solve_easy(self):
        solve_times = []
        for idx, puzzle in enumerate(self._easy):
            t1 = time.time()
            solver = Solver(puzzle)
            assert_array_equal(self._easy_solutions[idx], solver.solve())
            t2 = time.time()
            solve_time = t2 - t1
            print(f"    Solve time for easy {idx}: "
                  f"{solve_time}")
            solve_times.append(solve_time)
        return sum(solve_times) / len(solve_times)

    def solve_medium(self):
        solve_times = []
        for idx, puzzle in enumerate(self._medium):
            t1 = time.time()
            solver = Solver(puzzle)
            assert_array_equal(self._medium_solutions[idx], solver.solve())
            t2 = time.time()
            solve_time = t2 - t1
            print(f"    Solve time for medium {idx}: "
                  f"{solve_time}")
            solve_times.append(solve_time)
        return sum(solve_times) / len(solve_times)

    def solve_hard(self):
        solve_times = []
        for idx, puzzle in enumerate(self._hard):
            t1 = time.time()
            solver = Solver(puzzle)
            assert_array_equal(self._hard_solutions[idx], solver.solve())
            t2 = time.time()
            solve_time = t2 - t1
            print(f"    Solve time for hard {idx}: {solve_time}")
            solve_times.append(solve_time)
        return sum(solve_times) / len(solve_times)


if __name__ == '__main__':
    import cProfile
    import pstats

    pt = PerformanceTest()

    profile = cProfile.Profile()
    profile.runcall(pt.solve_all)
    ps = pstats.Stats(profile)
    ps.print_stats()


