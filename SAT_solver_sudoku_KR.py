import pycosat
import numpy as np

# Global sudoku length
N = 9

# Link to encoding a cell: https://nickp.svbtle.com/sudoku-satsolver, https://github.com/ContinuumIO/pycosat/blob/master/examples/sudoku.py
def transform(cell_row, cell_col, digit):
    return int(cell_row*N*N + cell_col*N + digit)

def ind_cell_encoding(encodings):
    for i in range(N):
        for j in range(N):
            all_possible_values = []
            for d in range(1, 10):
                d_transform = transform(i, j, d)
                all_possible_values.append(d_transform)
                for other_d in range(d+1, 10):
                    encodings.append([-d_transform, -transform(i, j, other_d)])
            encodings.append(all_possible_values)
    return encodings

def row_cell_encoding(encodings):
    for i in range(N):
        for d in range(1, 10):
            all_possible_values = []
            for j in range(N):
                d_transform = transform(i, j, d)
                all_possible_values.append(d_transform)
                for other_j in range(j+1, N):
                    encodings.append([-d_transform, -transform(i, other_j, d)])
            encodings.append(all_possible_values)
    return encodings
    
def col_cell_encoding(encodings):
    for j in range(N):
        for d in range(1, 10):
            all_possible_values = []
            for i in range(N):
                d_transform = transform(i, j, d)
                all_possible_values.append(d_transform)
                for other_i in range(i+1, N):
                    encodings.append([-d_transform, -transform(other_i, j, d)])
            encodings.append(all_possible_values)
    return encodings
    
     
def block_cell_encoding(encodings):
    for i in range(0, N, 3):
        for j in range(0, N, 3):
            for d in range(1, 10):
                all_possible_values = []
                for k in range(0, 3):
                    for l in range(0, 3):
                        d_transform = transform(i+k, j+l, d)
                        all_possible_values.append(d_transform)
                        for other_d in range(d+1, 10):
                            encodings.append([-d_transform, -transform(i+k, j+l, other_d)])  
                encodings.append(all_possible_values)
    return encodings
                
def filled_in_encoding(encodings, sudoku):
    for i in range(N):
        for j in range(N):
            current_number = sudoku[i][j]
            if current_number > 0:
                encodings.append([transform(i, j, current_number)])
    return encodings
    
def encoding(sudoku):
    encodings = []
    encodings = ind_cell_encoding(encodings)
    encodings = row_cell_encoding(encodings)
    encodings = col_cell_encoding(encodings)
    encodings = block_cell_encoding(encodings)
    encodings = filled_in_encoding(encodings, sudoku)
    return encodings

def reverse_encoding(solved):
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

def solver(sudoku):
    encodings = encoding(sudoku)
    print("Encoding length naive: {0} clauses".format(len(encodings)))
    solved = pycosat.solve(encodings)
    return(reverse_encoding(solved))

# Don't add clauses if a cell that is filled in affects it.
def encoding_efficient(sudoku):
    encodings = []
    encodings, filled_in = filled_in_encoding_efficient(encodings, sudoku)
    encodings = ind_cell_encoding_efficient(encodings, filled_in)
    encodings = row_cell_encoding_efficient(encodings, filled_in)
    encodings = col_cell_encoding_efficient(encodings, filled_in)
    encodings = block_cell_encoding_efficient(encodings, filled_in)
    return encodings

def filled_in_encoding_efficient(encodings, sudoku):
    filled_in = []
    for i in range(N):
        for j in range(N):
            current_number = sudoku[i][j]
            if current_number != 0:
                # Store filled in as true
                encoded_number = transform(i, j, current_number)
                encodings.append([encoded_number])
                filled_in.append(encoded_number)
                # Store rest of digits as false
                for d in [digit for digit in range(1, 10) if digit != current_number]:
                    encodings.append([-transform(i, j, d)])
    return encodings, filled_in

def check_cell_filled_in(row, col, filled_in):
    for d in range(1, 10):
        if transform(row, col, d) in filled_in:
            return True
    return False

def ind_cell_encoding_efficient(encodings, filled_in):
    for i in range(N):
        for j in range(N):
            all_possible_values = []
            cell_filled_in = check_cell_filled_in(i, j, filled_in)
            if not cell_filled_in:
                # Do regular encoding if not filled in, else no encoding needed for individual cells
                for d in range(1, 10):
                    d_transform = transform(i, j, d)
                    all_possible_values.append(d_transform)
                    for other_d in range(d+1, 10):
                        encodings.append([-d_transform, -transform(i, j, other_d)])
                encodings.append(all_possible_values)
    return encodings

def check_row_for_digit(row, d, filled_in):
    for col in range(N):
        if transform(row, col, d) in filled_in:
            return True
    return False

def row_cell_encoding_efficient(encodings, filled_in):
    for i in range(N):
        for d in range(1, 10):
            all_possible_values = []
            row_contains_digit = check_row_for_digit(i, d, filled_in)
            if not row_contains_digit:
                for j in range(N):
                    d_transform = transform(i, j, d)                
                    all_possible_values.append(d_transform)
                    for other_j in range(j+1, N):
                        encodings.append([-d_transform, -transform(i, other_j, d)])
                encodings.append(all_possible_values)
    return encodings

def check_col_for_digit(col, d, filled_in):
    for row in range(N):
        if transform(row, col, d) in filled_in:
            return True
    return False
    
def col_cell_encoding_efficient(encodings, filled_in):
    for j in range(N):
        for d in range(1, 10):
            all_possible_values = []
            col_contains_digit = check_col_for_digit(j, d, filled_in)
            if not col_contains_digit:
                for i in range(N):
                    d_transform = transform(i, j, d)               
                    all_possible_values.append(d_transform)
                    for other_i in range(i+1, N):
                        encodings.append([-d_transform, -transform(other_i, j, d)])
                encodings.append(all_possible_values)
    return encodings

def check_block_for_digit(i, j, d, filled_in):
    for k in range(0, 3):
        for l in range(0, 3):
            if(transform(i+k, j+l, d) in filled_in):
                return True
    return False
    
def block_cell_encoding_efficient(encodings, filled_in):
    for i in range(0, N, 3):
        for j in range(0, N, 3):
            for d in range(1, 10):
                all_possible_values = []
                block_contains_digit = check_block_for_digit(i, j, d, filled_in)
                if not block_contains_digit:
                    for k in range(0, 3):
                        for l in range(0, 3):
                            d_transform = transform(i+k, j+l, d)
                            all_possible_values.append(d_transform)
                            for other_d in range(d+1, 10):
                                encodings.append([-d_transform, -transform(i+k, j+l, other_d)])  
                    encodings.append(all_possible_values)
    return encodings

def solver_efficient(sudoku):
    encodings = encoding_efficient(sudoku)
    print("Encoding length efficient: {0} clauses".format(len(encodings)))
    solved = pycosat.solve(encodings)
    return reverse_encoding(solved)

def test_naive(sudoku):
    print("Sudoku to solve naive:")
    print(sudoku)
    print("Solved sudoku naive:")
    print(solver(sudoku))

# TODO: paper noemen?
def test_efficient(sudoku):
    print("Sudoku to solve efficient:")
    print(sudoku)
    print("Solved sudoku efficient:")
    print(solver_efficient(sudoku))

def main():
    sudoku = np.load("data\Easy\sudoku-Easy-0.npy")
    test_naive(sudoku)
    test_efficient(sudoku)
    
# TODO: Volgens mij kan je nog meer clauses skippen door in de clauses van andere digits ook nog de al ingevulde te filteren
if __name__ == '__main__':
    main()