import pandas as pd
import collections

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    
    # RD: used for keeping track of all steps
    if len(value) == 1:
        assignments.append(values.copy())
        
    return values

def naked_twins_unitLevel(unit, values):
    """
    Elimiting values using the naked twins strategy.
    
    Limited to only one unit (e.g., row).
    """

    # Finding all the values
    unit_values = [values[box] for box in unit]
    
    # Finding naked twins
    twins = [item for 
             item, count in collections.Counter(unit_values).items()
             if (count == 2) & (len(item) == 2)]

    # If there is any naked twins
    if twins:
    
        # Finding all the digits that can be removed
        digits_to_remove = list(set([digit for twin in twins for digit in list(twin)]))

        # Eliminate the naked twins as possibilities in their unit
        for box in unit:
            # We don't want to remove the twins from twins!
            if values[box] not in twins:
                for digit_to_remove in digits_to_remove:                    # Removing the twins digits from their unit boxes
                    new_value = values[box].replace(digit_to_remove,'')
                    values = assign_value(values, box, new_value)

    return values
    
    
    
def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find all row instances of naked twins
    for row in list('ABCDEFGHI'):
        # Making rows
        row_unit = cross(row, '123456789')
        # Removing twins for each peer
        values = naked_twins_unitLevel(row_unit, values)
        
    # Find all column instances of naked twins
    for col in list('123456789'):
        # Making cols
        col_unit = cross('ABCDEFGHI', col)
        # Removing twins for each peer
        values = naked_twins_unitLevel(col_unit, values)
                        
    # Finding all 3x3 square instances of naked twins
    square_units = [cross(r,c) for r in ['ABC','DEF','GHI']
                    for c in ['123','456','789']]
    for square_unit in square_units:
        # Removing twins for each peer
        values = naked_twins_unitLevel(square_unit, values)
        
    # Finding all Diagonal instances of naked twins
    rows = 'ABCDEFGHI'
    cols = '123456789'
    diag1 = [rows[i]+cols[i] for i in range(len(rows))]
    diag2 = [rows[i]+cols[len(rows)-1-i] for i in range(len(rows))]
    diagonals = [diag1, diag2]

    for diag_unit in diagonals:
        # Removing twins for each peer
        values = naked_twins_unitLevel(diag_unit, values)   
    
    return values


    
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 9*9
    
    # list of labels for each box
    boxes = list(cross('ABCDEFGHI','123456789'))
    # convert the grid into a list
    grid = list(grid)
    
    grid_dict = dict()
    
    for i in range(len(grid)):
        if grid[i] == '.':
            grid_dict[boxes[i]] = '123456789'
        else:
            grid_dict[boxes[i]] = grid[i]
            
    return grid_dict
    
    

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass



def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    assert len(values.keys()) == 9 * 9
    
    for key in list(values.keys()):
        # if it is a final value
        if len(values[key]) == 1:
            
            # row units
            row_unit = cross(key[0], '123456789')
            # cols units
            column_unit = cross('ABCDEFGHI', key[1])
            
            # square units
            row_index = 'ABCDEFGHI'.index(key[0])
            col_index = '123456789'.index(key[1])
            row_group = row_index//3
            col_group = col_index//3
            sqaure_unit = cross('ABCDEFGHI'[row_group*3: (row_group+1)*3],\
                                '123456789'[col_group*3: (col_group+1)*3])
            ## Main Peers
            peers = [row_unit, column_unit, sqaure_unit]
            
            # Diagonal units
            rows = 'ABCDEFGHI'
            cols = '123456789'
            diag1 = [rows[i]+cols[i] for i in range(len(rows))]
            diag2 = [rows[i]+cols[len(rows)-1-i] for i in range(len(rows))]

            for unit in peers:
                for box in unit:
                    if (box != key):
                        new_value = values[box].replace(values[key],'')
                        values = assign_value(values, box, new_value)                
            
            # Only if the box is on diagonal units -- eliminate             
            if key in diag1:
                for box in diag1:
                    if (box != key):
                        new_value = values[box].replace(values[key],'')
                        values = assign_value(values, box, new_value)

            if key in diag2:
                for box in diag2:
                    if (box != key):
                        new_value = values[box].replace(values[key],'')
                        values = assign_value(values, box, new_value)
            
    return values



def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
                        
    # Constructing row units
    for row in list('ABCDEFGHI'):
        row_units = cross(row, '123456789')
        
        # Finding the digits that have appeared only once as a possibility
        for digit in '123456789':
            dplaced = [unit for unit in row_units if digit in values[unit]]
            if len(dplaced) == 1:
                values = assign_value(values, dplaced[0], digit)
                 
                            
    # Constructing column units
    for col in list('123456789'):
        col_units = cross('ABCDEFGHI', col)
        
        # Finding the digits that have appeared only once as a possibility
        for digit in '123456789':
            dplaced = [unit for unit in col_units if digit in values[unit]]
            if len(dplaced) == 1:
                values = assign_value(values, dplaced[0], digit)
        
        
    # Constructing 3x3 sqaures units
    square_units = [cross(r,c) for r in ['ABC','DEF','GHI'] for c in ['123','456','789']]
    
    for square_unit in square_units:
        # Finding the digits that have appeared only once as a possibility
        for digit in '123456789':
            dplaced = [unit for unit in square_unit if digit in values[unit]]
            if len(dplaced) == 1:
                values = assign_value(values, dplaced[0], digit)
                
                
    # Diaglong units
    rows = 'ABCDEFGHI'
    cols = '123456789'
    diag1 = [rows[i]+cols[i] for i in range(len(rows))]
    diag2 = [rows[i]+cols[len(rows)-1-i] for i in range(len(rows))]
    diagonals = [diag1, diag2]

    for diag in diagonals:
        # Finding the digits that have appeared only once as a possibility
        for digit in '123456789':
            dplaced = [unit for unit in diag if digit in values[unit]]
            if len(dplaced) == 1:
                values = assign_value(values, dplaced[0], digit)
    
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use naked twins technique for elimination
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
  
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values) 
    
    # Stop if there a is mistake in the soduko
    if values is False:
        return False
    
    # Stop if the sodoku is solved
    solved_values = len([box for box in values.keys() if len(values[box]) == 1])
    if len(values) == solved_values:
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    unfilled = [(key, value, len(value)) for key, value in values.items() if len(value) > 1]
    unfilled_df = pd.DataFrame(unfilled, columns = ['unit','options','number_of_options'])
    fewest_possibilities = unfilled_df.sort_values('number_of_options').iloc[0,]
    unit = fewest_possibilities['unit']
    options = list(fewest_possibilities['options'])

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for each in options:
        values_cp = values.copy()
        values_cp[unit] = each
        attempt =  search(values_cp)
        
        if attempt:
            return attempt
        

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    # Converting the grid_string to a dictionary
    values = grid_values(grid)
    # And solving using search
    solution = search(values)
    
    if solution:
        return solution
    else:
        return 'found no solution'
    
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
