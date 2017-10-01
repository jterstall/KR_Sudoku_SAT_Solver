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
                    d_transform = sudoku_encoding.transform(i, j, d, N)
                    all_possible_values.append(d_transform)
                    for other_d in range(d+1, 10):
                        encodings.append([-d_transform, -sudoku_encoding.transform(i, j, other_d, N)])
                encodings.append(all_possible_values)
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
                    if not col_contains_digit:
                        d_transform = sudoku_encoding.transform(i, j, d, N)                
                        all_possible_values.append(d_transform)
                        for other_j in range(j+1, N):
                            other_j_transform = sudoku_encoding.transform(i, other_j, d, N)
                            if not other_j_transform in filled_in:
                                encodings.append([-d_transform, -other_j_transform])
                encodings.append(all_possible_values)
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
                    if not row_contains_digit:
                        d_transform = sudoku_encoding.transform(i, j, d, N)               
                        all_possible_values.append(d_transform)
                        for other_i in range(i+1, N):
                            other_i_transform = sudoku_encoding.transform(other_i, j, d, N)
                            if not other_i_transform in filled_in:
                                encodings.append([-d_transform, -other_i_transform])
                encodings.append(all_possible_values)
    return encodings

def check_block_for_digit(i, j, d, filled_in, N):
    for k in range(0, 3):
        for l in range(0, 3):
            if(sudoku_encoding.transform(i+k, j+l, d, N) in filled_in):
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
                            d_transform = sudoku_encoding.transform(i+k, j+l, d, N)
                            all_possible_values.append(d_transform)
                            for other_d in range(d+1, 10):
                                encodings.append([-d_transform, -sudoku_encoding.transform(i+k, j+l, other_d, N)])  
                    encodings.append(all_possible_values)
    return encodings

# Don't add clauses if a cell that is filled in affects it.
def encoding_efficient(sudoku, N):
    encodings = []
    encodings, filled_in = filled_in_encoding_efficient(encodings, sudoku, N)
    encodings = ind_cell_encoding_efficient(encodings, filled_in, N)
    encodings = row_cell_encoding_efficient(encodings, filled_in, N)
    encodings = col_cell_encoding_efficient(encodings, filled_in, N)
    encodings = block_cell_encoding_efficient(encodings, filled_in, N)
    return encodings

def solver_efficient(sudoku, N):
    encodings = encoding_efficient(sudoku, N)
    print("Encoding length efficient: {0} clauses".format(len(encodings)))
    solved = pycosat.solve(encodings)
    return sudoku_encoding.reverse_encoding(solved, N)