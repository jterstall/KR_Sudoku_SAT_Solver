import itertools

def sudoku_ok(line):
    return (len(line) == 9 and sum(line) == sum(set(line)))

def validate_sudoku(grid):
    bad_rows = [row for row in grid if not sudoku_ok(row)]
    grid = list(zip(*grid))
    bad_cols = [col for col in grid if not sudoku_ok(col)]
    squares = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
          square = list(itertools.chain(row[j:j+3] for row in grid[i:i+3]))
          square = [element for tupl in square for element in tupl]
          squares.append(square)
    bad_squares = [square for square in squares if not sudoku_ok(square)]
    return not any((bad_rows, bad_cols, bad_squares))