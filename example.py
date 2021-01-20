import numpy as np
from utils import Solver

puzzle = np.load("data/hard_puzzle.npy")[6]  # Take the sixth puzzle in the list
print(puzzle)
solver = Solver(puzzle)
solution = solver.solve()
print(solution)
