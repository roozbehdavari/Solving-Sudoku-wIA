# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem? 
A: Constraint Propagation helps us to reduce the search space. Naked twins refers to cases where two boxes (squares) of a unit (e.g. row) contain the same two possible values. Considering that those two values are bound to be to be used in those two boxes, they cannot to used in only other square of that unit. And therefore, this can be used for eliminating possibilities (i.e., reducing the search space) 


# (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal sudoku provides us with an extra constrain on the possible configuration of digits in sudoku. This can be viewed simply as an extension of unit constrains applied in a regular sudoku; row, column, and 3x3 squares. For diagonal sudoku, the same contain will be applied to both nine diagonal boxes. This constrain further reduces the search space. 


These codes requires **Python 3**.



### Code

* `solution.py` - This is the main code for solving sudoku.
* `solution_test.py` - Is used for testing the solution by running `python solution_test.py`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

