import pycosat
import sudoku_encoding

def ind_cell_encoding(encodings, N):
    for i in range(N):
        for j in range(N):
            all_possible_values = []
            for d in range(1, 10):
                d_transform = sudoku_encoding.transform(i, j, d, N)
                all_possible_values.append(d_transform)
                for other_d in range(d+1, 10):
                    encodings.append([-d_transform, -sudoku_encoding.transform(i, j, other_d, N)])
            encodings.append(all_possible_values)
    return encodings

def row_cell_encoding(encodings, N):
    for i in range(N):
        for d in range(1, 10):
            all_possible_values = []
            for j in range(N):
                d_transform = sudoku_encoding.transform(i, j, d, N)
                all_possible_values.append(d_transform)
                for other_j in range(j+1, N):
                    encodings.append([-d_transform, -sudoku_encoding.transform(i, other_j, d, N)])
            encodings.append(all_possible_values)
    return encodings
    
def col_cell_encoding(encodings, N):
    for j in range(N):
        for d in range(1, 10):
            all_possible_values = []
            for i in range(N):
                d_transform = sudoku_encoding.transform(i, j, d, N)
                all_possible_values.append(d_transform)
                for other_i in range(i+1, N):
                    encodings.append([-d_transform, -sudoku_encoding.transform(other_i, j, d, N)])
            encodings.append(all_possible_values)
    return encodings
    
     
def block_cell_encoding(encodings, N):
    for i in range(0, N, 3):
        for j in range(0, N, 3):
            for d in range(1, 10):
                all_possible_values = []
                for k in range(0, 3):
                    for l in range(0, 3):
                        d_transform = sudoku_encoding.transform(i+k, j+l, d, N)
                        all_possible_values.append(d_transform)
                        for other_d in range(d+1, 10):
                            encodings.append([-d_transform, -sudoku_encoding.transform(i+k, j+l, other_d, N)])  
                encodings.append(all_possible_values)
    return encodings
                
def filled_in_encoding(encodings, sudoku, N):
    for i in range(N):
        for j in range(N):
            current_number = sudoku[i][j]
            if current_number > 0:
                encodings.append([sudoku_encoding.transform(i, j, current_number, N)])
    return encodings
    
def encoding(sudoku, N):
    encodings = []
    encodings = ind_cell_encoding(encodings, N)
    encodings = row_cell_encoding(encodings, N)
    encodings = col_cell_encoding(encodings, N)
    encodings = block_cell_encoding(encodings, N)
    encodings = filled_in_encoding(encodings, sudoku, N)
    return encodings

def solver(sudoku, N):
    encodings = encoding(sudoku, N)
    print("Encoding length naive: {0} clauses".format(len(encodings)))
    solved = pycosat.solve(encodings)
    return sudoku_encoding.reverse_encoding(solved, N)