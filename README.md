# sudoku_solver
Solver of Sudoku puzzles using a graph

## Background & Inspiration

Sudoku puzzles are a constraint problem where rows, columns, and boxes all apply constraints on each cell.

As these puzzles have been around for a long time, many techniques and algorithms to solve the puzzles have been developed.

One particularly interesting way of thinking about Sudoku puzzles is as a graph.

[Ishaan Gupta (2020)](https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072) 
uses a graph abstraction of the Sudoku puzzle and applies a Graph Colouring algorithm to solve the puzzle.

However, there are some issues with Ishaan Gupta's implementation:
- Explicitly adding edges to the nodes and adding weights to the edges is a superfluous abstraction. We only care about
    cells linking to other cells. Ideally vertexes know their neighbours, but do not keep track of edges, and
- There is excessive hard coding and poor optimisation.

In addition, while the Graph Colouring algorithm Gupta implemented was interesting, I thought it might be possible
to do slightly better by having the vertexes cascade updates rather than check every cell.

## Implementation

#### utils/vertex.py
Every cell will be imagined as a vertex. This vertex class has the ability to be set to a value and to have 
neighbours added. This class is able to check its neighbours for any "solved" vertexes and narrow down 
the possible values based on its neighbours. In addition, this class can request all of its neighbours
to perform an update. When there is a contradiction between a vertex's possible values and the
neighbour's value, a ValueError is thrown.  

#### utils/graph.py
A graph class contains all of the vertexes. On initialisation, the graph class will initialise the vertexes
then link them all together. Each vertex is neighbours to all vertexes on its row, on its column, and in its 
sub box. The graph has that ability to set values of the vertexes and request updates for all vertexes.

#### utils/sudoku_puzzle.py
A puzzle class handles the interaction between numpy and the graph class. It has all the expected initialisation,
setting, getting, and updating methods. There are also methods to generate a list of all possible moves
and the location of the first 0 value cell.

#### utils/solver.py & Depth First Solving Method
In the Solver class there is a depth first solving method. Interestingly for very easy, easy, and medium puzzles,
no use of the depth first methods are required. Initialisation of the graph with puzzle inputs will cascade
all of the constraints and solve them all in about the same length of time (between 0.002 seconds and 0.02 seconds).
Averages were: 0.006 seconds for very easy, 0.007 seconds for easy, 0.006 seconds for medium.

However, the hard puzzles require a guess to be made. They could not be solved just by filling out the starting 
numbers. For this I employed a quite simple depth first algorithm. 


    Class Solver:
    
            ...
    
        def _sub_solve_process(self, move):
            try:
                self._sudoku.set_value(index=move["index"], value=move["known_value"])
                self._sudoku.update_unknowns()
                if self._sudoku.is_solved():
                    return self._sudoku.get_values()
                return self._depth_first_algo()
            except ValueError:
                return {-1}
    
        def _depth_first_algo(self):
            for move in self._good_moves():
                sub_solver = Solver(self._puzzle)
                sub_solver._sudoku = self._sudoku.copy()
                solution = sub_solver._sub_solve_process(move=move)
                if -1 not in solution:
                    return solution
            return {-1}
        

The basic method involves the two methods _sub_solve_process and _depth_first_algo.

The depth_first_algo method is initiated when basic constraints do not solve the puzzle. It loops over all 
possible "good moves" in the current state of the puzzle. In each loop it creates another Solver object
and copies the underlying graph. The move is taken on this copied graph and an update over the unknown 
values is performed. 

To prevent the Solver from trying too many moves in an impossible puzzle it looks for "good moves". A "good move" 
is a move than fills the first 0 value cell. If there are no moves that fill the first 0 value cell, then
the puzzle is impossible and we can quit early. 

If the puzzle still isn't solved it repeats the depth first algo. If at any point
a move creates an unsolvable graph, one of the vertexes will raise a ValueError. This is caught and 
returned as a set containing -1. A set is returned as it simpler to handle a check in the depth_first_algo 
for whether the sub_process produced a solution. 

The solve times for the hard puzzles on my machine were between 0.03 seconds and 7.8 seconds. No multiprocessing
has been implemented in this solution.

#### utils/performance_test.py
Extra class for identifying bottlenecks in the algorithm.

## Summary
This graph implementation has some quite reasonable hard puzzle solve times, but seems slow on the easier puzzles.
It appears that half the time on the easier puzzles is taken up by linking together the vertexes. This section
could be hardcoded for more speed increases. However, this would remove the ability for this Solver to work
with different sized puzzles and would not be elegant.

One potential area for improvement is a better backtracking implementation. 50% of the solving time is taken
up by the duplication of the  graph before taking a move. As the graph automatically cascades values it is 
quite difficult to backtrack by undo-ing the previous move.

## How To Use

Import the Solver from utils then start solving. Examples of Sudoku puzzles are stored in the data folder.
Example usage of the Solver is located in utils/performace_test.py.

Assuming your puzzle is an numpy array, solving is quite simple.

    from utils import Solver
    
    puzzle = np.load("data/very_easy_puzzle.npy")[6]  # Take the sixth puzzle in the list
    solver = Solver(puzzle)
    solution = solver.solve()
    print(solution)

## References

Ishaan, G., 2020. Sudoku Solver — Graph Coloring [Online]. Available from: https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072 
[Accessed 19 January 2021].
