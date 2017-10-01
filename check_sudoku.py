import itertools

def sudoku_ok(row, N):
    return len(row) == N and sum(row) == sum(set(row)) and all(number > 0 for number in row)

def validate_sudoku(grid, N):
    bad_rows = [row for row in grid if not sudoku_ok(row, N)]
    grid = list(zip(*grid))
    bad_cols = [col for col in grid if not sudoku_ok(col, N)]
    squares = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
          square = list(itertools.chain(row[j:j+3] for row in grid[i:i+3]))
          square = [element for tupl in square for element in tupl]
          squares.append(square)
    bad_squares = [square for square in squares if not sudoku_ok(square, N)]
    return not any((bad_rows, bad_cols, bad_squares))