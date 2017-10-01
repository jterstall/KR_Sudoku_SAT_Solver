import numpy as np
import solver_efficient
import solver_naive
import check_sudoku
import solver_pair

def test_naive(sudoku, N):
    print("Sudoku to solve naive:")
    print(sudoku)
    print("Solved sudoku naive:")
    solved_sudoku = solver_naive.solver(sudoku, N)
    print(solved_sudoku)
    print("Is sudoku solved correctly?:")
    print(check_sudoku.validate_sudoku(solved_sudoku, N))

# TODO: paper noemen?
def test_efficient(sudoku, N, recursion):
    print("Sudoku to solve efficient:")
    print(sudoku)
    print("Solved sudoku efficient:")
    solved_sudoku = solver_efficient.solver_efficient(sudoku, N, recursion)
    print(solved_sudoku)
    print("Is sudoku solved correctly?:")
    print(check_sudoku.validate_sudoku(solved_sudoku, N))

def test_pair(sudoku, N):
    print("Sudoku to solve pair:")
    print(sudoku)
    print("Solved sudoku pair:")
    solved_sudoku = solver_pair.solver_pair(sudoku, N)
    print(solved_sudoku)
    print("Is sudoku solved correctly?:")
    print(check_sudoku.validate_sudoku(solved_sudoku, N))

def main():
    # Sudoku length
    N = 9
    sudoku = np.load("data\Easy\sudoku-Easy-0.npy")
    # test_naive(sudoku, N)
    # test_efficient(sudoku, N, False)
    test_pair(sudoku, N)
    
if __name__ == '__main__':
    main()