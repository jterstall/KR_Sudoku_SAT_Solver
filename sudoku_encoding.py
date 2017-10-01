import numpy as np

# Link to encoding a cell: https://nickp.svbtle.com/sudoku-satsolver, https://github.com/ContinuumIO/pycosat/blob/master/examples/sudoku.py
def transform(cell_row, cell_col, digit, N):
    return int(cell_row*N*N + cell_col*N + digit)

def reverse_encode_solo(number, N):
    number, d = divmod(number, N)
    return d

def reverse_encode_pair(numbers, N):
    real_digits = []
    for number in numbers:
        number, d = divmod(number, N)
        if d == 0:
            d = 9
        real_digits.append(d)
    return(real_digits)

def reverse_encoding(solved, N):
    if isinstance(solved, str):
        return "Sudoku could not be solved: %s" % solved
    sudoku = np.zeros((N, N))
    for number in solved:
        if number > 0:
            number, d = divmod(number, N)
            if d == 0:
                number = number - 1
                d = 9
            number, cell_col = divmod(number, N)
            number, cell_row = divmod(number, N)
            sudoku[cell_row][cell_col] = d
    return sudoku