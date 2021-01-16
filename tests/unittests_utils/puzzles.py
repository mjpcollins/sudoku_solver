import glob
import numpy as np

all_puzzles = [np.load(file) for file in glob.glob("data/*puzzle.npy")]
all_solutions = [np.load(file) for file in glob.glob("data/*solution.npy")]



