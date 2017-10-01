import pycosat 
import sudoku_encoding

def filled_in_encoding_efficient(encodings, sudoku, N):
    filled_in = []
    for i in range(N):
        for j in range(N):
            current_number = sudoku[i][j]
            if current_number != 0:
                # Store filled in as true
                encoded_number = sudoku_encoding.transform(i, j, current_number, N)
                encodings.append([encoded_number])
                filled_in.append(encoded_number)
                # Store rest of digits as false
                for d in [digit for digit in range(1, 10) if digit != current_number]:
                    encodings.append([-sudoku_encoding.transform(i, j, d, N)])
    return encodings, filled_in

def check_cell_filled_in(row, col, filled_in, N):
    for d in range(1, 10):
        if sudoku_encoding.transform(row, col, d, N) in filled_in:
            return True
    return False

def ind_cell_encoding_efficient(encodings, filled_in, N):
    for i in range(N):
        for j in range(N):
            all_possible_values = []
            cell_filled_in = check_cell_filled_in(i, j, filled_in, N)
            if not cell_filled_in:
                # Do regular encoding if not filled in, else no encoding needed for individual cells
                for d in range(1, 10):
                    row_contains_digit = check_row_for_digit(i, d, filled_in, N)
                    col_contains_digit = check_col_for_digit(j, d, filled_in, N)
                    block_contains_digit = check_block_for_digit(i, j, d, filled_in, N)
                    if not any((row_contains_digit, col_contains_digit, block_contains_digit)):
                        d_transform = sudoku_encoding.transform(i, j, d, N)
                        all_possible_values.append(d_transform)
                encodings.append(all_possible_values)
                for k in range(len(all_possible_values)):
                    for l in range(k+1, len(all_possible_values)):
                        encodings.append([-all_possible_values[k], -all_possible_values[l]])
    return encodings

def check_row_for_digit(row, d, filled_in, N):
    for col in range(N):
        if sudoku_encoding.transform(row, col, d, N) in filled_in:
            return True
    return False

def row_cell_encoding_efficient(encodings, filled_in, N):
    for i in range(N):
        for d in range(1, 10):
            all_possible_values = []
            row_contains_digit = check_row_for_digit(i, d, filled_in, N)
            if not row_contains_digit:
                for j in range(N):
                    col_contains_digit = check_col_for_digit(j, d, filled_in, N)
                    block_contains_digit = check_block_for_digit(i, j, d, filled_in, N)
                    if not any((col_contains_digit, block_contains_digit)):
                        d_transform = sudoku_encoding.transform(i, j, d, N)   
                        all_possible_values.append(d_transform) 
                encodings.append(all_possible_values)
                for j in range(len(all_possible_values)):
                    for k in range(j+1, len(all_possible_values)):
                        encodings.append([-all_possible_values[j], -all_possible_values[k]])
    return encodings

def check_col_for_digit(col, d, filled_in, N):
    for row in range(N):
        if sudoku_encoding.transform(row, col, d, N) in filled_in:
            return True
    return False
    
def col_cell_encoding_efficient(encodings, filled_in, N):
    for j in range(N):
        for d in range(1, 10):
            all_possible_values = []
            col_contains_digit = check_col_for_digit(j, d, filled_in, N)
            if not col_contains_digit:
                for i in range(N):
                    row_contains_digit = check_row_for_digit(i, d, filled_in, N)
                    block_contains_digit = check_block_for_digit(i, j, d, filled_in, N)
                    if not any((row_contains_digit, block_contains_digit)):
                        d_transform = sudoku_encoding.transform(i, j, d, N)               
                        all_possible_values.append(d_transform)
                encodings.append(all_possible_values)
                for i in range(len(all_possible_values)):
                    for k in range(i+1, len(all_possible_values)):
                        encodings.append([-all_possible_values[i], -all_possible_values[k]])
    return encodings

def check_block_for_digit(i, j, d, filled_in, N):
    starting_i = i - (i % 3)
    starting_j = j - (j % 3)
    for k in range(0, 3):
        for l in range(0, 3):
            if(sudoku_encoding.transform(starting_i+k, starting_j+l, d, N) in filled_in):
                return True
    return False
    
def block_cell_encoding_efficient(encodings, filled_in, N):
    for i in range(0, N, 3):
        for j in range(0, N, 3):
            for d in range(1, 10):
                all_possible_values = []
                block_contains_digit = check_block_for_digit(i, j, d, filled_in, N)
                if not block_contains_digit:
                    for k in range(0, 3):
                        for l in range(0, 3):
                            row_contains_digit = check_row_for_digit(i+k, d, filled_in, N)
                            col_contains_digit = check_col_for_digit(j+l, d, filled_in, N)
                            if not any((row_contains_digit, col_contains_digit)):
                                d_transform = sudoku_encoding.transform(i+k, j+l, d, N)
                                all_possible_values.append(d_transform)
                    encodings.append(all_possible_values) 
                    for k in range(len(all_possible_values)):
                        for l in range(k+1, len(all_possible_values)):
                            encodings.append([-all_possible_values[k], -all_possible_values[l]])
    return encodings

def pair_row_col_encoding(encodings, N):
    for i in range(0, 1):
        for j in range(0, 1):
            print(encodings[i][j])
# Don't add clauses if a cell that is filled in affects it.
def encoding_efficient(sudoku, N):
    encodings = []
    encodings, filled_in = filled_in_encoding_efficient(encodings, sudoku, N)
    encodings = ind_cell_encoding_efficient(encodings, filled_in, N)
    encodings = row_cell_encoding_efficient(encodings, filled_in, N)
    encodings = col_cell_encoding_efficient(encodings, filled_in, N)
    encodings = block_cell_encoding_efficient(encodings, filled_in, N)
    print("yes")
    pair_row_col_encoding(encodings, N)
    return encodings

def solver_efficient(sudoku, N):
    encodings = encoding_efficient(sudoku, N)
    print("Encoding length efficient: {0} clauses".format(len(encodings)))
    solved = pycosat.solve(encodings)
    return sudoku_encoding.reverse_encoding(solved, N)

