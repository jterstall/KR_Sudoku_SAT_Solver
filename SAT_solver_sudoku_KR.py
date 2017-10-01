import numpy as np
import solver_efficient
import solver_naive
import solver_pair

def test_naive(sudoku, N):
    print("Sudoku to solve naive:")
    print(sudoku)
    print("Solved sudoku naive:")
    print(solver_naive.solver(sudoku, N))

# TODO: paper noemen?
def test_efficient(sudoku, N):
    print("Sudoku to solve efficient:")
    print(sudoku)
    print("Solved sudoku efficient:")
    print(solver_efficient.solver_efficient(sudoku, N))

def test_pair(sudoku, N):
    print("Sudoku to solve pair:")
    print(sudoku)
    print("Solved sudoku pair:")
    print(solver_pair.solver_efficient(sudoku, N))

def main():
    # Sudoku length
    N = 9
    sudoku = np.load("data\Easy\sudoku-Easy-0.npy")
    test_naive(sudoku, N)
    test_efficient(sudoku, N)
    # test_pair(sudoku, N)
    
# TODO: Volgens mij kan je nog meer clauses skippen door in de clauses van andere digits ook nog de al ingevulde te filteren
if __name__ == '__main__':
    main()