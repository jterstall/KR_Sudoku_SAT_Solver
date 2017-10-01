import pycosat 
import sudoku_encoding
import solver_efficient

def pair_row_col_encoding(encodings, N):
    for i in range(0, len(encodings)):
        if len(encodings[i]) >= 2:
            if encodings[i][0] > 0:
                    if len(encodings[i]) == 2:
                        reversed_list = sudoku_encoding.reverse_encode_pair(encodings[i], N)
                        _, possible_values_counter = divmod(i, 9)
                        j = i  
                        while True:
                            j += 1
                            if j == len(encodings):
                                break
                            if len(encodings[j]) >= 2:
                                if encodings[j][0] > 0:
                                    possible_values_counter += 1
                                    print(j)
                                    if len(encodings[j]) == 2:
                                        reversed_list_matching = sudoku_encoding.reverse_encode_pair(encodings[j], N)
                                        if reversed_list == reversed_list_matching:
                                            for k in range(i+1, j-1):
                                                for number in encodings[k]:
                                                    print(encodings[k])
                                                    matching_number = sudoku_encoding.reverse_encode_solo(number, N)
                                                    if matching_number == reversed_list[0] or matching_number == reversed_list[1]:
                                                        encodings[k].remove(number)
                                                        print("removed")
                                            values_list_counter = 9 - possible_values_counter
                                            m = j
                                            while True:
                                                m += 1
                                                if m == len(encodings):
                                                    break
                                                if len(encodings[m]) >= 2:
                                                    if encodings[m][0] > 0:
                                                        values_list_counter +=1
                                                        for number in encodings[m]:
                                                            matching_number = sudoku_encoding.reverse_encode_solo(number, N)
                                                            if matching_number == reversed_list[0] or matching_number == reversed_list[1]:
                                                                encodings[m].remove(number)
                                                                print("removed")
                                                    if values_list_counter == 9:
                                                        break
                            if possible_values_counter == 9:
                                break
    return encodings

# Don't add clauses if a cell that is filled in affects it.
def encoding_pair(sudoku, N):
    encodings = []
    encodings = solver_efficient.encoding_efficient(sudoku, N)
    encodings = pair_row_col_encoding(encodings, N)
    return encodings

def solver_pair(sudoku, N):
    encodings = encoding_pair(sudoku, N)
    print("Encoding length pair: {0} clauses".format(len(encodings)))
    solved = pycosat.solve(encodings)
    return sudoku_encoding.reverse_encoding(solved, N)

