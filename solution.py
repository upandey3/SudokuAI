assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

#declaring keys and units including the diagonal units
cols = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(r, c) for r in ['ABC','DEF', 'GHI'] for c in ['123', '456', '789']]
# Diagonal units - ['A1', 'B2, 'C3, ..., 'I9' ], ['A9,'B8','C7', ..., 'I1']
diag_unit1 = [r + c for r,c in zip(rows, cols)] # the first main diagonal
diag_unit2 = [r + c for r,c in zip(rows, cols[::-1])] # the second main diagonal
# units and peers now contain the diagonals as well
unitlist = row_units + col_units + square_units + [diag_unit1] + [diag_unit2]
units = {s:[unit for unit in unitlist if s in unit] for s in boxes}
peers = {s: set(sum(units[s], [])) - set([s]) for s in boxes}

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    boxes = [box for box in values if len(values[box]) == 2]
    possible_twins = [[b1, b2] for i, b1 in enumerate(boxes) for j, b2 in enumerate(boxes) if j > i and b1 != b2 and values[b1] == values[b2]]
    for pair in possible_twins:
        s = values[pair[0]]
        for unit in units[pair[0]]:
            if pair[1] in unit:
                for box in unit:
                    if box != pair[0] and box != pair[1]:
                        for c in s:
                            assign_value(values, box, values[box].replace(c, ''))
    return values
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

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
    d = {}
    s = '123456789'
    for i, v in enumerate(grid):
        if grid[i] == '.':
            d[boxes[i]] = s
        else:
            d[boxes[i]] = grid[i]
    assert(len(d) == 81)
    return d

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[box]) for box in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print (''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print (line)
    return values

def eliminate(values):
    """
    This function finds the boxes with determined values and eliminates those values from its
    peer units including the diagonal units (if the box is in the diagonal)
    """
    known = [box for box in values if len(values[box]) == 1]
    for box in known:
        c = values[box]
        for peer in peers[box]:
            if c in values[peer]:
                assign_value(values, peer, values[peer].replace(c, ''))
    return values

def only_choice(values):
    """
    This function finds the boxes in units for which there is only one possible value in that
    unit and assigns those values to those boxes. The units include the diagonal units
    """
    for unit in unitlist:
        for c in cols:
            dplaces = [box for box in unit if c in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], c)
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
        before_reduce = len([box for box in values if len(values[box]) == 1])
        eliminate(values)
        only_choice(values)
        after_reduce = len([box for box in values if len(values[box]) == 1])
        stalled = after_reduce == before_reduce
        if len([box for box in values if len(values[box]) == 0]):
            return False
    return values

def search(values):

    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # Reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False # Can't be solved

    # if solved, return
    if len([s for s in values if len(values[s]) == 1]) == 81:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    val, key = min([len(values[s]), s] for s in values if len(values[s]) > 1)

    # Use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for c in values[key]:
        temp = values.copy()
        assign_value(temp, key, c)
        temp[key] = c
        result = search(temp)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #
    return search(grid_values(grid))

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


# values1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
# values = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
# a = grid_values(values)
# display(a)
# print('\n')
# # a = eliminate(a)
# # display(a)
# # print('\n')
# # b = only_choice(a)
# # display(b)
# # if a == b:
#     # print ('Same')
# display(search(a))
