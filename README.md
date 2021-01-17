# sudoku_solver
Solver of Sudoku puzzles using a graph

## Background

- Sudokus are interesting
- If you think about it, they're kinda like a graph

## Inspiration

- I was inspired by this article on Sudoku with graph colouring https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072,
    but my implimentation differs in a few ways.
- The edge abstraction was superflious. We were not putting any weight on these edges, so neighbours was all the 
    vertexes needed to know
- The article had a huge amount of hard coding. Not that it matters, but mine can work for any sized Sudoku...
- The hard coding of the block connections is ridiculous.

## Abstraction

- Lets imagine the cells are vertexes
- Lets link all the vertexes to their constraining cells and neighbours
- This look a bit like a graph
- Now whenever I update a vertex the constraints are propagated across the graph
- Somewhat similar to graph colouring

## Solving Very Easy -> Medium

- No further work was required to solve V. Easy to Medium
- The applying of numbers in a cell caused constraining to happen
- Speed is a tad on the slow side for these Sudokus

## Solving Hard Puzzles

- These puzzles could not be solved by filling out the starting numbers
- We just need to take a punt and see where it gets us
- Employed quite simple backtracking
- Graph is copied at each stage (this seems to be an area where it's a bit slow, but hash table look up
    would be a lot of effort and is unlikely to give a speed up
- One could abstract backtracking into a super graph, but in this implementation it is in a recursive algorithm
- The solve speed is *okay* but could be better
- While the graph abstraction was academically interesting, I don't think it offered a speed increase over
    standard constraint application (despite mostly relying on sets). 
    If this was coded in a graph database (e.g. TigerGraph, Neo4j) I reckon this could be solved much faster.

## How To Use

- Import away then bish bosh bash

## References

- Just that article... Rest came from mah noggin.
