import time
import numpy as np
from utils.solver import Solver
from numpy.testing import assert_array_equal


class PerformanceTest:

    def __init__(self):
        self.puzzles = {"very_easy": {"puzzles": np.load("data/very_easy_puzzle.npy"),
                                      "solutions": np.load("data/very_easy_solution.npy")},
                        "easy": {"puzzles": np.load("data/easy_puzzle.npy"),
                                 "solutions": np.load("data/easy_solution.npy")},
                        "medium": {"puzzles": np.load("data/medium_puzzle.npy"),
                                   "solutions": np.load("data/medium_solution.npy")},
                        "hard": {"puzzles": np.load("data/hard_puzzle.npy"),
                                 "solutions": np.load("data/hard_solution.npy")}}

    def solve_all(self):
        self.time_solve(self.solve_and_time, "very_easy")
        self.time_solve(self.solve_and_time, "easy")
        self.time_solve(self.solve_and_time, "medium")
        self.time_solve(self.solve_and_time, "hard")

    @staticmethod
    def time_solve(func, var):
        print(f"Average solve time for {func.__name__}: {func(var)}")

    def solve_and_time(self, difficulty):
        solve_times = []
        for idx, puzzle in enumerate(self.puzzles[difficulty]["puzzles"]):
            t1 = time.time()
            solver = Solver(puzzle)
            assert_array_equal(self.puzzles[difficulty]["solutions"][idx],
                               solver.solve())
            t2 = time.time()
            solve_time = t2 - t1
            print(f"    Solve time for {difficulty} {idx}: "
                  f"{solve_time}")
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


